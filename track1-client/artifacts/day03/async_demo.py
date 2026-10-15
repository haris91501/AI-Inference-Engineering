import asyncio


async def fake_inference(
    request_id: int,
    duration: float,
) -> str:
    """Simulate an inference request that takes some time."""

    print(f"Request {request_id}: started")

    try:
        await asyncio.sleep(duration)
        print(f"Request {request_id}: completed")
        return f"Response from request {request_id}"

    finally:
        print(f"Request {request_id}: cleanup executed")


async def run_demo() -> None:
    """Run three inference requests concurrently."""

    tasks = [
        asyncio.create_task(fake_inference(1, 2.0)),
        asyncio.create_task(fake_inference(2, 1.0)),
        asyncio.create_task(fake_inference(3, 5.0)),
    ]

    try:
        results = await asyncio.gather(*tasks)
        print("Results:", results)

    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(run_demo())