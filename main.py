import os
from pathlib import Path

from pyrogram import Client, utils

from config import load_config, SESSIONS_DIR
from core.aggregator.bot import Aggregator
from core.wallet.bot import Wallet


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new  # FIX INVALID PEER


def main():
    if os.name == 'posix':
        import uvloop
        uvloop.install()

    config = load_config(Path('configuration.json'))
    aggregator_client = Client('aggregator',
                               config.clients.aggregator.api_id,
                               config.clients.aggregator.api_hash,
                               workdir=SESSIONS_DIR,
                               phone_number=config.clients.aggregator.phone)
    wallet_client = Client('wallet',
                           config.clients.wallet.api_id,
                           config.clients.wallet.api_hash,
                           workdir=SESSIONS_DIR,
                           phone_number=config.clients.wallet.phone)

    aggregator = Aggregator(aggregator_client, Wallet(wallet_client))
    aggregator.run()


if __name__ == '__main__':
    main()
