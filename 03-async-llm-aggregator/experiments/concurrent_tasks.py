import asyncio


async def provider_a() -> str:
    print("Provider A started")
    await asyncio.sleep(2)
    print("Provider A finished")
    return "Response from Provider A"


async def provider_b() -> str:
    print("Provider B started")
    await asyncio.sleep(3)
    print("Provider B finished")
    return "Response from Provider B"


async def provider_c() -> str:
    print("Provider C started")
    await asyncio.sleep(1)
    print("Provider C finished")
    return "Response from Provider C"
