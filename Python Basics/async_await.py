
# Async/Await

import asyncio

async def make_tea():
    print("Tea is being made...")
    await asyncio.sleep(2)
    print("Tea is ready!")

async def make_coffee():
    print("Coffee is being made...")
    await asyncio.sleep(1)
    print("Coffee is ready!")

async def main():
    await asyncio.gather(make_tea(), make_coffee())

asyncio.run(main())