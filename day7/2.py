import asyncio
import time 

async def fetch_data(source: str, delay: int) -> str:
    print(f"starting fetch : {source}")
    await asyncio.sleep(delay)
    print(f"finished fetch : {source}")
    return f"data from {source}"


async def main():
    start = time.time()

    results = await asyncio.gather(
        fetch_data("database", 3),
        fetch_data("cache", 1),
        fetch_data("external api", 2)
    )
    
    end = time.time()
    print("results:", results)
    print(f"async total time : {end - start: .2f} secs")



asyncio.run(main())