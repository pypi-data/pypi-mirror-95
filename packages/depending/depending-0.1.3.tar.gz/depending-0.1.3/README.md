# Depending

Yet another dependency injection framework for python.

## Usage

```python
import asyncio
from depending import dependency, bind, dependencies

@dependency
async def name():
    return "Item"

@bind
async def function(name):
    print(name)

async def main():
    async with dependencies():
        await function()

asyncio.run(main())
```

