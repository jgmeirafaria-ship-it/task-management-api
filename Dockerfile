# ---------- Fase 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

# ---------- Fase 2: imagem final (distroless) ----------
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

COPY --from=builder /install /usr/lib/python3.11/site-packages
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

ENV PYTHONPATH=/usr/lib/python3.11/site-packages

EXPOSE 8000

ENTRYPOINT ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]