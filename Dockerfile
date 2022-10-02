FROM ubuntu:20.04
RUN apt update && apt install curl -y
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
WORKDIR /app
COPY auto-start.py .
ENTRYPOINT ["tail", "-f", "/dev/null"]
