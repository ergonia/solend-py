# solend-py
A python library for interacting with solend

Usage

```
from solend.wallet import fetch_obligation_by_wallet
fetch_obligation_by_wallet("3oSE9CtGMQeAdtkm2U3ENhEpkFMfvrckJMA8QwVsuRbE")
```
Output
```
{'deposits': [{'asset': 'SOL', 'amount': 4501990.960223003}],
 'borrows': [{'asset': 'USDT', 'amount': 1550348.3728843194},
  {'asset': 'USDC', 'amount': 82820648.67344044}],
 'liquidation_threshold': 13340776430.450378,
 'user_total_deposit': 156950310.94647503,
 'user_total_borrow': 84369209.06055328,
 'borrow_limit': 11771273320.985626,
 'borrow_utilization': 0.007167381706288417,
 'net_account_value': 72581101.88592175
 }
```
