# Image for a NYU Lab development environment
#FROM rofrano/nyu-devops-base:fa23
FROM rofrano/pipeline-selenium:latest

# Set up the Python development environment
WORKDIR /app
COPY requirements.txt .
RUN sudo pip install -r requirements.txt && sudo pip install psycopg2

# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp && bash ./install-tools.sh
