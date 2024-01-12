import json
from config import GlobalConfig
global_config = GlobalConfig()


class BurrowHandler:
    def __init__(self, signer, contract_id):
        self._signer = signer
        self._contract_id = contract_id

    def storage_balance_of(self, account_id: str):
        return self._signer.view_function(
            self._contract_id,
            "storage_balance_of",
            {
                "account_id": account_id,
            }
        )['result']

    def get_assets_paged_detailed(self):
        return self._signer.view_function(
            self._contract_id,
            "get_assets_paged_detailed",
            {
                "from_index": 0,
                "limit": 100
            }
        )['result']

    def get_asset_farms_paged(self):
        return self._signer.view_function(
            self._contract_id,
            "get_asset_farms_paged",
            {
                "from_index": 0,
                "limit": 100
            }
        )['result']

    def get_account(self, account_id: str):
        return self._signer.view_function(
            self._contract_id,
            "get_account",
            {
                "account_id": account_id
            }
        )['result']

    def get_price_data(self):
        return self._signer.view_function(
            self._contract_id,
            "get_price_data",
            {
            }
        )['result']

    def ft_metadata(self):
        return self._signer.view_function(
            self._contract_id,
            "ft_metadata",
            {
            }
        )['result']

    def deposit(self, deposit: str):
        return {
            "contract_id": self._contract_id,
            "method_name": "ft_transfer_call",
            "args": {
                "receiver_id": global_config.burrow_contract,
                "amount": deposit,
                "msg": ""
            },
            "amount": global_config.deposit_yocto
        }

    def deposit_collateral(self, deposit: str, max_amount: str):
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
                "amount": deposit,
                "msg": json.dumps(msg)
            },
            "amount": global_config.deposit_yocto
        }

    def burrow(self, amount: str):
        msg = {
            "Execute": {
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

    def repay_from_supplied(self, amount: str, contract_id: str):
        return {
            "contract_id": global_config.burrow_contract,
            "method_name": "execute",
            "args": {
                "actions": [
                    {
                        "Repay": {
                            "token_id": contract_id,
                            "max_amount": amount
                        }
                    }
                ]
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

    def get_assets(self):
        return self._signer.view_function(
            self._contract_id,
            "get_asset",
            {
                "asset_id": "usdt.tether-token.near"
            }
        )['result']

    def ft_balance_of(self, account_id):
        return self._signer.view_function(
            self._contract_id,
            "ft_balance_of",
            {
                "account_id": account_id
            }
        )['result']

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

