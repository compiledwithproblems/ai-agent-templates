# message-brokers/redis/scripts/healthcheck.sh
#!/bin/sh
redis-cli -h localhost -p 6379 ping || exit 1