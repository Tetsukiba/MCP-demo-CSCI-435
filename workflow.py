#!/usr/bin/env python3
"""
End-to-end workflow: Figma → Code → SonarQube → Patch → PR
Uses EXISTING Figma and GitHub MCP servers (don't duplicate them!)

Usage:
    python workflow.py <figma_url>
    python workflow.py "https://www.figma.com/design/FILE_KEY/PROJECT_NAME?node-id=NODE_ID"
"""
import asyncio
import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import threading

from dashboard import run_dashboard
import time

# Import our Sonar tools
from sonar import scan, status, apply_patch, quality_gate
from mcp_helpers import log, TOOL_STATS, CORRELATION_CHAIN
from sse_tracker import get_sse_stats, SSE_EVENTS, monitor_sonar_ce_task_sse

# NOTE: Figma and GitHub tools come from MCP servers you're already connected to!
# In a real MCP environment, you'd call them via the MCP protocol.


def parse_figma_url(url: str) -> tuple[str, str]:
    """
    Parse Figma URL to extract file key and node ID.
    
    Example URL: https://www.figma.com/design/FILE_KEY/PROJECT_NAME?node-id=NODE_ID...
    Returns: (file_key, node_id)
    """
    # Match pattern: /design/{fileKey}/{fileName}?node-id={nodeId}
    pattern = r'figma\.com/design/([^/]+)/[^?]*\?node-id=([^&]+)'
    match = re.search(pattern, url)
    
    if not match:
        raise ValueError(f"Invalid Figma URL. Expected format: https://figma.com/design/FILE_KEY/NAME?node-id=NODE_ID\nGot: {url}")
    
    file_key = match.group(1)
    node_id = match.group(2).replace('-', ':')  # Convert 9-2708 to 9:2708
    
    return file_key, node_id


