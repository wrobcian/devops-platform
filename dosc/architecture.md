# Architecture Documentation

## System Overview

                ┌─────────────┐
                │   Nginx     │ :80
                │   (Proxy)   │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │  Flask App  │ :5000
                │  (Python)   │
                └──┬──────┬───┘
                   │      │
          ┌────────▼┐  ┌──▼────────┐
          │PostgreSQL│  │   Redis   │
          │  (DB)    │  │  (Cache)  │
          └──────────┘  └───────────┘

          
## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Application | Python/Flask | REST API |
| Proxy | Nginx | Reverse proxy, load balancing |
| Database | PostgreSQL | Data storage |
| Cache | Redis | Session/data caching |
| Container | Docker | Containerization |
| Orchestration | Kubernetes | Container orchestration |
| CI/CD | GitHub Actions | Automated pipeline |
| IaC | Terraform | AWS infrastructure |
| Monitoring | Prometheus + Grafana | Metrics and dashboards |

## CI/CD Pipeline

Push to GitHub
│
├── Lint (code quality)
│
├── Test (pytest)
│
├── Docker Build + Health Check
│
├── Terraform Validate
│
└── Kubernetes Validate


## Infrastructure (AWS)

- VPC with public subnet
- EC2 instance (t2.micro)
- S3 bucket for artifacts
- Security groups for HTTP/HTTPS/SSH