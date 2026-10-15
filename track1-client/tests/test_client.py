import asyncio

import pytest

from inference_client.client import stream_request


@pytest.mark.asyncio
async def test_stream_request_returns_chunks():
    result = await stream_request(
        "http://127.0.0.1:8765/stream",
        {"request_id": "req-test-001"},
    )

    assert result["error_type"] is None
    assert result["request_id"] == "req-test-001"
    assert len(result["chunks"]) == 4
    assert result["first_chunk_seconds"] is not None
    assert result["final_seconds"] is not None


@pytest.mark.asyncio
async def test_stream_request_handles_http_error():
    result = await stream_request(
        "http://127.0.0.1:8765/stream",
        {
            "request_id": "req-test-002",
            "status_code": 500,
        },
    )

    assert result["error_type"] == "HTTPStatusError"
    assert result["status_code"] == 500


@pytest.mark.asyncio
async def test_stream_request_handles_timeout():
    result = await stream_request(
        "http://127.0.0.1:8765/stream",
        {
            "request_id": "req-test-003",
            "delay_seconds": 2,
        },
        timeout_seconds=0.2,
    )

    assert result["error_type"] == "TimeoutError"


@pytest.mark.asyncio
async def test_stream_request_propagates_cancellation():
    task = asyncio.create_task(
        stream_request(
            "http://127.0.0.1:8765/stream",
            {
                "request_id": "req-test-004",
                "delay_seconds": 1,
            },
            timeout_seconds=10,
        )
    )

    await asyncio.sleep(0.1)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task