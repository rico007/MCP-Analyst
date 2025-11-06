#!/bin/bash

# Data Analyst MCP Server Setup Script (FastMCP Version)

set -e

echo "============================================"
echo "Data Analyst MCP Server Setup (FastMCP)"
echo "============================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Install dependencies
echo ""
echo "Installing Python dependencies (including FastMCP)..."
pip3 install -r requirements.txt

echo ""
echo "✓ Dependencies installed successfully"

# Get the absolute path to server.py
SERVER_PATH="$(cd "$(dirname "$0")" && pwd)/server.py"

# Make server.py executable
chmod +x server.py

echo ""
echo "============================================"
echo "Setup Complete! (FastMCP Version)"
echo "============================================"
echo ""
echo "✨ You're using the FastMCP version with:"
echo "   • Cleaner code (50% less boilerplate)"
echo "   • Better type safety"
echo "   • Automatic validation"
echo ""
echo "Next steps:"
echo ""
echo "1. Add this configuration to your Claude Desktop config file:"
echo ""

# Detect OS and show appropriate path
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="~/Library/Application Support/Claude/claude_desktop_config.json"
    echo "   macOS Config Location:"
    echo "   $CONFIG_PATH"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    CONFIG_PATH="%APPDATA%/Claude/claude_desktop_config.json"
    echo "   Windows Config Location:"
    echo "   $CONFIG_PATH"
else
    CONFIG_PATH="~/.config/Claude/claude_desktop_config.json"
    echo "   Linux Config Location:"
    echo "   $CONFIG_PATH"
fi

echo ""
echo "2. Add this JSON configuration:"
echo ""
cat << EOF
{
  "mcpServers": {
    "data-analyst-fastmcp": {
      "command": "python3",
      "args": [
        "$SERVER_PATH"
      ],
      "env": {
        "MOTHERDUCK_TOKEN": ""
      }
    }
  }
}
EOF

echo ""
echo "3. (Optional) Get a MotherDuck token from https://motherduck.com"
echo "   and add it to the MOTHERDUCK_TOKEN field for cloud persistence"
echo ""
echo "4. Restart Claude Desktop completely"
echo ""
echo "5. Start analyzing data! Try:"
echo "   - Load example_data.csv as customers"
echo "   - What are the top customers by revenue?"
echo ""
echo "✨ Enjoy the cleaner FastMCP implementation!"
echo ""
