from mcpi.minecraft import Minecraft
from mcpi.event import ChatEvent, BlockEvent, ProjectileEvent

class McpiListener():
    def __init__(self, mc:Minecraft):
        self.mc = mc
    
    def listen_chat_posts(self) -> ChatEvent:
        """
        listens to chat posts events

        :yields: :class:`ChatEvent`
        """
        while True:
            for chat_event in self.mc.events.pollChatPosts():
                yield chat_event

    def listen_block_hits(self) -> BlockEvent:
        """
        listens to block hits events

        :yields: :class:`BlockEvent`
        """
        while True:
            for block_event in self.mc.events.pollBlockHits():
                yield block_event

    def listen_projectile_hits(self) -> ProjectileEvent:
        """
        listens to projectile hits events

        :yields: :class:`ProjectileEvent`
        """
        while True:
            for projectile_event in self.mc.events.pollProjectileHits():
                yield projectile_event