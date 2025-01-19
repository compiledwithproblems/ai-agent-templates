FROM redis:6.2-alpine

# Add Redis configuration
COPY config/redis.conf /usr/local/etc/redis/redis.conf

# Add custom scripts if needed
COPY scripts/healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh

# Create necessary directories with correct permissions
RUN mkdir -p /var/log/redis \
    && chown redis:redis /var/log/redis \
    && chmod 777 /var/log/redis

HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
    CMD redis-cli ping || exit 1

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
