FROM mcr.microsoft.com/azure-cli
WORKDIR /app
COPY auto-start.py .
ENTRYPOINT ["tail", "-f", "/dev/null"]
