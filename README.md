# MCP-demo-CSCI-435
# Figma → SonarQube → GitHub PR Workflow with Full Observability

End-to-end automated workflow:
1. Fetch Figma design (via existing Figma MCP server)
2. Generate code  
3. Run SonarQube analysis (real scanner + simulation fallback)
4. Auto-apply patches
5. Verify quality gate
6. Create GitHub PR (via existing GitHub MCP server)

**Features:** Correlation tracking, JSON-RPC correlation, SSE timing, real-time dashboard, secure logging, rate limiting, caching.

## Files

- `workflow.py` - Orchestrator (Figma → Sonar → GitHub)
- `sonar.py` - SonarQube MCP server
- `mcp_helpers.py` - Instrumentation & correlation
- `sse_tracker.py` - SSE event tracking
- `dashboard.py` - Observability dashboard
- `test_sonar.py` - Testing

## Setup

```bash
# Install sonar-scanner
cd ~
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
sudo mv ~/sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner
echo 'export PATH=$PATH:/opt/sonar-scanner/bin' >> ~/.bashrc
source ~/.bashrc

# If no python: sudo apt install python3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens

code .
```
## Install Extensions: Copilot MCP
Ctrl+Shift+X > Search Copilot MCP

## Add github & figma MCP server
File > Open File > Paste ~/.vscode-server/data/User/mcp.json

Paste the config in the json file:
```json
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${input:github_token}"
      }
    },
    "figma/mcp-server-guide": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp",
      "gallery": "https://api.mcp.github.com",
      "version": "1.0.0"
    }
  },
  "inputs": [
    {
      "id": "token",
      "type": "promptString",
      "description": "",
      "password": true
    },
    {
      "type": "promptString",
      "id": "github_token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ]
}
```

## Update .env variables
Navigate to .env and update token variables

## Usage (MCP Server Simulation)

```bash
# Run workflow
python workflow.py

# With dashboard
python dashboard.py 8080  # Terminal 1
python workflow.py "<figma_url>"  # Terminal 2
# Open http://localhost:8080 in your browser

# Test
python test_sonar.py
```

## Usage (MCP Server Prompt)
# NOTE: Users on the Figma Starter plan or with View or Collab seats on paid plans will be limited to up to 6 tool calls per month.
```txt

Do NOT use workflow.py.

As the agent, personally invoke each MCP server tool step-by-step, printing results after each step. For SonarQube analysis, you MUST use the SonarQube MCP server tool (not local scripts or direct terminal commands).

**IMPORTANT:** After extracting code from Figma, you MUST create the extracted code file(s) in the repo (e.g., `figma_extracted/Home.jsx`) before running SonarQube analysis. Do NOT skip this step or attempt to fetch the file from GitHub. The SonarQube MCP server tool must analyze the actual file you created locally.

**IMPORTANT:** Do NOT use any local git or bash commands for branch, commit, or PR operations. Only use the GitHub MCP server tools for all repository actions (branch creation, file commits, pull requests, etc.). If you use any local commands, you must stop and switch to the MCP server tools.

**Step-by-step workflow:**
1. Use the Figma MCP server tool to fetch the design for https://www.figma.com/design/kn0QYBr8YvZp0jX4OgsL9U/Demo?node-id=9-2708&p=f&m=dev
Print: Step name, cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, status (✓/⊘/✗), and all returned data.
2. Use the Figma MCP server tool to extract code files from the design. 
Print: Step name,  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, status, and all returned data.
3. **Create the extracted code file(s) in the repo (e.g., `figma_extracted/Home.jsx`).**
Print: Confirmation,  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms,  and file paths.
4. **When running SonarQube analysis, use the MCP server tool with the following parameters:**
  - `project_key`: your project key
  - `files`: an object mapping filenames to their contents, e.g. `{ "Home.jsx": "<file contents>" }`
Print: The full scan result,  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, including all metrics, issues, code smells, duplications, coverage, and the raw JSON response.
If issues are found: Print issue details, apply up to 3 suggested patches, print patch results, and reanalyze.
5. **After creating the extracted file(s), commit them to the new branch before creating a pull request.**
Print: Confirmation,  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms,  and branch name.
6. Use the SonarQube MCP server tool to poll status with the taskId and print the full scan result (including issues, metrics, etc.).
Print: Step name,  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, status, and all returned data.
7. Use the SonarQube MCP server tool to apply any suggested patches.
Print:  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, patch results and updated analysis.
8. Use the SonarQube MCP server tool to check the quality gate.
Print:  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, full quality gate result and status.
9. Use the GitHub MCP server tool to create a new branch, commit the extracted file(s) to it, and then create a pull request in the repo Tetsukiba/MCP-demo-CSCI-435 (or another repo).
Print:  cid, jsonrpc_id, parent ID, tool name, elapsed time in ms, PR URL and number.
10. At the end, print a summary of all steps, including the full SonarQube scan result, PR URL, tool performance statistics (calls, average time per tool), correlation chain tracking, cid, jsonprc_id and parent IDs.

**Notes:**
- Always check the required input format for each MCP server tool.
- Always print detailed output for each tool call and workflow step, including status icons and all returned data.
- Always commit new or changed files to the branch before creating a PR.
Do not use orchestrator scripts. Advance automatically through each step, confirming completion before proceeding.
```
## Troubleshooting

- If you see "sonar-scanner not found in PATH. Falling back to simulation mode.", install SonarScanner and check your PATH.
```bash
    #For Linux
    sudo apt-get install sonar-scanner
```
- If you see authentication errors, check your tokens in `.env`.
- Always run the dashboard before the workflow to see live metrics.


## Observability

- Correlation IDs across all operations
- Secret redaction (automatic)
- Per-tool metrics
- MCP Inspector: `mcp dev sonar.py`

---

Uses **existing** Figma & GitHub MCP servers - doesn't duplicate them!
