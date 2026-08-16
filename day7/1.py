import asyncio
import time

async def make_call(name: str, delay: int):
    print(f"Starting call: {name}")
    await asyncio.sleep(delay)  # simulates a slow network call
    print(f"Finished call: {name}")
    return f"Result from {name}"


async def main():
    start = time.time()

    # Run all 3 "calls" concurrently, not one after another
    results = await asyncio.gather(
        make_call("Weather API", 3),
        make_call("Stock API", 2),
        make_call("News API", 1)
    )

    end = time.time()
    print("All results:", results)
    print(f"Total time: {end - start:.2f} seconds")


asyncio.run(main())