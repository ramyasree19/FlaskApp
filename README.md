# FlaskApp

A small Flask application that uses Redis. This README explains how to run the app locally (with and without Docker), how to use environment files, and how to use docker-compose to run the application.

## Table of contents
- [Prerequisites](#prerequisites)
- [Project structure](#project-structure)
- [Environment variables](#environment-variables)
- [Install dependencies](#install-dependencies)
- [Run locally (without Docker)](#run-locally-without-docker)
- [Run with Docker](#run-with-docker)
- [Run with docker-compose (recommended)](#run-with-docker-compose-recommended)
  - [Optional: Add an Nginx reverse proxy (myapp.local)](#optional-add-an-nginx-reverse-proxy-myapplocal)
- [Troubleshooting](#troubleshooting)
- [Next steps / Recommendations](#next-steps--recommendations)
- [Contributing](#contributing)
- [License](#license)

---

## Prerequisites
- Python 3.8+
- pip
- (Optional) Redis server if running without Docker
- Docker & Docker Compose (if you plan to run in containers)

---

## Project structure
(Adjust to match your repo)
- `app.py` (or package folder containing the Flask app)
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `.env.example` (recommended)

---

## Environment variables
Create a `.env` file at the project root (do not commit secrets). Copy from a template if available:

```env
FLASK_ENV=development
FLASK_DEBUG=1
PORT=8000
REDIS_HOST=redis        # or host.docker.internal for local Docker on mac/windows
REDIS_PORT=6379
```

Suggested files:
- `.env.example` — tracked template with example values
- `.env` — local overrides (ignored by git)

---

## Install dependencies

Create a virtual environment and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Note: The correct pip install command is `pip install -r requirements.txt` (not `python3 -m pip install requirements.txt`).

---

## Run locally (without Docker)

1. Start Redis locally (one option):

- macOS (Homebrew):
```bash
brew install redis
brew services start redis
```

- Or run Redis in Docker:
```bash
docker run -d --name local-redis -p 6379:6379 redis:7
```

2. Start the Flask app:

If your entrypoint is `app.py`:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=${PORT:-8000}
# or
python app.py
```

The app will be reachable at http://localhost:8000 (or the port you set).

---

## Run with Docker

Build an image and run (simple single-container example):

```bash
# Build image
docker build -t flaskapp:v1 .

# Run (if connecting to local Redis, use host.docker.internal on mac/windows)
docker run -p 3000:8000 --name flaskapp \
  -e REDIS_HOST=host.docker.internal \
  -e REDIS_PORT=6379 \
  flaskapp:v1
```

- Browser port: 3000 (mapped to container port 8000)
- Container port: 8000

Note: `host.docker.internal` works on Docker Desktop for macOS/Windows. Linux may need a different approach (see docker-compose instructions below).

---

## Run with docker-compose (recommended)

Create a `docker-compose.yml` that runs the app and a Redis service together. Example:

```yaml
version: "3.8"
services:
  app:
    build: .
    env_file:
      - .env
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "3000:8000"
    depends_on:
      - redis

  redis:
    image: redis:7
    restart: unless-stopped
    ports:
      - "6379:6379"   # optional; exposes Redis to host
```

Commands:

```bash
# Start services in background
docker compose up -d

# Stop app only
docker compose stop app

# Start app only
docker compose start app

# Stop and remove all containers created by compose
docker compose down

# To check config of multiple services
docker compose config
```

With this compose file, the app can use `redis` (the service name) as the Redis hostname.

### Optional: Add an Nginx reverse proxy (myapp.local)
If you want a lightweight reverse proxy in front of the Flask container and a friendly local hostname (for example `myapp.local`), add an `nginx` service to your `docker-compose.yml` and a small nginx config.

Example `docker-compose.yml` fragment (extended):

```yaml
services:
  # ... app and redis from above ...

  nginx:
    image: nginx:1.25
    depends_on:
      - app
    ports:
      - "80:80"
    volumes:
      - ./deploy/nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

Example `deploy/nginx/nginx.conf` (simple proxy to the `app` service):

```nginx
server {
    listen 80;
    server_name myapp.local;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

To use `myapp.local` on your development machine, add a hosts entry:

```bash
sudo nano /etc/hosts
```

Add the following line to the file:

```
127.0.0.1   myapp.local
```

Now `http://myapp.local` in your browser will reach the nginx container which proxies to the Flask app.

---

## Troubleshooting

- Connection refused for Redis inside container:
  - If you ran the app container separately and attempted to connect to a host Redis server, the container may not reach `localhost:6379`. Use:
    - `REDIS_HOST=host.docker.internal` on Docker Desktop (macOS/Windows)
    - Or run Redis as a separate container and use docker-compose so the app can use the `redis` service hostname.
  - Check the Redis container is running: `docker ps` and `docker logs <redis-container>`.
  - From inside the app container, test connectivity with: `apt-get update && apt-get install -y redis-tools` (or use a debug image) then `redis-cli -h redis ping`.

- Make sure `requirements.txt` is present and correct.

- If using Linux and `host.docker.internal` is not available, either run Redis as a container or create a user-defined network and run both containers there.

---

## Next steps / Recommendations
- Add a `.env.example` file to the repo with example variables.
- Add a `docker-compose.yml` (example above) to the repo.
- Add a small healthcheck for the app (optional) and a readiness check for Redis in compose.
- Add CI checks and a brief `CONTRIBUTING.md` if others will collaborate.
- Commit the `deploy/nginx/nginx.conf` (or similar) and the `docker-compose.yml` if you use the nginx setup.

---

## Contributing
Contributions welcome. Please open an issue or PR with changes. Include how to run and test.

---

## License
Add appropriate license information here.

---

<img width="459" height="296" alt="image" src="https://github.com/user-attachments/assets/f82d625b-e4e4-43fd-8168-68bc25043bc8" />