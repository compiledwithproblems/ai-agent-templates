# AI Agent Web Server Template

A FastAPI-based web server template for AI agent projects with Redis integration for asynchronous processing.

## Features

- FastAPI web server with async support
- Redis integration for message queue
- Request/Response middleware for logging and request tracking
- Prometheus metrics integration
- Health check endpoints
- CORS support
- Environment-based configuration
- Docker support

## Project Structure

```
web-server/
├── app/
│   ├── config.py           # Configuration settings
│   ├── main.py            # FastAPI application entry point
│   ├── models/            # Pydantic models
│   ├── middleware/        # Custom middleware
│   ├── routes/           # API endpoints
│   └── services/         # Business logic
├── tests/                # Test files
├── docker/              # Docker configuration
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- API documentation: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/api/v1/openapi.json
- Health check: http://localhost:8000/api/v1/health
- Metrics: http://localhost:8000/metrics

## Docker Support

Build and run with Docker:
```bash
docker-compose up --build
``` 