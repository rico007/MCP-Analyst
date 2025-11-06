FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY server.py .
COPY example_data.csv .

# Create a volume mount point for user data
VOLUME ["/data"]

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MOTHERDUCK_TOKEN=""

# Make server.py executable
RUN chmod +x server.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Run the MCP server
CMD ["python3", "server.py"]
