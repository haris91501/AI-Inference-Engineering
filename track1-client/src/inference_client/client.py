import asyncio
from pathlib import Path
import json
import time
from typing import Any

import httpx


async def stream_request(
    url: str,
    payload: dict[str, Any],
    timeout_seconds: float = 5.0,
) -> dict[str, Any]:
    request_id = payload.get("request_id", "req-unknown")

    result: dict[str, Any] = {
        "request_id": request_id,
        "chunks": [],
        "first_chunk_seconds": None,
        "final_seconds": None,
        "error_type": None,
        "status_code": None,
    }

    start = time.perf_counter()
    first_chunk_time: float | None = None

    try:
        timeout = httpx.Timeout(timeout_seconds)

        async with httpx.AsyncClient(timeout=timeout) as client:
            async with asyncio.timeout(timeout_seconds):
                async with client.stream(
                    "POST",
                    url,
                    json=payload,
                ) as response:
                    result["status_code"] = response.status_code
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if not line:
                            continue

                        chunk = json.loads(line)

                        if first_chunk_time is None:
                            first_chunk_time = time.perf_counter()
                            result["first_chunk_seconds"] = (
                                first_chunk_time - start
                            )

                        result["chunks"].append(chunk)

    except httpx.HTTPStatusError as exc:
        result["error_type"] = "HTTPStatusError"
        result["status_code"] = exc.response.status_code

    except (httpx.TimeoutException, TimeoutError):
        result["error_type"] = "TimeoutError"

    except asyncio.CancelledError:
        result["error_type"] = "CancelledError"
        raise

    except (
        httpx.HTTPError,
        json.JSONDecodeError,
        ValueError,
    ) as exc:
        result["error_type"] = type(exc).__name__

    finally:
        result["final_seconds"] = time.perf_counter() - start
        save_result(result)

    return result


def save_result(
    result: dict[str, Any],
    log_path: str = "logs/day04.jsonl",
) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(
            json.dumps(result, ensure_ascii=False) + "\n"
        )
