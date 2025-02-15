FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

#Declaring the working directory
WORKDIR /app

#Copying the Local file
COPY app.py /app/app.py
COPY tool_call_function.py /app/
COPY service.py /app/

#Declaring the command to run the application
CMD [ "uv","run","app.py" ]