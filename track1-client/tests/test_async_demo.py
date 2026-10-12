import asyncio
import time

import pytest

from src.inference_client.async_demo import (
    cancellation_demo,
    fake_inference,
    run_concurrent_requests,
    run_with_timeout,
)


def test_requests_run_concurrently():
    async def scenario():
        start = time.perf_counter()

        results = await run_concurrent_requests()

        elapsed = time.perf_counter() - start

        assert len(results) == 3
        assert results == [
            "Response from request 1",
            "Response from request 2",
            "Response from request 3",
        ]

        # Sequential execution would take about 0.6 seconds.
        # Concurrent execution should take about 0.3 seconds.
        assert elapsed < 0.5

    asyncio.run(scenario())


def test_timeout_raises_timeout_error():
    async def scenario():
        with pytest.raises(TimeoutError):
            await run_with_timeout(timeout=0.2)

    asyncio.run(scenario())


def test_cancellation_runs_cleanup(capsys):
    async def scenario():
        result = await cancellation_demo()
        assert result is True

    asyncio.run(scenario())

    output = capsys.readouterr().out

    assert "Request 4: cleanup executed" in output


def test_negative_duration_is_rejected():
    async def scenario():
        with pytest.raises(ValueError):
            await fake_inference(5, -1)

    asyncio.run(scenario())