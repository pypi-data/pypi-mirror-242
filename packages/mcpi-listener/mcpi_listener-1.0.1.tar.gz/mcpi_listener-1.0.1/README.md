# Package for listening to the minecraft events (uses MCPI)
## Installing
```
pip install mcpi_listener
```
## Usage examples
### Chat posts
```
from mcpi.minecraft import Minecraft
from mcpi_listener import McpiListener

mc = Minecraft.Create()
listener = McpiListener(mc)

for chat_post in listener.listen_chat_posts():
    print(chat_post)
```
### Block hits
```
from mcpi.minecraft import Minecraft
from mcpi_listener import McpiListener

mc = Minecraft.Create()
listener = McpiListener(mc)

for block_hit in listener.listen_block_hits():
    print(block_hit)
```
### Projectile hits
```
from mcpi.minecraft import Minecraft
from mcpi_listener import McpiListener

mc = Minecraft.Create()
listener = McpiListener(mc)

for projectile_hit in listener.listen_projectile_hits():
    print(projectile_hit)
```