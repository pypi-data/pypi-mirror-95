# MCOauth
This is a simple package to use MCOauth. Initialize a Minecraft Player
``` 
MinecraftPlayer(token)
```
Most things are async except for initializing MinecraftPlayer which is not a blocking call because it uses
```
asyncio.run
```
A MinecraftPlayer has two properties, uuid and username.
Using
```
int(MinecraftPlayer(token))
```
will return token.
Note that tokens are only valid for 5 minutes, see https://mc-oauth.net/