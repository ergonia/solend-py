from solana.utils.helpers import decode_byte_string
from solana.rpc.api import Client, MemcmpOpt


def query_solana_account(account, solana_rpc="https://api.mainnet-beta.solana.com"):
    http_client = Client(endpoint=solana_rpc)
    account_info = http_client.get_account_info(account)
    data = account_info["result"]["value"]["data"][0]
    data = decode_byte_string(data)
    return data


def get_program_accounts(
        address,
        data_size,
        memcmp_offset,
        memcmp_bytes,
        encoding="base64",
        solana_rpc="https://api.mainnet-beta.solana.com",
        timeout=60
):
    http_client = Client(endpoint=solana_rpc, timeout=timeout)
    memcmp_opts = [MemcmpOpt(offset=memcmp_offset, bytes=memcmp_bytes)]
    data = http_client.get_program_accounts(
        pubkey=address,
        encoding=encoding,
        data_size=data_size,
        memcmp_opts=memcmp_opts
    )
    return data


if __name__ == "__main__":
    program_account = "So1endDq2YkqhipRh3WViPa8hdiSpxWy6z3Z6tMCpAo"
    main_pool = "4UpD2fh7xH3VP9QQaXtsS1YY3bxzWhtfpks7FatyKvdY"
    data = get_program_accounts(program_account, 619, 10, main_pool)
    print(data)
