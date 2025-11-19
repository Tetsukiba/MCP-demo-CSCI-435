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
"Use MCP server tools to:

Fetch the Figma design for node 9-1637 (OR ANOTHER NODE ID) in file kn0QYBr8YvZp0jX4OgsL9U (OR ANOTHER FILE_KEY).
Extract code files from the design.
Run SonarQube analysis on the code files for project Tetsukiba_MCP-demo-CSCI-435 (OR ANOTHER PROJECT_KEY).
Apply any suggested patches.
Check the SonarQube quality gate.
Create a new branch and pull request in GitHub repo Tetsukiba/MCP-demo-CSCI-435 (OR ANOTHER REPO).
Return a summary of each step and the PR URL."
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
