# DBList

An async wrapper for DBL api.

Example:
```py
import dblist
import asyncio

client = dblist.Client(auth_key)
print(asyncio.get_event_loop().run_until_complete(client.metrics(bot_id)))
```
