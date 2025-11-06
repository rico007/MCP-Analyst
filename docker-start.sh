#!/bin/bash
set -e

echo "=========================================="
echo "Data Analyst MCP Server - Docker Startup"
echo "=========================================="
echo ""

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: docker-compose is not installed"
    echo "Please install docker-compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data
fi

# Create user_data directory if it doesn't exist
if [ ! -d "user_data" ]; then
    echo "📁 Creating user_data directory..."
    mkdir -p user_data
fi

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Remember to edit .env if you want to add your MotherDuck token"
fi

# Build and start the container
echo ""
echo "🐳 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting MCP server container..."
docker-compose up -d

echo ""
echo "=========================================="
echo "✅ MCP Server Started Successfully!"
echo "=========================================="
echo ""
echo "Container Status:"
docker-compose ps

echo ""
echo "Next Steps:"
echo "1. Configure Claude Desktop to use the Docker container"
echo "2. Update your claude_desktop_config.json:"
echo ""
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo ""
echo "3. Add this configuration:"
echo ""
cat << 'EOF'
{
  "mcpServers": {
    "data-analyst": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "data-analyst-mcp",
        "python3",
        "server.py"
      ]
    }
  }
}
EOF
echo ""
echo "4. Restart Claude Desktop completely"
echo ""
echo "Useful Commands:"
echo "  View logs:    docker-compose logs -f"
echo "  Stop server:  docker-compose stop"
echo "  Start server: docker-compose start"
echo "  Restart:      docker-compose restart"
echo "  Stop & remove: docker-compose down"
echo "  Full rebuild: docker-compose down && docker-compose up -d --build"
echo ""
