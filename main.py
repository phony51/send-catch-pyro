import os
from pathlib import Path

from pyrogram import Client

from config import load_config, SESSIONS_DIR
from core.aggregator.bot import Aggregator
from core.wallet.bot import Wallet


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
