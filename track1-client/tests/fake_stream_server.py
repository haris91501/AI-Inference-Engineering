import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn


app = FastAPI()


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

        for index, chunk in enumerate(chunks):
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
        host="127.0.0.1",
        port=8765,
    )