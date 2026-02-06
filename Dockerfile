FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libffi-dev \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libxml2 \
    libxslt1.1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY app.py .
COPY config.py .
COPY utils.py .
COPY templates/ templates/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data/input /app/data/output && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Create data directories
RUN mkdir -p /app/data/input /app/data/output

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:5000/ || exit 1

# Run application
CMD ["python", "app.py"]
