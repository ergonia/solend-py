from solend.api import solend_market_config
from solend.solana_rpc import query_solana_account
from solend.schema import ACCOUNT_SCHEMA, RESERVE_SCHEMA
from solend.constant import WAD
from solana.publickey import PublicKey
import numpy as np


def solend_wallet_account_state(
    wallet_address, 
    market="main", 
    deployment="production",
    solend_api="https://api.solend.fi",
    solana_http_rpc="https://api.mainnet-beta.solana.com",
):
        config = solend_market_config(deployment, solend_api)
        market_metadata = next((m for m in config["markets"] if m["name"] == market))
        if market_metadata:
            market_address = market_metadata["address"]
            program_id = config["programID"]
            account_address = PublicKey.create_with_seed(PublicKey(wallet_address), 
                                                         market_address[0:32], 
                                                         PublicKey(program_id))
            data = query_solana_account(account_address, layout=ACCOUNT_SCHEMA, solana_http_rpc=solana_http_rpc)
            return data


def compute_deposit_quantity(deposit, reserve):
    total_borrow_wads = reserve.borrowedAmountWads
    total_supply_wads = reserve.availableAmount * WAD
    total_deposit_wads = total_borrow_wads + total_supply_wads
    c_token_exchange_rate = total_deposit_wads / reserve.collateralMintTotalSupply / WAD
    amount = np.floor(deposit.depositedAmount * c_token_exchange_rate)
    amount = amount / 10**reserve.liquidityMintDecimals
    return amount


def compute_borrow_quantity(borrow, reserve):
    amount = borrow.borrowAmountWads * \
        reserve.cumulativeBorrowRateWads / borrow.cumulativeBorrowRateWads / WAD
    amount = amount / 10**reserve.liquidityMintDecimals
    return amount


def load_price(reserve):
    return reserve.marketPrice / WAD


def load_reserve(address, market_metadata, solana_rpc):
    config = next((m for m in market_metadata["reserves"] if m["address"] == str(address)))
    reserve = query_solana_account(config["address"], layout=RESERVE_SCHEMA, solana_http_rpc=solana_rpc)
    return reserve, config["asset"]


def calculate_positions(
    account_payload,
    market_metadata,
    solana_rpc
):
    user_total_deposit = 0
    user_total_borrow = 0
    borrow_limit = 0
    liquidation_threshold = 0
    deposits_parsed = []
    borrows_parsed = []
    
    for deposit in account_payload.deposits:
        reserve, asset = load_reserve(deposit.depositReserve, market_metadata, solana_rpc)

        ltv = reserve.loanToValueRatio / 100
        liq_threshold = reserve.liquidationThreshold / 100
        supply_amount = compute_deposit_quantity(deposit, reserve)
        price = load_price(reserve)
        
        supply_amount_usd = supply_amount * price
        user_total_deposit += supply_amount_usd
        borrow_limit += supply_amount_usd * ltv
        liquidation_threshold += supply_amount_usd * liq_threshold
        deposits_parsed.append({
            "asset": asset,
            "amount": supply_amount,
            "amount_usd": supply_amount_usd
        })

    for borrow in account_payload.borrows:
        reserve, asset = load_reserve(borrow.borrowReserve, market_metadata, solana_rpc)
        borrow_amount = compute_borrow_quantity(borrow, reserve)
        price = load_price(reserve)
        
        borrow_amount_usd = borrow_amount * price
        user_total_borrow += borrow_amount_usd
        borrows_parsed.append({
            "asset": asset,
            "amount": borrow_amount,
            "amount_usd": borrow_amount_usd
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


def fetch_obligation_by_wallet(
    address,
    market="main",
    deployment="production",
    solend_api="https://api.solend.fi",
    solana_rpc="https://api.mainnet-beta.solana.com",
):
    config = solend_market_config(deployment, solend_api)
    market_metadata = next((m for m in config["markets"] if m["name"] == market))
    account_payload = solend_wallet_account_state(address, market, deployment, solend_api, solana_rpc)
    
    obligation = calculate_positions(account_payload, market_metadata, solana_rpc)
    return obligation


if __name__ == "__main__":
    obligation = fetch_obligation_by_wallet("3oSE9CtGMQeAdtkm2U3ENhEpkFMfvrckJMA8QwVsuRbE")
    print(obligation)