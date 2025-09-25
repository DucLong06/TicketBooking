# Dockerfile for Jenkins with Docker and Helm
FROM jenkins/jenkins:lts-jdk17

USER root

# Install Docker
RUN curl https://get.docker.com > dockerinstall && \
    chmod 777 dockerinstall && \
    ./dockerinstall && \
    rm dockerinstall

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install additional tools for CI/CD
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jenkins user
USER jenkins

