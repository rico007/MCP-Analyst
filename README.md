# MCP Data Analyst Server

Transform Claude (or ChatGPT) into a powerful data analyst with SQL capabilities. Import CSVs or Google Sheets, run complex queries, and get instant insights - all through natural language.

## 🎯 What This Does

This MCP server lets AI assistants analyze your data by:
- **Importing** CSV files and Google Sheets
- **Querying** data with full SQL (JOINs, aggregations, window functions)
- **Analyzing** datasets from 100 rows to billions
- **Exporting** results to CSV

**Simple Example:**

```
You: "Load sales_2024.csv as sales and show me the top 10 products by revenue"

Claude/ChatGPT:
1. Imports your CSV into a DuckDB database
2. Writes SQL: SELECT product, SUM(revenue) FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 10
3. Executes the query
4. Shows results with insights: "Your top product is Widget A with $50K revenue..."
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (or Docker Desktop)
- Claude Desktop or ChatGPT Desktop
- 2GB+ RAM

### Installation

**Option 1: Docker (Recommended)**

```bash
# Clone or download this repo
cd mcp-data-analyst

# Start the container
./docker-start.sh

# Follow the instructions to configure Claude/ChatGPT
```

**Option 2: Direct Python Install**

```bash
# Clone or download this repo
cd mcp-data-analyst

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

## 📋 Configuration

### Step 1: Configure Your AI Assistant

#### For Claude Desktop

Edit the config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**If using Docker:**
```json
{
  "mcpServers": {
    "mcp-data-analyst": {
      "command": "docker",
      "args": ["exec", "-i", "data-analyst-mcp", "python3", "server.py"]
    }
  }
}
```

**If using direct install:**
```json
{
  "mcpServers": {
    "mcp-data-analyst": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp-data-analyst/server.py"]
    }
  }
}
```

#### For ChatGPT Desktop

Edit the config file:
- **macOS**: `~/Library/Application Support/ChatGPT/config.json`
- **Windows**: `%APPDATA%\ChatGPT\config.json`

Use the same JSON format as Claude Desktop above.

### Step 2: Configure Environment (Optional)

For cloud storage with MotherDuck (handles billions of rows):

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your token
nano .env
```

Add your MotherDuck token:
```bash
MOTHERDUCK_TOKEN=your_token_here
MEMORY_LIMIT=4G
CPU_LIMIT=2.0
```

Get a free token at [motherduck.com](https://motherduck.com) (10GB free tier).

**Without MotherDuck:** Data is stored in-memory (fast, but session-only).

### Step 3: Restart Your AI Assistant

Completely quit and restart Claude Desktop or ChatGPT Desktop.

### Step 4: Test It!

```
You: "Load example_data.csv as customers and show me the data"
```

The AI will import the file and show you the results!

## 📊 Features

### 6 Powerful Tools

1. **import_csv** - Load CSV files, Google Sheets, or URLs
2. **query_data** - Execute SQL queries with full DuckDB support
3. **list_tables** - Show all available tables
4. **describe_table** - Get schema and sample data
5. **export_query_results** - Save query results to CSV
6. **get_table_stats** - Get statistical summaries

### Supported Data Sources

- **Local CSV files** - Any CSV on your computer
- **CSV URLs** - Direct HTTP/HTTPS links
- **Google Sheets** - Automatically converts share links to CSV
- **Multiple files** - Load multiple CSVs as separate tables

### SQL Capabilities

Full SQL support including:
- SELECT, WHERE, GROUP BY, ORDER BY, LIMIT
- JOINs (INNER, LEFT, RIGHT, FULL OUTER)
- Aggregate functions (SUM, AVG, COUNT, MIN, MAX)
- Window functions (ROW_NUMBER, RANK, LAG, LEAD)
- CTEs (WITH clauses)
- Subqueries
- Date/time functions

### Data Size Limits

| Rows | CSV Size | Mode | Performance |
|------|----------|------|-------------|
| < 1M | ~100MB | In-memory | ⚡ Instant |
| 1-10M | ~1GB | In-memory | ✅ Fast (seconds) |
| 10M+ | 1GB+ | MotherDuck | ☁️ Optimized (cloud) |

**Recommendation**: Use in-memory for < 10M rows, MotherDuck for larger datasets.

## 💡 Usage Examples

### Example 1: Basic Analysis

```
You: "Load my sales data from https://example.com/sales.csv as sales"
AI: ✓ Imported 50,000 rows into 'sales' table

You: "What are the top 5 products by revenue?"
AI: [Writes and executes SQL, shows results with insights]

