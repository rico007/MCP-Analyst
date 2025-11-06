#!/bin/bash
set -e

echo "=========================================="
echo "Data Analyst MCP Server - Docker Shutdown"
echo "=========================================="
echo ""

# Check if container is running
if docker ps | grep -q data-analyst-mcp; then
    echo "🛑 Stopping MCP server container..."
    docker-compose stop
    
    echo ""
    echo "✅ Container stopped successfully!"
    echo ""
    echo "To start again, run: ./docker-start.sh"
    echo "To remove completely, run: docker-compose down"
else
    echo "ℹ️  Container is not running"
fi

echo ""
