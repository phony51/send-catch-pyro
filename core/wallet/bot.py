from pyrogram import Client


class Wallet:
    def __init__(self, client: Client):
        self._client = client

    async def start(self):
        await self._client.start()

    async def stop(self):
        await self._client.stop()

    async def activate_cheque(self, cheque_id: str):
        await self._client.send_message(1559501630, text=f'/start {cheque_id}')
