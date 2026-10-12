import asyncio


async def fake_inference(
    request_id: int,
    duration: float,
) -> str:
    """Simulate an inference request."""

    if duration < 0:
        raise ValueError("duration must not be negative")

    print(f"Request {request_id}: started")

    try:
        await asyncio.sleep(duration)
        print(f"Request {request_id}: completed")
        return f"Response from request {request_id}"

    finally:
        print(f"Request {request_id}: cleanup executed")


async def run_concurrent_requests() -> list[str]:
    """Run three inference requests concurrently."""

    tasks = [
        asyncio.create_task(fake_inference(1, 0.2)),
        asyncio.create_task(fake_inference(2, 0.1)),
        asyncio.create_task(fake_inference(3, 0.3)),
    ]

    try:
        return await asyncio.gather(*tasks)

    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)


async def run_with_timeout(timeout: float = 0.2) -> list[str]:
    """Run requests with an overall deadline."""

    tasks = [
        asyncio.create_task(fake_inference(1, 0.1)),
        asyncio.create_task(fake_inference(2, 0.1)),
        asyncio.create_task(fake_inference(3, 1.0)),
    ]

    try:
        return await asyncio.wait_for(
            asyncio.gather(*tasks),
            timeout=timeout,
        )

    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)


async def cancellation_demo() -> bool:
    """Cancel a task and verify its final state."""

    task = asyncio.create_task(fake_inference(4, 10.0))

    try:
        await asyncio.sleep(0.05)
        task.cancel()

        try:
            await task

        except asyncio.CancelledError:
            pass

        return task.done() and task.cancelled()

    finally:
        if not task.done():
            task.cancel()

        await asyncio.gather(task, return_exceptions=True)


if __name__ == "__main__":
    async def main() -> None:
        results = await run_concurrent_requests()
        print("Results:", results)

    asyncio.run(main())