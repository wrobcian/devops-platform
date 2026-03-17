#!/bin/bash

APP_URL=${1:-"http://localhost:8080"}

echo "======================================"
echo "HEALTH CHECK: $APP_URL"
echo "Date: $(date)"
echo "======================================"

endpoints=(
    "/"
    "/health"
    "/info"
    "/metrics"
    "/api/status"
)

PASS=0
FAIL=0

for endpoint in "${endpoints[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL$endpoint" 2>/dev/null)
    
    if [ "$STATUS" = "200" ] || [ "$STATUS" = "201" ]; then
        echo "  OK   $endpoint ($STATUS)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL $endpoint ($STATUS)"
        FAIL=$((FAIL + 1))
    fi
done

echo ""
echo "======================================"
echo "Results: $PASS passed, $FAIL failed"
echo "======================================"

if [ $FAIL -gt 0 ]; then
    exit 1
fi