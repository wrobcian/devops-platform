# DevOps Platform

Full DevOps project demonstrating containerization, CI/CD, Infrastructure as Code, and monitoring.

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python/Flask | Application |
| Docker/Compose | Containerization |
| GitHub Actions | CI/CD Pipeline |
| Terraform | Infrastructure as Code (AWS) |
| Kubernetes | Container Orchestration |
| Nginx | Reverse Proxy |
| PostgreSQL | Database |
| Redis | Cache |
| Prometheus/Grafana | Monitoring |

## Quick Start

```bash
git clone https://github.com/TWOJ_USER/devops-platform.git
cd devops-platform

docker build -t devops-platform -f docker/Dockerfile .
docker run -d -p 8080:5000 devops-platform

cd docker && docker compose up -d