FROM vault:1.10.4

COPY config.hcl /vault/config/config.hcl

ENV VAULT_ADDR=http://127.0.0.1:8200
ENV VAULT_DEV_ROOT_TOKEN_ID=root

EXPOSE 8200

CMD ["vault", "server", "-config=/vault/config/config.hcl"]


