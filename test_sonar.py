#!/usr/bin/env python3
"""Test script to demonstrate Sonar MCP tools with @instrument decorator."""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from sonar import scan, status, apply_patch, quality_gate
from mcp_helpers import TOOL_STATS, log

async def main():
    log("=" * 60)
    log("Starting Sonar MCP Demo")
    log("=" * 60)
    
    # Step 1: Scan code files
    log("\n[STEP 1] Submitting files for analysis...")
    scan_result = await scan(
        project_key="demo-project",
        files={
            "src/app.py": "def unused_function():\n    pass\n\nprint('debug log')",
            "src/utils.py": "console.log('test')\n# TODO: fix this"
        }
    )
    log("Scan submitted: {}", scan_result)
    task_id = scan_result.get("taskId")
    
    # Step 2: Poll status (wait for analysis to complete)
    log("\n[STEP 2] Polling task status...")
    for i in range(6):
        await asyncio.sleep(0.8)
        status_result = await status(task_id=task_id)
        log("Status check {}: {}", i+1, status_result.get("status"))
        
        if status_result.get("status") == "FINISHED":
            if "issues" in status_result:
                log("Issues found: {}", status_result["issues"])
            break
    
    # Step 3: Apply a patch
    log("\n[STEP 3] Applying suggested patch...")
    patch_result = await apply_patch(task_id=task_id, patch_id="remove_unused_function")
    log("Patch applied: {}", patch_result)
    
    # Wait for reanalysis
    await asyncio.sleep(1.5)
    
    # Step 4: Check quality gate
    log("\n[STEP 4] Checking quality gate...")
    gate_result = await quality_gate(project_key="Tetsukiba_MCP-demo-CSCI-435")
    log("Quality gate: {}", gate_result)
    
    # Step 5: Show aggregated stats
    log("\n" + "=" * 60)
    log("TOOL STATISTICS (from @instrument decorator)")
    log("=" * 60)
    for tool_name, stats in TOOL_STATS.items():
        avg_ms = stats["total_ms"] / stats["count"] if stats["count"] > 0 else 0
        log("{}: {} calls, {:.1f}ms total, {:.1f}ms avg", 
            tool_name, stats["count"], stats["total_ms"], avg_ms)
    log("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
