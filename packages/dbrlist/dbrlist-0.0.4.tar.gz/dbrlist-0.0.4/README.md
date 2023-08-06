# DBList

An async wrapper for DBL api.

Example:
```py
import dbrlist
import asyncio

client = dbrlist.Client(auth_key)
print(asyncio.get_event_loop().run_until_complete(client.metrics(bot_id)))
```
