# AI Code Trust Validator - Docker Image
# Multi-stage build for minimal image size

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install
COPY pyproject.toml .
COPY ai_trust_validator ./ai_trust_validator
RUN pip install --no-cache-dir .

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create non-root user
RUN useradd -m -u 1000 validator
USER validator

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default port
EXPOSE 8080

# Labels
LABEL org.opencontainers.image.title="AI Code Trust Validator"
LABEL org.opencontainers.image.description="Validate AI-generated code for security, hallucinations & logic errors"
LABEL org.opencontainers.image.url="https://github.com/rudra496/ai-code-trust-validator"
LABEL org.opencontainers.image.author="Rudra Sarker"

# Entry point
ENTRYPOINT ["aitrust"]
CMD ["--help"]
