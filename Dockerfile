FROM mcr.microsoft.com/azure-cli
WORKDIR /app
COPY azurevm.py .
ENTRYPOINT ["tail", "-f", "/dev/null"]
