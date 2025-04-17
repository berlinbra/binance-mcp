FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .
RUN pip install uvicorn

# Copy source code
COPY src/ src/

# Set environment variables
ENV PYTHONPATH="/app"

# Run the server
CMD ["python", "-m", "binance_mcp.server"]