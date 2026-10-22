import asyncio
import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn

app = FastAPI(title="Fake Inference Stream Server")

MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "/app/cache")


@app.get("/health")
async def health_check():
    """Health check endpoint: verifies service is alive, cache is accessible, and reports GPU state."""
    cache_exists = os.path.exists(MODEL_CACHE_DIR) and os.path.isdir(MODEL_CACHE_DIR)
    
    # Check GPU availability gracefully
    gpu_available = False
    gpu_device_name = "None"
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        if gpu_available:
            gpu_device_name = torch.cuda.get_device_name(0)
    except ImportError:
        pass

    return {
        "status": "healthy",
        "cache_mounted": cache_exists,
        "cache_dir": MODEL_CACHE_DIR,
        "gpu_available": gpu_available,
        "gpu_device": gpu_device_name,
    }


@app.post("/stream")
async def stream_response(request: Request):
    payload = await request.json()

    request_id = payload.get("request_id", "req-unknown")
    delay = float(payload.get("delay_seconds", 0))
    status_code = int(payload.get("status_code", 200))

    if status_code != 200:
        return JSONResponse(
            status_code=status_code,
            content={
                "request_id": request_id,
                "error": "simulated_http_error",
            },
        )

    async def generate():
        chunks = [
            {"request_id": request_id, "chunk": "Hello"},
            {"request_id": request_id, "chunk": " from"},
            {"request_id": request_id, "chunk": " the"},
            {"request_id": request_id, "chunk": " server"},
        ]

        for chunk in chunks:
            if delay > 0:
                await asyncio.sleep(delay)
            yield json.dumps(chunk) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8765,
    )
