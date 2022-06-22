# Solend Python Explorer
A python library for interacting with solend. In current state this library provides the ability to parse the position of a wallet.

Usage

```
from solend.wallet import fetch_obligation_by_wallet
fetch_obligation_by_wallet("3oSE9CtGMQeAdtkm2U3ENhEpkFMfvrckJMA8QwVsuRbE")
```
Output
```
{
  "deposits": [
    {
      "asset": "SOL",
      "amount": 4000016.620523712
    }
  ],
  "borrows": [
    {
      "asset": "USDT",
      "amount": 0.49660628370575016
    },
    {
      "asset": "USDC",
      "amount": 72833116.89264491
    }
  ],
  "liquidation_threshold": 12022575880.969307,
  "user_total_deposit": 141442069.1878742,
  "user_total_borrow": 72833135.5969685,
  "borrow_limit": 106081551.89090565,
  "borrow_utilization": 0.6865768297947805,
  "net_account_value": 68608933.5909057
}
```
