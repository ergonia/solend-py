from borsh_construct import CStruct, U8, U64, U128
from anchorpy.borsh_extension import BorshPubkey, Padding


RESERVE_SCHEMA = CStruct(
    "version" / U8,
    "slot" / U64,
    "stale" / U8,
    "lendingMarket" / BorshPubkey,
    "liquidityMintPubkey" / BorshPubkey,
    "liquidityMintDecimals" / U8,
    "liquiditySupplyPubkey" / BorshPubkey,
    "pythOracle" / BorshPubkey,
    "switchboardOracle" / BorshPubkey,
    "availableAmount" / U64,
    "borrowedAmountWads" / U128,
    "cumulativeBorrowRateWads" / U128,
    "marketPrice" / U128,
    "collateralMintPubkey" / BorshPubkey,
    "collateralMintTotalSupply" / U64,
    "collateralSupplyPubkey" / BorshPubkey,
    "optimalUtilizationRate" / U8,
    "loanToValueRatio" / U8,
    "liquidationBonus" / U8,
    "liquidationThreshold" / U8,
    "minBorrowRate" / U8,
    "optimalBorrowRate" / U8,
    "maxBorrowRate" / U8,
    "borrowFeeWad" / U64,
    "flashLoanFeeWad" / U64,
    "hostFeePercentage" / U8,
    "depositLimit" / U64,
    "borrowLimit" / U64,
    "feeReceiver" / BorshPubkey
)

OVERVIEW_SCHEMA = CStruct(
    "version" / U8,
    "slot" / U64,
    "stale" / U8,
    "lendingMarket"/ BorshPubkey,
    "owner" / BorshPubkey,
    "depositedValue" / U128,
    "borrowedValue" / U128,
    "allowedBorrowValue" / U128,
    "unhealthyBorrowValue" / U128,
    "padding" / Padding(64),
    "depositsLen" / U8,
    "borrowsLen" / U8
)

DEPOSIT_SCHEMA =  CStruct(
    "depositReserve" / BorshPubkey,
    "depositedAmount" / U64,
    "marketValue" / U128,
    "padding" / Padding(32)
)

BORROW_SCHEMA = CStruct(
    "borrowReserve" / BorshPubkey,
    "cumulativeBorrowRateWads" / U128,
    "borrowAmountWads" / U128,
    "marketValue" / U128,
    "padding" / Padding(32)
)

LIQUIDATION_TRANSACTION_SCHEMA = CStruct(
    "instruction" / U8,
    "liquidityAmount" / U64
)