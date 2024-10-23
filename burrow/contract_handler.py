import json
from config import GlobalConfig
from cachetools import TTLCache
import copy

global_config = GlobalConfig()
cache = TTLCache(maxsize=10000, ttl=600)

class BurrowHandler:
    def __init__(self, signer, contract_id):
        self._signer = signer
        self._contract_id = contract_id

    def storage_balance_of(self, account_id: str):
        cache_key = 'storage_balance_of' + self._contract_id + account_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "storage_balance_of",
                {
                    "account_id": account_id,
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_assets_paged_detailed(self):
        cache_key = 'get_assets_paged_detailed' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_assets_paged_detailed",
                {
                    "from_index": 0,
                    "limit": 100
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_asset_farms_paged(self):
        cache_key = 'get_asset_farms_paged' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_asset_farms_paged",
                {
                    "from_index": 0,
                    "limit": 100
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_account(self, account_id: str):
        cache_key = 'get_account' + self._contract_id + account_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_account",
                {
                    "account_id": account_id
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        new_cache_value = copy.deepcopy(cache_value)
        return new_cache_value

    def get_price_data(self):
        cache_key = 'get_price_data' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_price_data",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def ft_metadata(self):
        cache_key = 'ft_metadata' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "ft_metadata",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def deposit(self, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }

    def deposit_collateral(self, amount: str, max_amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "IncreaseCollateral": {
                        "token_id": self._contract_id,
                        "max_amount": max_amount
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def burrow(self, amount: str):
        msg = {
            "actions": [{
                "Borrow": {
                    "token_id": self._contract_id,
                    "amount": amount
                }
            }, {
                "Withdraw": {
                    "token_id": self._contract_id,
                    "max_amount": amount
                }
            }]
        }
        return {
            "contract_id": global_config.priceoracle_contract,
            "method_name": "oracle_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def burrow_lp(self, amount: str, token_id: str, position: str):
        msg = {
            "Execute": {
                "actions": [{
                    "PositionBorrow": {
                        "asset_amount": {
                            "token_id": token_id,
                            "amount": amount
                        },
                        "position": position,
                    },
                }, {
                    "Withdraw": {
                        "token_id": token_id,
                        "max_amount": amount
                    }
                }]
            }
        }
        return {
            "contract_id": global_config.priceoracle_contract,
            "method_name": "oracle_call",
            "args": {
                "receiver_id": self._contract_id,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def burrow_pyth(self, amount: str):
        msg = {
            "actions": [{
                "Borrow": {
                    "token_id": self._contract_id,
                    "amount": amount
                }
            }, {
                "Withdraw": {
                    "token_id": self._contract_id,
                    "max_amount": amount
                }
            }]
        }
        return {
            "contract_id": global_config.burrow_contract,
            "method_name": "execute_with_pyth",
            "args": json.dumps(msg),
            "amount": global_config.deposit_yocto
        }

    def burrow_pyth_lp(self, amount: str, token_id: str, position: str):
        msg = {
            "actions": [{
                "PositionBorrow": {
                    "asset_amount": {
                        "token_id": token_id,
                        "amount": amount
                    },
                    "position": position,
                },
            }, {
                "Withdraw": {
                    "token_id": token_id,
                    "max_amount": amount
                }
            }]
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "execute_with_pyth",
            "args": json.dumps(msg),
            "amount": global_config.deposit_yocto
        }

    def near_withdraw(self, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "near_withdraw",
            "args": {
                "amount": amount
            },
            "amount": global_config.deposit_yocto
        }

    def withdraw(self, amount: str):
        return {
            "contract_id": global_config.burrow_contract,
            "method_name": "execute",
            "args": {
                "actions": [
                    {
                        "Withdraw": {
                            "token_id": self._contract_id,
                            "max_amount": amount
                        }
                    }
                ]
            },
            "amount": global_config.deposit_yocto
        }

    def repay_from_wallet(self, amount: str, max_amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "Repay": {
                        "max_amount": max_amount,
                        "token_id": self._contract_id,
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def repay_from_wallet_lp(self, amount: str, token_id: str, position: str, max_amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "PositionRepay": {
                        "position": position,
                        "asset_amount": {
                            "amount": max_amount,
                            "token_id": token_id
                        }
                    }
                }]
            }
        }
        return {
            "contract_id": token_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": self._contract_id,
                "amount": amount,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def repay_from_supplied(self, amount: str, token_id: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "execute",
            "args": {
                "actions": [
                    {
                        "Repay": {
                            "token_id": token_id,
                            "max_amount": amount
                        }
                    }
                ]
            },
            "amount": global_config.deposit_yocto
        }

    def repay_from_supplied_lp(self, amount: str, token_id: str, position: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "execute",
            "args": {
                "actions": [{
                    "PositionRepay": {
                        "position": position,
                        "asset_amount": {
                            "token_id": token_id,
                            "amount": amount
                        }
                    }
                }]
            },
            "amount": global_config.deposit_yocto
        }

    def storage_deposit(self, account_id: str, amount: float):
        return {
            "contract_id": self._contract_id,
            "method_name": "storage_deposit",
            "args": {
                "account_id": account_id
            },
            "amount": amount
        }

    def decrease_collateral(self, token_id: str, amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "DecreaseCollateral": {
                        "token_id": token_id,
                        "max_amount": amount
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "oracle_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def decrease_collateral_pyth(self, token_id: str, amount: str):
        msg = {
            "actions": [{
                "DecreaseCollateral": {
                    "token_id": token_id,
                    "max_amount": amount
                }
            }]
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "execute_with_pyth",
            "args": json.dumps(msg),
            "amount": global_config.deposit_yocto
        }

    def decrease_collateral_pyth_lp(self, token_id: str, amount: str):
        msg = {
                "actions": [{
                    "PositionDecreaseCollateral": {
                        "position": token_id,
                        "asset_amount": {
                            "token_id": token_id,
                            "amount": amount
                        }
                    }
                }]
            }
        return {
            "contract_id": self._contract_id,
            "method_name": "execute_with_pyth",
            "args": json.dumps(msg),
            "amount": global_config.deposit_yocto
        }

    def decrease_collateral_lp(self, token_id: str, amount: str):
        msg = {
            "Execute": {
                "actions": [{
                    "PositionDecreaseCollateral": {
                        "position": token_id,
                        "asset_amount": {
                            "token_id": token_id,
                            "amount": amount
                        }
                    }
                }]
            }
        }
        return {
            "contract_id": self._contract_id,
            "method_name": "oracle_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def increase_collateral(self, token_id: str, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "execute",
            "args": {
                "actions": [{
                    "IncreaseCollateral": {
                        "token_id": token_id,
                        "max_amount": amount
                    }
                }]
            },
            "amount": global_config.deposit_yocto
        }

    def increase_collateral_lp(self, token_id: str, amount: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "execute",
            "args": {
                "actions": [{
                    "PositionIncreaseCollateral": {
                        "position": token_id,
                        "asset_amount": {
                            "token_id": token_id,
                            "amount": amount
                        }
                    }
                }]
            },
            "amount": global_config.deposit_yocto
        }

    def get_assets(self):
        cache_key = 'get_assets' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_asset",
                {
                    "asset_id": "usdt.tether-token.near"
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def ft_balance_of(self, account_id):
        cache_key = 'ft_balance_of' + self._contract_id + account_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "ft_balance_of",
                {
                    "account_id": account_id
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def account_stake_booster(self, amount: str, duration: int):
        return {
            "contract_id": self._contract_id,
            "method_name": "account_stake_booster",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": amount,
                "duration": duration
            },
        }

    def account_unstake_booster(self):
        return {
            "contract_id": self._contract_id,
            "method_name": "account_unstake_booster",
            "args": {
                "receiver_id": global_config.burrow_contract
            },
        }

    def account_farm_claim_all(self):
        return {
            "contract_id": self._contract_id,
            "method_name": "account_farm_claim_all",
            "args": None,
        }

    def get_account_all_positions(self, account_id: str):
        cache_key = 'get_account_all_positions' + self._contract_id + account_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_account_all_positions",
                {
                    "account_id": account_id
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        new_cache_value = copy.deepcopy(cache_value)
        return new_cache_value

    def get_config(self):
        cache_key = 'get_config' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_config",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_unit_lpt_assets(self, pool_ids: list):
        cache_key = 'get_unit_lpt_assets' + self._contract_id + str(pool_ids)
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_unit_lpt_assets",
                {
                    "pool_ids": pool_ids
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_pool_shares(self, account_id: str, pool_id: int):
        cache_key = 'get_pool_shares' + self._contract_id + account_id + str(pool_id)
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_pool_shares",
                {
                    "account_id": account_id,
                    "pool_id": pool_id
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_shadow_records(self, account_id: str):
        cache_key = 'get_shadow_records' + self._contract_id + account_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_shadow_records",
                {
                    "account_id": account_id
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def shadow_action(self, amount: str, pool_id: int):
        # msg = {
        #     "Execute": {
        #         "actions": [{
        #             "PositionIncreaseCollateral": {
        #                 "position": position,
        #                 "asset_amount": {
        #                     "token_id": position
        #                 }
        #             }
        #         }]
        #     }
        # }
        ret = {
            "contract_id": self._contract_id,
            "method_name": "shadow_action",
            "args": {
                "action": "ToBurrowland",
                "pool_id": pool_id,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }
        if amount != "":
            ret["args"]["amount"] = amount
        return ret

    def shadow_action_collateral(self, token_id: str, amount: str, pool_id: int):
        msg = {
            "Execute": {
                "actions": [{
                    "PositionIncreaseCollateral": {
                        "position": token_id,
                        "asset_amount": {
                            "token_id": token_id
                        }
                    }
                }]
            }
        }
        ret = {
            "contract_id": self._contract_id,
            "method_name": "shadow_action",
            "args": {
                "action": "ToBurrowland",
                "pool_id": pool_id,
                "amount": amount,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }
        return ret

    def withdraw_lp(self, amount: str, pool_id: int):
        ret = {
            "contract_id": self._contract_id,
            "method_name": "shadow_action",
            "args": {
                "action": "FromBurrowland",
                "pool_id": pool_id,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }
        if amount != "":
            ret["args"]["amount"] = amount
        return ret

    def get_all_token_pyth_infos(self):
        cache_key = 'get_all_token_pyth_infos' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_all_token_pyth_infos",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_nearx_price(self):
        cache_key = 'get_nearx_price' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_nearx_price",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def ft_price(self):
        cache_key = 'ft_price' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "ft_price",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_st_near_price(self):
        cache_key = 'get_st_near_price' + self._contract_id
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_st_near_price",
                {
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def get_price(self, price_identifier):
        cache_key = 'get_price' + self._contract_id + price_identifier
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                "get_price",
                {
                    "price_identifier": price_identifier
                }
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value

    def ft_contract_call(self, method, args):
        cache_key = 'ft_contract_call' + self._contract_id + method + str(args)
        cache_value = cache.get(cache_key, None)
        if cache_value is None:
            ret = self._signer.view_function(
                self._contract_id,
                method,
                args
            )['result']
            cache_value = ret
            cache[cache_key] = ret
        return cache_value
