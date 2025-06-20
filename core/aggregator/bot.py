from functools import cached_property

from pyrogram import Client
from pyrogram.handlers import RawUpdateHandler, DisconnectHandler
from pyrogram.raw.base import Update
from pyrogram.raw.types import UpdateNewMessage, UpdateEditMessage, KeyboardButtonUrl

from core.wallet.bot import Wallet


class Aggregator:

    @staticmethod
    def _is_cheque(update: Update):
        if isinstance(update, UpdateNewMessage) or isinstance(update, UpdateEditMessage):
            msg = update.message
            if msg.via_bot_id is not None \
                    and msg.via_bot_id == 1559501630 \
                    and msg.reply_markup is not None:
                if isinstance(msg.reply_markup.rows[0].buttons[0], KeyboardButtonUrl):
                    return msg.reply_markup.rows[0].buttons[0].url[23:25] == 'CQ'
        return False

    def __init__(self, client: Client, wallet: Wallet):
        self._client = client
        self._wallet = wallet
        self._client.add_handler(self.update_handler)

    def run(self):
        self._client.add_handler(self.disconnect_handler)
        self._client.run(self._wallet.start())
        self._client.run()

    @cached_property
    def disconnect_handler(self):
        async def handler(client: Client):
            await client.stop()
            await self._wallet.stop()

        return DisconnectHandler(handler)

    @cached_property
    def update_handler(self):
        async def handler(_, update: Update, __, ___):
            if self._is_cheque(update):
                await self._wallet.activate_cheque(update.message.reply_markup.rows[0].buttons[0].url[23:])

        return RawUpdateHandler(handler)
