from pyrogram import Client


class Wallet:
    __slots__ = 'client',

    def __init__(self, client: Client):
        self.client = client

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.stop()

    async def activate_cheque(self, cheque_id: str):
        await self.client.send_message(1559501630, text=f'/start {cheque_id}')
