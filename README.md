## Response Code List

| Response Code | Description                 |
| ------------- | --------------------------- |
| 0             | Successful API call         |
| 1001          | Contract call exception     |
| 1002          | Mandatory parameter missing |
| 1003          | Incorrect parameter type    |

**Note**: For all inputs involving amounts, the amount should be entered with decimal precision as per the decimal precision in the metadata.

---

## NETWORK
- **TEST_URL**:https://test-api.burrow.finance
- **PROD_URL**:https://api.burrow.finance

## 1. Account Query

- **Test Interface URL**: [https://test-api.burrow.finance/storage_balance_of](https://test-api.burrow.finance/storage_balance_of)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description            |
| ---------- | ---------- | ---------------------- |
| token_id   | String     | Contract address       |
| account_id | String     | Account to be queried  |

**Sample Call**:

```
{
  "token_id": "contract.main.burrow.near",
  "account_id": "account.near"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "available": "150000000000000000000000",
    "total": "250000000000000000000000"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Storage fees for the current account           |

---

## 2. Account Registration

- **Test Interface URL**: [https://test-api.burrow.finance/storage_deposit](https://test-api.burrow.finance/storage_deposit)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                     |
| ---------- | ---------- | ----------------------------------------------- |
| token_id   | String     | Contract address                                |
| account_id | String     | Account to be queried                           |
| amount     | String     | Storage fee in yoctoNear, as per burrow contract |

**Sample Call**:

```
{
  "account_id": "dom1.near",
  "token_id": "contract.main.burrow.near",
  "amount": 1
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "account_id": "dom1.near"
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "storage_deposit"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Parameters of the contract call                |


## 3. Token Asset List

- **Test Interface URL**: [https://test-api.burrow.finance/get_assets_paged_detailed](https://test-api.burrow.finance/get_assets_paged_detailed)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": [
    {
      "borrow_apr": "0.0",
      "borrowed": {
        "balance": "0",
        "shares": "0"
      },
      ...
      "token_id": "token.burrow.near"
    },
    ...
  ],
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Successful return of token asset list          |


## 4. Farms List

- **Test Interface URL**: [https://test-api.burrow.finance/get_asset_farms_paged](https://test-api.burrow.finance/get_asset_farms_paged)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": [
    [
      {
        "Supplied": "token.burrow.near"
      },
      {
        "block_timestamp": "1700208807839905264",
        "rewards": {
          "token.burrow.near": {
            "boosted_shares": "255113043332545463643545574",
            "booster_log_base": "0",
            "remaining_rewards": "177511740235341250000406",
            "reward_per_day": "12000000000000000000000"
          }
        }
      }
    ]
  ],
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Successful return of farm list                 |

---

## 5. Account Asset Details

- **Test Interface URL**: [https://test-api.burrow.finance/get_account/juaner.near](https://test-api.burrow.finance/get_account/juaner.near)
- **Method**: GET

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "account_id": "juaner.near",
    "booster_staking": {
      "staked_booster_amount": "10000000000000000000",
      "unlock_timestamp": "1702705309123136860",
      "x_booster_amount": "10000000000000000000"
    },
    "borrowed": [{
      "apr": "0.020115787307602972732631807",
      "balance": "2000063444139612355115550",
      "shares": "1824204883064976309651628",
      "token_id": "wrap.near"
    }],
    ...
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Current account's asset balance in the contract |


## 6. Price Query

- **Test Interface URL**: [https://test-api.burrow.finance/get_price_data](https://test-api.burrow.finance/get_price_data)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "prices": [
      {
        "asset_id": "wrap.near",
        "price": {
          "decimals": 28,
          "multiplier": "18900"
        }
      },
      {
        "asset_id": "c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2.factory.bridge.near",
        "price": null
      },
      ...
    ],
    "recency_duration_sec": 90,
    "timestamp": "1700211816385474579"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Token price list                               |

---

## 7. Token Analysis Data List

- **Test Interface URL**: [https://test-api.burrow.finance/list_token_data](https://test-api.burrow.finance/list_token_data)
- **Method**: GET

**Parameter Description**: No parameters

**Sample Return Data**:

```
{
  "code": "0",
  "data": [
    {
      "available_liquidity_balance": "262203363.455576",
      "available_liquidity_price": "103140.315049",
      "base_apy": "0.00",
      "borrow_apy": "0.00",
      "net_liquidity_apy": "1.85",
      "price": "0.00039336",
      "supply_apy": "3.52",
      "supply_farm_apy": "1.67",
      "symbol": "BRRR",
      "token": "token.burrow.near",
      ...
    },
    ...
  ],
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Token information data list                    |


## 8. Supply

- **Test Interface URL**: [https://test-api.burrow.finance/supply](https://test-api.burrow.finance/supply)
- **Method**: POST

**Parameter Description**:

| Field Name    | Field Type | Description                             |
| ------------- | ---------- | --------------------------------------- |
| token_id      | String     | Token to operate on                     |
| amount        | String     | Supply amount, precision as per metadata|
| is_collateral | Boolean    | Whether to use as collateral            |

**Sample Call**:

```
{
  "token_id": "a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near",
  "amount": "1000000",
  "is_collateral": true
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "amount": "1000000",
      "msg": "{\"Execute\": {\"actions\": [{\"IncreaseCollateral\": {\"token_id\": \"a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near\", \"max_amount\": \"1000000000000000000\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.factory.bridge.near",
    "method_name": "ft_transfer_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

---

## 9. Burrow

- **Test Interface URL**: [https://test-api.burrow.finance/burrow](https://test-api.burrow.finance/burrow)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Burrow amount, precision as per metadata  |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "1": 1,
    "args": {
      "msg": "{\"Execute\": {\"actions\": [{\"Borrow\": {\"token_id\": \"wrap.near\", \"amount\": \"1\"}}, {\"Withdraw\": {\"token_id\": \"wrap.near\", \"max_amount\": \"1\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "priceoracle.near",
    "method_name": "oracle_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |


## 10. Withdraw

- **Test Interface URL**: [https://test-api.burrow.finance/withdraw](https://test-api.burrow.finance/withdraw)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Withdrawal amount, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "actions": [
        {
          "Withdraw": {
            "max_amount": "1",
            "token_id": "wrap.near"
          }
        }
      ]
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "execute"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

---

## 11. Repay from Wallet

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_wallet](https://test-api.burrow.finance/repay_from_wallet)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Repayment amount, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "amount": "1",
      "msg": "{\"Execute\": {\"actions\": [{\"Repay\": {\"max_amount\": \"1000000000000\", \"token_id\": \"17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",
    "method_name": "ft_transfer_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |


## 12. Repay from Supplied

- **Test Interface URL**: [https://test-api.burrow.finance/repay_from_supplied](https://test-api.burrow.finance/repay_from_supplied)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                               |
| ---------- | ---------- | ----------------------------------------- |
| token_id   | String     | Token to operate on                       |
| amount     | String     | Repayment amount, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "wrap.near",
  "amount": "1000000000000000000000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "actions": [
        {
          "Repay": {
            "max_amount": "1000000000000",
            "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"
          }
        }
      ]
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "execute"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |

---

## 13. Increase Collateral

- **Test Interface URL**: [https://test-api.burrow.finance/increase_collateral](https://test-api.burrow.finance/increase_collateral)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                |
| ---------- | ---------- | ------------------------------------------ |
| token_id   | String     | Token to operate on                        |
| amount     | String     | Amount to increase collateral, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",
  "amount": "1000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "actions": [
        {
          "IncreaseCollateral": {
            "max_amount": "1000000000000",
            "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"
          }
        }
      ]
    },
    "contract_id": "contract.main.burrow.near",
    "method_name": "execute"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |


## 14. Decrease Collateral

- **Test Interface URL**: [https://test-api.burrow.finance/decrease_collateral](https://test-api.burrow.finance/decrease_collateral)
- **Method**: POST

**Parameter Description**:

| Field Name | Field Type | Description                                 |
| ---------- | ---------- | ------------------------------------------- |
| token_id   | String     | Token to operate on                         |
| amount     | String     | Amount to decrease collateral, precision as per metadata |

**Sample Call**:

```
{
  "token_id": "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",
  "amount": "1000000"
}
```

**Sample Return Data**:

```
{
  "code": "0",
  "data": {
    "amount": 1,
    "args": {
      "msg": "{\"Execute\": {\"actions\": [{\"DecreaseCollateral\": {\"token_id\": \"17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1\", \"max_amount\": \"1000000000000\"}}]}}",
      "receiver_id": "contract.main.burrow.near"
    },
    "contract_id": "priceoracle.near",
    "method_name": "oracle_call"
  },
  "msg": "success"
}
```

**Return Parameter Description**:

| Field Name | Field Type | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| code       | String     | Response code, 0 for success                   |
| msg        | String     | 'success' for successful return, error message for exceptions |
| data       | Object     | Contract call parameters                       |