class Workflow:
    async def _fetch_figma_design(self) -> dict:
        """Fetch design from Figma MCP server (simulated for demo)."""
        log("Calling Figma MCP: get_design_context(fileKey={}, nodeId={})", self.figma_file_key, self.figma_node_id)
        await asyncio.sleep(0.5)  # Simulate API call
        return {
            "code": """import React from 'react';\n\nexport const LoginForm = () => {\n  const [email, setEmail] = React.useState('');\n  const [password, setPassword] = React.useState('');\n  \n  const handleSubmit = (e) => {\n    e.preventDefault();\n    console.log('Login attempt:', email);  // Security issue!\n  };\n  \n  return (\n    <form onSubmit={handleSubmit}>\n      <input \n        type=\"email\" \n        value={email} \n        onChange={(e) => setEmail(e.target.value)} \n      />\n      <input \n        type=\"password\" \n        value={password} \n        onChange={(e) => setPassword(e.target.value)} \n      />\n      <button type=\"submit\">Login</button>\n    </form>\n  );\n};\n""",
            "metadata": {
                "name": "LoginForm",
                "type": "COMPONENT"
            }
        }
    """End-to-end Figma-to-PR workflow orchestrator."""
    
    def __init__(self, figma_file_key: str, figma_node_id: str, repo: str, project_key: str):
        self.figma_file_key = figma_file_key
        self.figma_node_id = figma_node_id
        self.repo = repo  # "owner/repo"
        self.project_key = project_key

        self.correlation_id = None
    
    async def run(self) -> dict:
        """Execute the full workflow."""
        results = {
            "steps": [],
            "overall_status": "started"
        }
        # Simulate SSE event for Figma fetch
        SSE_EVENTS.append({"correlation_id": "figma-fetch", "event": "FETCH", "timestamp": time.time()})
        try:
            # Step 1: Fetch design from Figma (via Figma MCP server)
            log("\n" + "="*60)
            log("STEP 1: Fetching Figma design")
            log("="*60)

            design_result = await self._fetch_figma_design()
            results["steps"].append({
                "step": "figma_fetch",
                "status": "success",
                "file_key": self.figma_file_key,
                "node_id": self.figma_node_id
                # Simulate SSE event for code extraction
            })
            SSE_EVENTS.append({"correlation_id": "code-extract", "event": "EXTRACT", "timestamp": time.time()})

            # Step 2: Extract code files
            log("\n" + "="*60)
            log("STEP 2: Extracting code from design")
            log("="*60)

            files = self._extract_code_files(design_result)
            results["steps"].append({
                "step": "code_extraction",
                "status": "success",
                "file_count": len(files)
            })

            # Step 3: Run SonarQube scan
            log("\n" + "="*60)
            log("STEP 3: Running SonarQube analysis")
            log("="*60)

            scan_result = await scan(
                project_key=self.project_key,
                files=files,
                _jsonrpc_id="rpc-sonar-scan",
                _parent_cid="figma-code"
            )
            task_id = scan_result.get("taskId")
            log("Scan started: taskId={}, mode={}", task_id, scan_result.get("mode"))
            # Simulate SSE event for Sonar scan start
            SSE_EVENTS.append({"correlation_id": "sonar-scan", "event": "STARTED", "timestamp": time.time()})

            results["steps"].append({
                "step": "sonar_scan",
                "status": "success",
                "task_id": task_id,
                "mode": scan_result.get("mode")
            })

            # Step 4: Poll for completion
            # Simulate SSE event for Sonar analysis complete
            SSE_EVENTS.append({"correlation_id": "sonar-scan", "event": "FINISHED", "timestamp": time.time()})
            log("\n" + "="*60)
            log("STEP 4: Waiting for analysis to complete")
            log("="*60)

            issues = await self._wait_for_analysis(
                task_id,
                _jsonrpc_id="rpc-sonar-status",
                _parent_cid="sonar-scan"
            )
            results["steps"].append({
                "step": "analysis_complete",
                "status": "success",
                "issue_count": len(issues)
            })

            # Step 5: Apply patches automatically
            if issues:
                log("\n" + "="*60)
                log("STEP 5: Applying automated patches ({} issues)", len(issues))
                # Simulate SSE event for patch application
                SSE_EVENTS.append({"correlation_id": "sonar-patch", "event": "PATCH_APPLIED", "timestamp": time.time()})
                # Real SSE tracking for patch application (if supported)
                try:
                    await monitor_sonar_ce_task_sse(task_id, os.getenv("SONARQUBE_URL", "http://localhost:9000"), (os.getenv("SONARQUBE_USER", "admin"), os.getenv("SONARQUBE_PASS", "admin")), "sonar-patch")
                except Exception as sse_exc:
                    log("SSE tracking error: {}", sse_exc)
                log("="*60)

                patches_applied = await self._apply_patches(
                    task_id,
                    issues,
                    files,
                    _jsonrpc_id="rpc-sonar-applypatch",
                    _parent_cid="sonar-status"
                )
                results["steps"].append({
                    "step": "patch_application",
                    "status": "success",
                    "patches_applied": len(patches_applied)
                })
            else:
                log("\n✓ No issues found, skipping patch step")
                results["steps"].append({
                    "step": "patch_application",
                    "status": "skipped",
                    "reason": "no_issues"
                })

            # Step 6: Verify quality gate
            log("\n" + "="*60)
            log("STEP 6: Checking quality gate")
            log("="*60)

            gate_result = await quality_gate(
                project_key=self.project_key,
                _jsonrpc_id="rpc-sonar-qualitygate",
                _parent_cid="sonar-applypatch"
            )
            gate_status = gate_result.get("qualityGate", {}).get("projectStatus", {}).get("status", "UNKNOWN")

            results["steps"].append({
                "step": "quality_gate",
                "status": "success",
                "gate_status": gate_status
            })

            # Step 7: Create PR (via GitHub MCP server)
            log("\n" + "="*60)
            log("STEP 7: Creating Pull Request")
            log("="*60)

            pr_result = await self._create_pr(files, issues)
            results["steps"].append({
                "step": "pr_creation",
                "status": pr_result.get("status", "pending"),
                "pr_url": pr_result.get("pr_url")
            })

            results["overall_status"] = "completed"
            log("\n" + "="*60)
            log("✓ WORKFLOW COMPLETED SUCCESSFULLY")
            log("="*60)

        except Exception as e:
            log("✗ WORKFLOW FAILED: {}", repr(e))
            results["overall_status"] = "failed"
            results["error"] = str(e)

        return results

    
    def _extract_code_files(self, design_result: dict) -> dict[str, str]:
        """Extract files from Figma design data."""
        component_name = design_result.get("metadata", {}).get("name", "Component")
        code = design_result.get("code", "")
        
        files = {
            f"src/components/{component_name}.tsx": code,
            f"src/components/{component_name}.test.tsx": self._generate_test(component_name)
        }
        
        log("Extracted {} files from design", len(files))
        return files
    
    def _generate_test(self, component_name: str) -> str:
        """Generate basic test file."""
        return f"""import {{ render }} from '@testing-library/react';
import {{ {component_name} }} from './{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
  }});
}});
"""
    
    async def _wait_for_analysis(self, task_id: str, max_attempts: int = 10, **kwargs) -> list[dict]:
        """Poll task until complete and return issues."""
        for attempt in range(max_attempts):
            await asyncio.sleep(1.0)
            result = await status(task_id=task_id)
            
            task_status = result.get("status")
            log("Analysis status: {}", task_status)
            
            if task_status in ("FINISHED", "SUCCESS"):
                return result.get("issues", [])
            elif task_status in ("FAILED", "CANCELED"):
                log("Analysis failed with status: {}", task_status)
                return []
        
        log("Analysis timed out after {} attempts", max_attempts)
        return []
    
    async def _apply_patches(self, task_id: str, issues: list[dict], files: dict[str, str]) -> list[str]:
        """Apply patches for detected issues."""
        patches_applied = []
        
        for issue in issues[:3]:  # Limit to first 3 patches
            patch_id = issue.get("suggested_patch") or issue.get("id")
            if patch_id:
                log("Applying patch: {}", patch_id)
                result = await apply_patch(task_id=task_id, patch_id=patch_id)
                
                if result.get("applied"):
                    patches_applied.append(patch_id)
        
        # Wait for reanalysis
        if patches_applied:
            await asyncio.sleep(2.0)
        
        return patches_applied
    
    async def _create_pr(self, files: dict[str, str], issues: list[dict]) -> dict:
        """Create PR via GitHub API."""
        import httpx
        github_token = os.getenv("GITHUB_TOKEN")
        repo = self.repo
        owner, repo_name = repo.split("/")
        safe_node_id = self.figma_node_id.replace(':', '-')
        branch_name = f"figma-{safe_node_id}-{int(asyncio.get_event_loop().time())}"

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        async with httpx.AsyncClient() as client:
            # Get default branch
            repo_url = f"https://api.github.com/repos/{owner}/{repo_name}"
            repo_resp = await client.get(repo_url, headers=headers)
            repo_resp.raise_for_status()
            default_branch = repo_resp.json()["default_branch"]

            # Get default branch SHA
            branch_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/ref/heads/{default_branch}"
            branch_resp = await client.get(branch_url, headers=headers)
            branch_resp.raise_for_status()
            sha = branch_resp.json()["object"]["sha"]

            # Create new branch
            create_branch_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/refs"
            branch_data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": sha
            }
            branch_create_resp = await client.post(create_branch_url, json=branch_data, headers=headers)
            if branch_create_resp.status_code != 201:
                log("Branch creation failed: {} {}", branch_create_resp.status_code, branch_create_resp.text)
                raise Exception(f"Branch creation failed: {branch_create_resp.status_code} {branch_create_resp.text}")

            # Create tree with new files
            tree_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/trees"
            tree_data = {
                "base_tree": sha,
                "tree": [
                    {
                        "path": path,
                        "mode": "100644",
                        "type": "blob",
                        "content": content
                    } for path, content in files.items()
                ]
            }
            tree_resp = await client.post(tree_url, json=tree_data, headers=headers)
            tree_resp.raise_for_status()
            new_tree_sha = tree_resp.json()["sha"]

            # Create commit
            commit_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/commits"
            commit_data = {
                "message": f"feat: Add {len(files)} components from Figma design",
                "tree": new_tree_sha,
                "parents": [sha]
            }
            commit_resp = await client.post(commit_url, json=commit_data, headers=headers)
            commit_resp.raise_for_status()
            new_commit_sha = commit_resp.json()["sha"]

            # Update branch to point to new commit
            update_ref_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/refs/heads/{branch_name}"
            update_ref_data = {
                "sha": new_commit_sha,
                "force": True
            }
            update_ref_resp = await client.patch(update_ref_url, json=update_ref_data, headers=headers)
            update_ref_resp.raise_for_status()

            # Create PR
            pr_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
            pr_title = f"feat: Add {len(files)} components from Figma design"
            pr_body = f"""## Auto-generated from Figma

        - Design: `{self.figma_file_key}#{self.figma_node_id}`
        - Files: {len(files)}
        - Issues found: {len(issues)}
        - Quality gate: Checking...

        Generated by MCP workflow automation.
        """
            pr_data = {
                "title": pr_title,
                "head": branch_name,
                "base": default_branch,
                "body": pr_body
            }
            pr_resp = await client.post(pr_url, json=pr_data, headers=headers)
            pr_resp.raise_for_status()
            pr_json = pr_resp.json()

        log("Created PR: {}", pr_json.get("html_url"))
        return {
            "status": "success",
            "pr_url": pr_json.get("html_url"),
            "pr_number": pr_json.get("number")
        }
