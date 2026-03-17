#!/bin/bash
set -e

APP_NAME="devops-platform"
VERSION=${1:-"latest"}

echo "======================================"
echo "DEPLOYING $APP_NAME v$VERSION"
echo "Date: $(date)"
echo "======================================"

echo ""
echo "[1/5] Building Docker image..."
docker build -t $APP_NAME:$VERSION -f docker/Dockerfile .

echo ""
echo "[2/5] Stopping old container..."
docker stop $APP_NAME 2>/dev/null || true
docker rm $APP_NAME 2>/dev/null || true

echo ""
echo "[3/5] Starting new container..."
docker run -d \
    --name $APP_NAME \
    -p 8080:5000 \
    -e ENVIRONMENT=production \
    -e APP_VERSION=$VERSION \
    --restart unless-stopped \
    $APP_NAME:$VERSION

echo ""
echo "[4/5] Waiting for health check..."
sleep 5

echo ""
echo "[5/5] Verifying deployment..."
HEALTH=$(curl -s http://localhost:8080/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])" 2>/dev/null)

if [ "$HEALTH" = "healthy" ]; then
    echo ""
    echo "======================================"
    echo "DEPLOYMENT SUCCESSFUL!"
    echo "App: http://localhost:8080"
    echo "Health: http://localhost:8080/health"
    echo "======================================"
else
    echo ""
    echo "======================================"
    echo "DEPLOYMENT FAILED! Rolling back..."
    echo "======================================"
    docker stop $APP_NAME
    docker rm $APP_NAME
    exit 1
fi