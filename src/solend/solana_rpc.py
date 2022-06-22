from solana.utils.helpers import decode_byte_string
from solana.rpc.api import Client


def query_solana_account(account, solana_rpc="https://api.mainnet-beta.solana.com"):
        http_client = Client(endpoint=solana_rpc)
        account_info = http_client.get_account_info(account)
        data = account_info["result"]["value"]["data"][0]
        data = decode_byte_string(data)
        return data