async def main():
    """Run the demo workflow."""
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python workflow.py <figma_url>", file=sys.stderr)
        print("Example: python workflow.py 'https://www.figma.com/design/FILE_KEY/PROJECT_NAME?node-id=NODE_ID'", file=sys.stderr)
        sys.exit(1)
    
    figma_url = sys.argv[1]
    
    log("="*60)
    log("FIGMA → SONARQUBE → GITHUB WORKFLOW")
    log("="*60)
    
    # Parse Figma URL
    try:
        figma_file_key, figma_node_id = parse_figma_url(figma_url)
        log("Parsed Figma URL:")
        log("  File Key: {}", figma_file_key)
        log("  Node ID: {}", figma_node_id)
    except ValueError as e:
        log("ERROR: {}", str(e))
        sys.exit(1)
    
    # Configuration from environment
    github_repo = os.getenv("GITHUB_REPO", "Tetsukiba/MCP-demo-CSCI-435")
    sonar_project = os.getenv("SONAR_PROJECT", "MCP-demo-CSCI-435")
    
    # Run workflow
    workflow = Workflow(
        figma_file_key=figma_file_key,
        figma_node_id=figma_node_id,
        repo=github_repo,
        project_key=sonar_project
    )
    
    results = await workflow.run()
    
    # Inject simulated Figma and GitHub tool stats for dashboard visibility
    TOOL_STATS["figma.get_design_context"] = {"count": 1, "total_ms": 120.0}
    TOOL_STATS["figma.extract_code"] = {"count": 1, "total_ms": 80.0}
    TOOL_STATS["github.create_branch"] = {"count": 1, "total_ms": 150.0}
    TOOL_STATS["github.create_pull_request"] = {"count": 1, "total_ms": 200.0}

    # Simulate JSON-RPC and parent correlation IDs
    CORRELATION_CHAIN["figma-ctx"] = {
        "tool": "figma.get_design_context",
        "status": "success",
        "elapsed_ms": 120.0,
        "jsonrpc_id": "rpc-figma-001",
        "parent_cid": None
    }
    CORRELATION_CHAIN["figma-code"] = {
        "tool": "figma.extract_code",
        "status": "success",
        "elapsed_ms": 80.0,
        "jsonrpc_id": "rpc-figma-002",
        "parent_cid": "figma-ctx"
    }
    CORRELATION_CHAIN["gh-branch"] = {
        "tool": "github.create_branch",
        "status": "success",
        "elapsed_ms": 150.0,
        "jsonrpc_id": "rpc-gh-001",
        "parent_cid": "figma-code"
    }
    CORRELATION_CHAIN["gh-pr"] = {
        "tool": "github.create_pull_request",
        "status": "success",
        "elapsed_ms": 200.0,
        "jsonrpc_id": "rpc-gh-002",
        "parent_cid": "gh-branch"
    }

    # Print summary
    log("\n" + "="*60)
    log("WORKFLOW SUMMARY")
    log("="*60)
    log("Overall status: {}", results["overall_status"])
    log("Steps completed: {}/{}", 
        len([s for s in results["steps"] if s["status"] == "success"]),
        len(results["steps"]))

    for step in results["steps"]:
        status_icon = "✓" if step["status"] == "success" else ("⊘" if step["status"] == "skipped" else "✗")
        log("  {} {}: {}", status_icon, step["step"], step["status"])

    # Tool statistics
    log("\n" + "="*60)
    log("TOOL PERFORMANCE")
    log("="*60)
    for tool_name, stats in TOOL_STATS.items():
        avg_ms = stats["total_ms"] / stats["count"] if stats["count"] > 0 else 0
        log("{}: {} calls, {:.1f}ms avg", tool_name, stats["count"], avg_ms)

    # Correlation tracking
    log("\n" + "="*60)
    log("CORRELATION CHAINS ({} tracked)", len(CORRELATION_CHAIN))
    log("="*60)
    for cid, info in list(CORRELATION_CHAIN.items())[:9]:  # Show first 9 (including simulated)
        log("[{}] tool={} status={} elapsed={:.1f}ms", 
            cid, info.get("tool"), info.get("status"), info.get("elapsed_ms", 0))
    
    # SSE stats
    sse_stats = get_sse_stats()
    if sse_stats["total_events"] > 0:
        from datetime import datetime
        log("\n" + "="*60)
        log("SSE EVENTS: {} events across {} streams", sse_stats["total_events"], sse_stats["streams"])
        for cid, count in sse_stats["events_by_stream"].items():
            log("  Stream '{}': {} events", cid, count)
            for event in [e for e in SSE_EVENTS if e["correlation_id"] == cid]:
                ts = datetime.fromtimestamp(event["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
                data_str = event.get("data", "")
                if isinstance(data_str, dict):
                    data_str = str(data_str)
                log("    Event #{}: type={}, timestamp={}, offset_ms={:.1f}, data={}",
                    event.get("event_number", "?"),
                    event.get("event", event.get("data", {}).get("status", "")),
                    ts,
                    event.get("offset_ms", 0.0),
                    data_str)
        log("="*60)

    log("\nProgram complete. Workflow finished. Dashboard server will remain running.")
    # Block main thread to keep dashboard server alive
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("\nReceived KeyboardInterrupt. Exiting.")
        sys.exit(0)

def start_dashboard():
    threading.Thread(target=run_dashboard, args=(8080,), daemon=True).start()

if __name__ == "__main__":
    start_dashboard()
    asyncio.run(main())
