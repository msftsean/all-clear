# Lab 02 Setup Notes

Configured Azure MCP setup for the All Clear repository and validated the prerequisites used to inspect Azure OpenAI, Azure AI Search, and Azure Container Apps from VS Code.

## Steps Completed

1. ✅ Verified Azure CLI is installed (v2.74.0) and available in the Codespaces terminal.
2. ✅ Installed Node.js 20.20.0 via nvm for MCP package compatibility.
3. ✅ Created `.vscode/mcp.json` with Azure MCP server configuration.
4. ✅ Verified Azure MCP server is accessible via npx (v2.0.0-beta.22).
5. ✅ Authenticated Azure CLI using device code flow.
6. ✅ Verified subscription and resource group access for All Clear deployment resources.

## Verification Status

```
Tests passed: 10/10
Points earned: 8.5/8.5
Rubric score: EXEMPLARY
```

## Azure Configuration

**Subscription:** Microsoft Azure Sponsorship  
**Resource Group:** rg-azureday-user-11-use2  
**Workload:** All Clear incident-triage resources

## MCP Configuration

Created `.vscode/mcp.json`:
```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest"]
    }
  }
}
```

## Validation Commands

```bash
# Check Azure CLI status
az account show

# Switch to Node 20 (required for MCP)
source /usr/local/share/nvm/nvm.sh && nvm use 20

# Test MCP server
npx -y @azure/mcp@latest --version

# Run lab verification
python3 labs/02-azure-mcp-setup/test_lab02.py
```

## Testing @azure Queries

After completing setup, test in VS Code Copilot Chat:
- `@azure List my subscriptions`
- `@azure What resource groups do I have?`
- `@azure Show me Azure OpenAI resources that can power QueryAgent classification`
- `@azure Show me Azure AI Search indexes for incident runbooks and SOPs`
- `@azure Show me Azure Container Apps resources for the All Clear backend`
