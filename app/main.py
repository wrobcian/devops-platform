from flask import Flask, jsonify, request
import datetime
import socket
import os
import platform
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

metrics = {
    "total_requests": 0,
    "endpoints": {},
    "errors": 0,
    "start_time": datetime.datetime.now().isoformat()
}

def track_request(endpoint):
    """Śledź metryki requestów"""
    metrics["total_requests"] += 1
    if endpoint not in metrics["endpoints"]:
        metrics["endpoints"][endpoint] = 0
    metrics["endpoints"][endpoint] += 1



@app.route('/')
def home():
    track_request("/")
    logger.info("Home page accessed")
    return jsonify({
        "app": "DevOps Platform",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now().isoformat(),
        "endpoints": [
            "GET /         - This page",
            "GET /health   - Health check",
            "GET /info     - System info",
            "GET /metrics  - App metrics",
            "GET /api/status - Service status",
            "POST /api/log  - Log a message"
        ]
    })


@app.route('/health')
def health():
    track_request("/health")
    health_status = {
        "status": "healthy",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "uptime_since": metrics["start_time"],
        "checks": {
            "app": "passing",
            "memory": "passing",
            "disk": "passing"
        }
    }
    logger.info("Health check: OK")
    return jsonify(health_status), 200


@app.route('/info')
def info():
    track_request("/info")
    return jsonify({
        "application": {
            "name": "DevOps Platform",
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "author": "DevOps Learner"
        },
        "tech_stack": {
            "language": f"Python {platform.python_version()}",
            "framework": "Flask",
            "containerization": "Docker",
            "orchestration": "Kubernetes",
            "ci_cd": "GitHub Actions",
            "iac": "Terraform",
            "cloud": "AWS"
        },
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "python": platform.python_version()
        }
    })


@app.route('/metrics')
def get_metrics():
    track_request("/metrics")
    uptime = datetime.datetime.now() - datetime.datetime.fromisoformat(metrics["start_time"])
    return jsonify({
        "total_requests": metrics["total_requests"],
        "endpoints": metrics["endpoints"],
        "errors": metrics["errors"],
        "uptime_seconds": int(uptime.total_seconds()),
        "start_time": metrics["start_time"]
    })


@app.route('/api/status')
def api_status():
    track_request("/api/status")
    
    db_host = os.getenv("DATABASE_HOST", "not configured")
    redis_host = os.getenv("REDIS_HOST", "not configured")
    
    return jsonify({
        "services": {
            "web_app": {
                "status": "running",
                "port": os.getenv("PORT", "5000")
            },
            "database": {
                "status": "configured" if db_host != "not configured" else "not configured",
                "host": db_host
            },
            "cache": {
                "status": "configured" if redis_host != "not configured" else "not configured",
                "host": redis_host
            }
        },
        "environment_variables": {
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "not set"),
            "APP_VERSION": os.getenv("APP_VERSION", "not set"),
            "PORT": os.getenv("PORT", "not set"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "not set")
        }
    })


@app.route('/api/log', methods=['POST'])
def log_message():
    track_request("/api/log")
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            metrics["errors"] += 1
            return jsonify({"error": "Missing 'message' field"}), 400
        
        level = data.get('level', 'INFO').upper()
        message = data['message']
        
        if level == "ERROR":
            logger.error(f"User log: {message}")
        elif level == "WARNING":
            logger.warning(f"User log: {message}")
        else:
            logger.info(f"User log: {message}")
        
        return jsonify({
            "status": "logged",
            "level": level,
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        metrics["errors"] += 1
        logger.error(f"Error processing log: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    metrics["errors"] += 1
    return jsonify({
        "error": "Not Found",
        "message": "Endpoint does not exist. Visit / for available endpoints."
    }), 404


@app.errorhandler(500)
def server_error(error):
    metrics["errors"] += 1
    return jsonify({
        "error": "Internal Server Error"
    }), 500


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("ENVIRONMENT") == "development"
    
    logger.info(f"Starting DevOps Platform v{os.getenv('APP_VERSION', '1.0.0')}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)