from solend.solana_rpc import query_solana_account
from solend.schema import RESERVE_SCHEMA


def load_reserve_config(address, solana_rpc="https://api.mainnet-beta.solana.com"):
    reserve_metadata = query_solana_account(address, solana_rpc)
    config = RESERVE_SCHEMA.parse(reserve_metadata)
    return config