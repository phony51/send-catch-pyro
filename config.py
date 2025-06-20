from pathlib import Path

from pydantic import BaseModel, alias_generators, ConfigDict

SESSIONS_DIR = 'sessions'
class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True
    )


class Client(CamelCaseBaseModel):
    api_id: int
    api_hash: str
    phone: str


class Clients(CamelCaseBaseModel):
    wallet: Client
    aggregator: Client


class Configuration(CamelCaseBaseModel):
    clients: Clients


def load_config(path: Path) -> Configuration:
    with open(path, 'r') as f:
        return Configuration.model_validate_json(f.read())