You: "Show me monthly revenue trends"
AI: [Creates time-series analysis with DATE_TRUNC]
```

### Example 2: Multi-Table Analysis

```
You: "Load sales.csv as sales and products.csv as products"
AI: ✓ Imported both tables

You: "Join these tables and show me which product categories generate the most revenue"
AI: [Automatically identifies the relationship (product_id), performs JOIN, provides analysis]
```

### Example 3: Advanced Analytics

```
You: "Analyze customer behavior and create segments based on purchase patterns"
AI: [Performs multi-step analysis with CTEs, window functions, and provides business insights]
```

### Example 4: Google Sheets

```
You: "Load this Google Sheet: https://docs.google.com/spreadsheets/d/abc123/edit"
AI: ✓ Converted to CSV and imported

You: "Calculate the correlation between marketing spend and sales"
AI: [Performs statistical analysis]
```

## 🐳 Docker Commands

```bash
# Start server
./docker-start.sh

# Stop server
./docker-stop.sh

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop and remove
docker-compose down

# Rebuild
docker-compose down && docker-compose up -d --build
```

## 🔧 Troubleshooting

### MCP Server Not Appearing

1. Verify config file path is correct
2. Use absolute paths (not `~` or relative)
3. Ensure container is running: `docker ps`
4. Check logs: `docker-compose logs`
5. Restart AI assistant completely (quit, not just close)

### Permission Denied on Scripts

```bash
chmod +x docker-start.sh docker-stop.sh setup.sh
```

### Import Errors

- **Local files**: Use absolute paths
- **Google Sheets**: Share with "Anyone with link"
- **URLs**: Verify URL is publicly accessible

### Out of Memory

For large datasets (> 10M rows):

**Option 1**: Increase Docker memory in `docker-compose.yml`:
```yaml
memory: 8G  # or 16G
cpus: '4.0'
```

**Option 2**: Use MotherDuck (recommended for > 10M rows):
1. Get token from [motherduck.com](https://motherduck.com)
2. Add to `.env`: `MOTHERDUCK_TOKEN=your_token`
3. Restart: `docker-compose restart`

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Claude Desktop / ChatGPT Desktop  │
│   (Natural Language Interface)      │
└─────────────────┬───────────────────┘
                  │ MCP Protocol
                  ▼
┌─────────────────────────────────────┐
│   MCP Data Analyst Server (Python) │
│   - 6 Tools (FastMCP)               │
│   - CSV Import & SQL Query          │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│   DuckDB Database                   │
│   - In-Memory (< 10M rows)          │
│   - MotherDuck Cloud (billions)     │
└─────────────────────────────────────┘
```

## 🔒 Security & Privacy

- **In-memory mode**: All data stays on your computer, never leaves your machine
- **MotherDuck mode**: Data stored in your private cloud account
- **No external sharing**: Your data is never sent to third parties
- **Read-only SQL**: Only SELECT queries, no data modification
- **Container isolation**: Docker provides additional security layer

## 📚 Advanced Configuration

### Custom Memory Limits

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 8G      # Increase for large datasets
      cpus: '4.0'     # More CPU for faster processing
```

### Multiple Tables

Load multiple CSVs:
```
You: "Load sales.csv, products.csv, and customers.csv"
AI: [Imports all three as separate tables]

You: "Show me how these tables relate to each other"
AI: [Analyzes schemas, identifies foreign keys, suggests JOINs]
```

### Export Results

```
You: "Export the top 100 customers to a CSV file"
AI: [Executes query and saves to /data/top_customers.csv]
```

## 🛠️ Development

### Adding Custom Tools

The FastMCP framework makes it easy to add new tools:

```python
@mcp.tool()
def my_custom_tool(param: str, count: int = 10) -> dict:
    """Description that appears to the AI"""
    # Your logic here
    return {"result": "..."}
```

That's it! FastMCP handles validation, errors, and protocol details.

### Project Structure

```
mcp-data-analyst/
├── server.py              # Main MCP server (FastMCP)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Docker orchestration
├── docker-start.sh       # Easy start script
├── docker-stop.sh        # Easy stop script
├── setup.sh              # Direct install script
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── example_data.csv      # Sample data for testing
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🙏 Credits

Built with:
- **FastMCP** - Modern MCP framework
- **DuckDB** - Fast analytical database
- **MotherDuck** - Cloud data warehouse
- **MCP Protocol** by Anthropic

## 📞 Support

- **Issues**: Open a GitHub issue
- **Questions**: Start a discussion
- **Documentation**: Check this README

## 🌟 Star This Repo

If you find this useful, please star the repo! ⭐

---

**Transform your AI assistant into a data analyst in 5 minutes!** 📊✨
