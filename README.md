# ML Inference Service

TF-IDF based game recommendation microservice.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1` | Service info |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/recommend` | Get game recommendations |

## Usage

```bash
# Info service
curl http://localhost:5001/api/v1

# Health check
curl http://localhost:5001/api/v1/health

# Rekomendasi game
curl -X POST http://localhost:5001/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "game santai buat dimainkan bareng teman", "top_n": 3}'
```

## Run

```bash
./run-dev.sh    # development
./run.sh        # production (gunicorn)
```
