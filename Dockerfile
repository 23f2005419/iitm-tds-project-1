# Stage 1: Python application
FROM python:3.12-slim-bookworm as python-app

# Install curl and certificates
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Download and run the installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Create the /data directory
RUN mkdir -p /data

# Declaring the working directory
WORKDIR /app

# Copying the local files
COPY app.py /app/app.py
COPY tool_call_function.py /app/
COPY service.py /app/

# Stage 2: Node.js environment to get npx
FROM node:latest as node-env

# Install npm and npx
RUN apt-get update && apt-get install -y curl \
  && curl -L https://www.npmjs.com/install.sh | sh \
  && npm install -g --force npx

# Copy npx from Node.js environment to Python environment
FROM python-app
COPY --from=node-env /usr/local/bin/npx /usr/local/bin/npx

# Ensure the installed binary is on the PATH
ENV PATH="/root/.local/bin/:$PATH"

# Check the contents of the /app directory (for debugging purposes)
RUN ls -la /app

# Declaring the command to run the application
CMD ["uv", "run", "app.py"]
