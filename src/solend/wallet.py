from solend.api import solend_market_config
from solend.solana_rpc import query_solana_account
from solend.reserve import load_reserve_config
from solend.schema import USER_GENERAL_SCHEMA, USER_DEPOSIT_SCHEMA, USER_BORROW_SCHEMA
from solend.constant import WAD
from solana.utils.helpers import decode_byte_string
from solana.publickey import PublicKey
import numpy as np


def solend_wallet_account_state(wallet_address, 
                                market="main", 
                                deployment="production",
                                solend_api="https://api.solend.fi",
                                solana_rpc="https://api.mainnet-beta.solana.com",
                                ):
        config = solend_market_config(deployment, solend_api)
        market_metadata = next((m for m in config["markets"] if m["name"] == market))
        if market_metadata:
            market_address = market_metadata["address"]
            program_id = config["programID"]
            account_address = PublicKey.create_with_seed(PublicKey(wallet_address), 
                                                         market_address[0:32], 
                                                         PublicKey(program_id))
            data = query_solana_account(account_address, solana_rpc)
            return data


def calculate_positions(market_metadata, deposits, borrows, solana_rpc):
    user_total_deposit = 0
    user_total_borrow = 0
    borrow_limit = 0
    liquidation_threshold = 0
    deposits_parsed = []
    borrows_parsed = []
    
    for deposit in deposits:
        config = next((m for m in market_metadata["reserves"] if m["address"] == str(deposit.depositReserve)))
        reserve_config = load_reserve_config(config["address"], solana_rpc)
        
        ltv = reserve_config.loanToValueRatio
        liq_threshold = reserve_config.liquidationThreshold
        
        total_borrow_wads = reserve_config.borrowedAmountWads
        total_supply_wads = reserve_config.availableAmount * WAD
        total_deposit_wads = total_borrow_wads + total_supply_wads
        c_token_exchange_rate = total_deposit_wads / reserve_config.collateralMintTotalSupply / WAD
        supply_amount = np.floor(deposit.depositedAmount * c_token_exchange_rate)
        supply_amount = supply_amount / 10**reserve_config.liquidityMintDecimals

        asset_price_usd = reserve_config.marketPrice / WAD
        supply_amount_usd = supply_amount * asset_price_usd
        user_total_deposit += supply_amount_usd
        borrow_limit += supply_amount_usd * ltv / 100
        liquidation_threshold += supply_amount_usd * liq_threshold
        deposits_parsed.append({
            "asset": config["asset"],
            "amount": supply_amount
        })

    for borrow in borrows:
        config = next((m for m in market_metadata["reserves"] if m["address"] == str(borrow.borrowReserve)))
        reserve_config = load_reserve_config(config["address"])
        borrow_amount = borrow.borrowAmountWads * \
            reserve_config.cumulativeBorrowRateWads / borrow.cumulativeBorrowRateWads / WAD
        borrow_amount = borrow_amount / 10**reserve_config.liquidityMintDecimals

        asset_price_usd = reserve_config.marketPrice / WAD
        borrow_amount_usd = borrow_amount * asset_price_usd
        user_total_borrow += borrow_amount_usd
        borrows_parsed.append({
            "asset": config["asset"],
            "amount": borrow_amount
        })
        
    return {
        "deposits": deposits_parsed,
        "borrows": borrows_parsed,
        "liquidation_threshold": liquidation_threshold,
        "user_total_deposit": user_total_deposit,
        "user_total_borrow": user_total_borrow,
        "borrow_limit": borrow_limit,
        "borrow_utilization": user_total_borrow / borrow_limit,
        "net_account_value": user_total_deposit - user_total_borrow
    }


def fetch_obligation_by_wallet(address,
                               market="main",
                               deployment="production",
                               solend_api="https://api.solend.fi",
                               solana_rpc="https://api.mainnet-beta.solana.com",
                               ):
    config = solend_market_config(deployment, solend_api)
    market_metadata = next((m for m in config["markets"] if m["name"] == market))
    user_account_bytes = solend_wallet_account_state(address, market, deployment, solend_api, solana_rpc)
    user_general_payload = USER_GENERAL_SCHEMA.parse(user_account_bytes[0:USER_GENERAL_SCHEMA.sizeof()])

    deposit_borrow_data = user_account_bytes[USER_GENERAL_SCHEMA.sizeof():]
    deposits = []
    borrows = []
    deposits_len = user_general_payload.depositsLen
    borrows_len = user_general_payload.borrowsLen
    deposit_size = USER_DEPOSIT_SCHEMA.sizeof()
    borrow_size = USER_BORROW_SCHEMA.sizeof()

    for i in range(deposits_len):
        deposit_payload = USER_DEPOSIT_SCHEMA.parse(deposit_borrow_data[deposit_size*i:deposit_size*(i+1)])
        deposits.append(deposit_payload)

    for i in range(borrows_len):
        borrow_unpacked = USER_BORROW_SCHEMA.parse(
            deposit_borrow_data[deposits_len*deposit_size+i*borrow_size:deposits_len*deposit_size+(i+1)*borrow_size]
        )
        borrows.append(borrow_unpacked)

    
    obligation = calculate_positions(market_metadata, deposits, borrows, solana_rpc)
    return obligation


if __name__ == "__main__":
    obligation = fetch_obligation_by_wallet("3oSE9CtGMQeAdtkm2U3ENhEpkFMfvrckJMA8QwVsuRbE")
    print(obligation)