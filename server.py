#!/usr/bin/env python3
"""
Data Analyst MCP Server with MotherDuck Integration (FastMCP Version)
Allows Claude to import CSV/Google Sheets and perform SQL analysis
"""

import os
from typing import Optional
import duckdb
import pandas as pd
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("data-analyst-mcp")

# Global connection to MotherDuck
MOTHERDUCK_TOKEN = os.getenv("MOTHERDUCK_TOKEN", "")
db_connection = None


def get_connection():
    """Get or create MotherDuck connection"""
    global db_connection
    if db_connection is None:
        if MOTHERDUCK_TOKEN:
            db_connection = duckdb.connect(f'md:?motherduck_token={MOTHERDUCK_TOKEN}')
        else:
            db_connection = duckdb.connect(':memory:')
    return db_connection


def convert_google_sheet_url(url: str) -> str:
    """Convert Google Sheets URL to CSV export URL"""
    if '/edit' in url or '/view' in url:
        sheet_id = url.split('/d/')[1].split('/')[0]
        return f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'
    return url


@mcp.tool()
def import_csv(source: str, table_name: str) -> dict:
    """Import data from a CSV file URL or local path into a database table.
    
    Supports:
    - Direct CSV URLs (http/https)
    - Google Sheets URLs (automatically converted to CSV export)
    - Local file paths
    
    Args:
        source: CSV file URL, Google Sheets URL, or local file path
        table_name: Name for the database table (will be created/replaced)
    
    Returns:
        Dictionary with success status, message, and table info
    """
    conn = get_connection()
    
    # Convert Google Sheets URL if needed
    if "docs.google.com/spreadsheets" in source:
        source = convert_google_sheet_url(source)
    
    # Load data using pandas
    if source.startswith("http://") or source.startswith("https://"):
        df = pd.read_csv(source)
    else:
        df = pd.read_csv(source)
    
    # Create table in DuckDB
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    
    return {
        "success": True,
        "message": f"Successfully imported {len(df)} rows into table '{table_name}'",
        "table_name": table_name,
        "row_count": len(df),
        "columns": list(df.columns)
    }


@mcp.tool()
def query_data(query: str, limit: int = 100) -> dict:
    """Execute a SQL query on the loaded data for analysis.
    
    You can use standard SQL including:
    - SELECT, WHERE, GROUP BY, ORDER BY
    - JOINs across multiple tables
    - Aggregate functions (SUM, AVG, COUNT, etc.)
    - Window functions
    - CTEs (WITH clauses)
    
    Args:
        query: SQL query to execute
        limit: Maximum number of rows to return (default: 100)
    
    Returns:
        Dictionary with query results, columns, and row count
    """
    conn = get_connection()
    
    # Add LIMIT if not present
    if "LIMIT" not in query.upper():
        query = f"{query} LIMIT {limit}"
    
    # Execute query
    result_df = conn.execute(query).fetchdf()
    
    return {
        "success": True,
        "row_count": len(result_df),
        "columns": list(result_df.columns),
        "data": result_df.to_dict(orient='records')
    }


@mcp.tool()
def list_tables() -> dict:
    """List all available tables in the database with row counts and basic info.
    
    Returns:
        Dictionary with list of tables and their row counts
    """
    conn = get_connection()
    tables_df = conn.execute("SHOW TABLES").fetchdf()
    
    tables_info = []
    for _, row in tables_df.iterrows():
        table_name = row['name']
        count = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}").fetchone()[0]
        tables_info.append({
            "table_name": table_name,
            "row_count": count
        })
    
    return {
        "success": True,
        "table_count": len(tables_info),
        "tables": tables_info
    }


@mcp.tool()
def describe_table(table_name: str) -> dict:
    """Get detailed schema information about a specific table including column names, 
    types, and sample data.
    
    Args:
        table_name: Name of the table to describe
    
    Returns:
        Dictionary with schema, sample data, and row count
    """
    conn = get_connection()
    
    # Get schema
    schema_df = conn.execute(f"DESCRIBE {table_name}").fetchdf()
    
    # Get sample data
    sample_df = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
    
    # Get row count
    row_count = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}").fetchone()[0]
    
    return {
        "success": True,
        "table_name": table_name,
        "row_count": row_count,
        "schema": schema_df.to_dict(orient='records'),
        "sample_data": sample_df.to_dict(orient='records')
    }


@mcp.tool()
def export_query_results(query: str, output_path: str) -> dict:
    """Export query results to a CSV file.
    
    Args:
        query: SQL query to execute
        output_path: Path where to save the CSV file
    
    Returns:
        Dictionary with export status and file info
    """
    conn = get_connection()
    
    # Execute query and save to CSV
    result_df = conn.execute(query).fetchdf()
    result_df.to_csv(output_path, index=False)
    
    return {
        "success": True,
        "message": f"Exported {len(result_df)} rows to {output_path}",
        "row_count": len(result_df),
        "output_path": output_path
    }


@mcp.tool()
def get_table_stats(table_name: str) -> dict:
    """Get statistical summary of a table including column statistics, 
    null counts, and value distributions.
    
    Args:
        table_name: Name of the table to analyze
    
    Returns:
        Dictionary with statistical summaries
    """
    conn = get_connection()
    
    # Get basic stats using DuckDB's SUMMARIZE
    stats_df = conn.execute(f"SUMMARIZE {table_name}").fetchdf()
    
    return {
        "success": True,
        "table_name": table_name,
        "statistics": stats_df.to_dict(orient='records')
    }


# Resources for listing tables as resources
@mcp.resource("table://{table_name}")
def get_table_resource(table_name: str) -> str:
    """Get a table as a resource with schema and sample data.
    
    Args:
        table_name: Name of the table
    
    Returns:
        JSON string with table information
    """
    import json
    conn = get_connection()
    
    # Get table schema
    schema_df = conn.execute(f"DESCRIBE {table_name}").fetchdf()
    
    # Get sample data (first 10 rows)
    sample_df = conn.execute(f"SELECT * FROM {table_name} LIMIT 10").fetchdf()
    
    result = {
        "table_name": table_name,
        "schema": schema_df.to_dict(orient='records'),
        "sample_data": sample_df.to_dict(orient='records'),
        "row_count": conn.execute(f"SELECT COUNT(*) as count FROM {table_name}").fetchone()[0]
    }
    
    return json.dumps(result, indent=2, default=str)


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()
