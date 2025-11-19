# sonar.py
import os
import sys
import time
import json
import asyncio
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from mcp_helpers import instrument, log, cache_get, cache_set
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("sonar")

SONAR_BASE = os.getenv("SONAR_BASE_URL")  # e.g. https://sonarcloud.io or your SonarQube instance
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
SONAR_ORGANIZATION = os.getenv("SONAR_ORGANIZATION", "")  # for SonarCloud
if not SONAR_BASE or not SONAR_TOKEN:
    log("SONAR_BASE_URL or SONAR_TOKEN not set. Sonar server will require these to function.")
    SONAR_BASE = SONAR_BASE or "http://localhost:9000"  # dummy default
    SONAR_TOKEN = SONAR_TOKEN or "dummy-token"  # dummy default

AUTH = (SONAR_TOKEN, "")

# Real scanner integration helpers
async def _run_sonar_scanner(project_key: str, project_dir: Path) -> Optional[str]:
    """Run sonar-scanner CLI and return the compute engine task ID."""
    scanner_cmd = ["sonar-scanner"]
    
    # Check if scanner is available
    if not shutil.which("sonar-scanner"):
        log("sonar-scanner not found in PATH. Falling back to simulation mode.")
        return None
    
    scanner_args = [
        f"-Dsonar.projectKey={project_key}",
        f"-Dsonar.sources=.",
        f"-Dsonar.host.url={SONAR_BASE}",
        f"-Dsonar.token={SONAR_TOKEN}",
    ]
    
    if SONAR_ORGANIZATION:
        scanner_args.append(f"-Dsonar.organization={SONAR_ORGANIZATION}")
    
    try:
        proc = await asyncio.create_subprocess_exec(
            *scanner_cmd, *scanner_args,
            cwd=str(project_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            log("sonar-scanner failed: {}", stderr.decode())
            return None
        
        # Extract task ID from output
        output = stdout.decode()
        for line in output.split('\n'):
            if 'ceTaskId' in line or 'task?id=' in line:
                # Parse task ID from scanner output
                import re
                match = re.search(r'task\?id=([A-Za-z0-9_-]+)', line)
                if match:
                    return match.group(1)
        
        log("Could not extract task ID from scanner output")
        return None
        
    except Exception as e:
        log("Error running sonar-scanner: {}", repr(e))
        return None

async def _poll_ce_task(task_id: str, max_attempts: int = 60) -> dict:
    """Poll SonarQube compute engine task status until complete."""
    async with httpx.AsyncClient(auth=AUTH, timeout=20.0) as client:
        for attempt in range(max_attempts):
            try:
                r = await client.get(f"{SONAR_BASE}/api/ce/task", params={"id": task_id})
                if r.status_code == 200:
                    data = r.json()
                    task_status = data.get("task", {}).get("status")
                    
                    if task_status in ("SUCCESS", "FAILED", "CANCELED"):
                        return data
                    
                    log("CE task {} status: {}", task_id, task_status)
                    await asyncio.sleep(2)
                else:
                    log("CE task poll failed: HTTP {}", r.status_code)
                    await asyncio.sleep(2)
            except Exception as e:
                log("Error polling CE task: {}", repr(e))
                await asyncio.sleep(2)
    
    return {"task": {"status": "TIMEOUT"}}

async def _fetch_issues(project_key: str, chunk_size: int = 100) -> list[dict]:
    """Fetch issues from SonarQube with pagination/chunking."""
    all_issues = []
    page = 1
    
    async with httpx.AsyncClient(auth=AUTH, timeout=30.0) as client:
        while True:
            try:
                r = await client.get(
                    f"{SONAR_BASE}/api/issues/search",
                    params={
                        "componentKeys": project_key,
                        "ps": chunk_size,
                        "p": page,
                        "resolved": "false"
                    }
                )
                
                if r.status_code != 200:
                    log("Failed to fetch issues: HTTP {}", r.status_code)
                    break
                
                data = r.json()
                issues = data.get("issues", [])
                all_issues.extend(issues)
                
                total = data.get("total", 0)
                if len(all_issues) >= total:
                    break
                
                page += 1
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                log("Error fetching issues: {}", repr(e))
                break
    
    return all_issues

@instrument("sonar.scan")
@mcp.tool()
async def scan(project_key: str, files: dict[str, str], **kwargs) -> dict:
    print("SCAN FUNCTION CALLED") # DEBUG
    """
    Submit files for real SonarQube analysis using sonar-scanner.
    Creates temp directory, writes files, runs scanner, returns task ID.
    Falls back to simulation if scanner not available.
    """
    # Try real scanner first
    temp_dir = Path(tempfile.mkdtemp(prefix=f"sonar_{project_key}_"))
    
    try:
        # Write files to temp directory
        for file_path, content in files.items():
            full_path = temp_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
        
        log("Created temp project at {} with {} files", temp_dir, len(files))
        
        # Run scanner
        task_id = await _run_sonar_scanner(project_key, temp_dir)
        
        if task_id:
            # Real scanner succeeded
            cache_set(f"sonar_task:{task_id}", {
                "project": project_key,
                "status": "PENDING",
                "real": True,
                "temp_dir": str(temp_dir)
            })
            return {"taskId": task_id, "status": "PENDING", "mode": "real"}
        
    except Exception as e:
        log("Real scanner error: {}", repr(e))
    
    # Fallback to simulation
    log("Using simulation mode for project {}", project_key)
    task_id = f"sim-task-{int(time.time()*1000)}"
    cache_set(f"sonar_task:{task_id}", {
        "project": project_key,
        "files": files,
        "status": "PENDING",
        "real": False
    })
    asyncio.create_task(_simulate_analysis(task_id))
    
    return {"taskId": task_id, "status": "PENDING", "mode": "simulated"}

async def _simulate_analysis(task_id: str):
    """Simulate analysis with staged SSE-like updates (for demo)."""
    # Each step sleeps then updates cache so pollers can see progress
    steps = [
        ("QUEUED", 0.5),
        ("ANALYZING", 1.0),
        ("COMPUTING", 1.2),
        ("FINISHED", 0.4)
    ]
    for status, delay in steps:
        await asyncio.sleep(delay)
        rec = cache_get(f"sonar_task:{task_id}") or {}
        rec["status"] = status
        # create a small faux issues list on ANALYZING->COMPUTING
        if status == "COMPUTING":
            rec["issues"] = [
                {"id": "ISSUE-1", "rule": "no-dead-code", "message": "Unused function", "location": "src/App.tsx:12", "suggested_patch": "remove_unused_function"},
                {"id": "ISSUE-2", "rule": "no-console", "message": "console.log found", "location": "src/utils.ts:8", "suggested_patch": "replace_with_logger"}
            ]
        cache_set(f"sonar_task:{task_id}", rec)

@instrument("sonar.status")
@mcp.tool()
async def status(task_id: str, **kwargs) -> dict:
    """Poll task status - supports both real and simulated tasks."""
    rec = cache_get(f"sonar_task:{task_id}")
    if not rec:
        return {"error": "task not found"}
    
    # Handle real SonarQube tasks
    if rec.get("real"):
        ce_result = await _poll_ce_task(task_id, max_attempts=1)
        task_status = ce_result.get("task", {}).get("status", "UNKNOWN")
        
        # Update cache
        rec["status"] = task_status
        cache_set(f"sonar_task:{task_id}", rec)
        
        out = {"taskId": task_id, "status": task_status, "mode": "real"}
        
        # If finished, fetch issues
        if task_status == "SUCCESS":
            project_key = rec.get("project")
            issues = await _fetch_issues(project_key)
            rec["issues"] = issues
            cache_set(f"sonar_task:{task_id}", rec)
            out["issues"] = issues
            out["issueCount"] = len(issues)
        
        return out
    
    # Simulated mode
    out = {"taskId": task_id, "status": rec.get("status"), "mode": "simulated"}
    if "issues" in rec:
        out["issues"] = rec["issues"]
    return out

@instrument("sonar.apply_patch")
@mcp.tool()
async def apply_patch(task_id: str, patch_id: str, **kwargs) -> dict:
    """
    Apply a suggested patch from the issues to the file set stored in the task.
    Real world: you'd apply patch and resubmit analysis; here we mutate cached files then mark a 'reanalysis' run.
    """
    rec = cache_get(f"sonar_task:{task_id}")
    if not rec:
        return {"error": "task not found"}
    # naive patch application: record that patch was applied for demo
    applied = rec.setdefault("applied_patches", [])
    applied.append(patch_id)
    rec["status"] = "REANALYZING"
    cache_set(f"sonar_task:{task_id}", rec)
    # re-simulate a short reanalysis
    asyncio.create_task(_simulate_reanalysis(task_id))
    return {"taskId": task_id, "applied": applied}

async def _simulate_reanalysis(task_id: str):
    await asyncio.sleep(1.0)
    rec = cache_get(f"sonar_task:{task_id}") or {}
    # on reanalysis we'll remove one issue to simulate fix
    issues = rec.get("issues", [])
    if issues:
        issues = issues[:-1]
        rec["issues"] = issues
    rec["status"] = "FINISHED"
    cache_set(f"sonar_task:{task_id}", rec)

@instrument("sonar.quality_gate")
@mcp.tool()
async def quality_gate(project_key: str, **kwargs) -> dict:
    """
    Check quality gate status for the project using the real SonarQube API.
    Fails loudly if the API is unreachable or returns an error.
    """
    async with httpx.AsyncClient(auth=AUTH, timeout=20.0) as client:
        r = await client.get(f"{SONAR_BASE}/api/qualitygates/project_status", params={"projectKey": project_key})
        if r.status_code == 200:
            return {"qualityGate": r.json()}
        else:
            raise RuntimeError(f"SonarQube quality gate API error: HTTP {r.status_code} - {r.text}")

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
