FROM debian:bullseye-slim

WORKDIR /app

COPY wisecow/wisecow.sh .

RUN chmod +x wisecow.sh \
    && apt-get update \
    && apt-get install -y fortune-mod cowsay netcat \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/games:${PATH}"

EXPOSE 4499

CMD ["./wisecow.sh"]
