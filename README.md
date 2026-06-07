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
curl http://178.128.220.121:5001/api/v1/health

# Rekomendasi game
curl -X POST http://178.128.220.121:5001/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "game santai buat dimainkan bareng teman", "top_n": 3}'
```

## Run (Local)

```bash
./run-dev.sh    # development
./run.sh        # production (gunicorn)
```

## Run (Docker Compose)

### Prerequisites

- Docker & Docker Compose terinstal

```
chmod +x setup-docker.sh

./setup-docker.sh

```

- File `.env` sudah dibuat (salin dari `.env.example`):

```bash
cp .env.example .env
```

### Build & Start

```bash
# Build image dan jalankan service
docker compose up -d --build
```

### Perintah Lainnya

```bash
# Lihat log
docker compose logs -f ml-inference

# Stop service
docker compose down

# Restart service
docker compose restart ml-inference

# Rebuild setelah perubahan kode
docker compose up -d --build
```

### Verifikasi

```bash
# Info service
curl http://localhost:5001/api/v1

# Health check
curl http://localhost:5001/api/v1/health
```
