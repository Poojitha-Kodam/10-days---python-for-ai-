# import asyncio 
# import time 

# async def fetch_data(source:str, delay:int)->str:
#     print(f"start task : {source}")
#     await asyncio.sleep(delay)
#     print(f"end task : {source}")
#     return f"return task : {source}"


# async def main():
#     start = time.time()
#     results = asyncio.gather(
#         fetch_data("data", 3),
#         fetch_data("data1", 4),
#         fetch_data("data2", 5)
#     )
#     end = time.time()

#     print("results : ",  results)
#     print(f"async total time : {end - start: .2f} secs")


# asyncio.run(main())


import time

def fetch_data_sync(source: str, delay: int) -> str:
    print(f"Starting fetch: {source}")
    time.sleep(delay)
    print(f"Finished fetch: {source}")
    return f"Data from {source}"


def main_sync():
    start = time.time()

    results = []
    results.append(fetch_data_sync("Database", 3))
    results.append(fetch_data_sync("Cache", 1))
    results.append(fetch_data_sync("External API", 2))

    end = time.time()
    print("Results:", results)
    print(f"Sync total time: {end - start:.2f} seconds")


main_sync()