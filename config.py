import os


class GlobalConfig:
    def __init__(self):
        near_env = os.getenv('NEAR_ENV')
        if near_env:
            if near_env not in ["mainnet", "testnet"]:
                raise Exception("Invalid NEAR_ENV!")
            self._near_env = near_env
        else:
            raise Exception("Missing NEAR_ENV!")

        if self._near_env == "mainnet":
            self._rpc_url = "https://rpc.mainnet.near.org" if not os.getenv('NEAR_RPC_URL') else os.getenv('NEAR_RPC_URL')
            # self._rpc_url = "http://45.77.96.53:3030"
            self._burrow_contract = "contract.main.burrow.near"
            self._private_key = "" if not os.getenv('PRIVATE_KEY') else os.getenv('PRIVATE_KEY')
            self._deposit_yocto = 1
            self._priceoracle_contract = "priceoracle.near"
            self._near_contract = "wrap.near"
            self._signer_account_id = "juaner.near" if not os.getenv('SIGNER_ACCOUNT_ID') else os.getenv('SIGNER_ACCOUNT_ID')
            self._burrow_token = "token.burrow.near"
            self._ref_ex = "v2.ref-finance.near"
            self._pyth_oracle_contract_id = "pyth-oracle.near"
            self._nearx_token_contract_id = "v2-nearx.stader-labs.near"
            self._linear_token_contract_id = "linear-protocol.near"
            self._stnear_token_contract_id = "meta-pool.near"
        elif self._near_env == "testnet":
            self._rpc_url = "https://rpc.testnet.near.org" if not os.getenv('NEAR_RPC_URL') else os.getenv('NEAR_RPC_URL')
            self._burrow_contract = "contract.dev-burrow.testnet"
            self._private_key = "" if not os.getenv('PRIVATE_KEY') else os.getenv('PRIVATE_KEY')
            self._deposit_yocto = 1
            self._priceoracle_contract = "mock-priceoracle.testnet"
            self._near_contract = "wrap.testnet"
            self._signer_account_id = "juaner.testnet" if not os.getenv('SIGNER_ACCOUNT_ID') else os.getenv('SIGNER_ACCOUNT_ID')
            self._burrow_token = "token.dev-burrow.testnet"
            self._ref_ex = "exchange.ref-dev.testnet"
            self._pyth_oracle_contract_id = "pyth-oracle.testnet"
            self._nearx_token_contract_id = "v2-nearx.staderlabs.testnet"
            self._linear_token_contract_id = "linear-protocol.testnet"
            self._stnear_token_contract_id = "meta-v2.pool.testnet"
        else:
            raise Exception("Invalid NEAR_ENV!")

    @property
    def near_env(self):
        return self._near_env

    @property
    def rpc_url(self):
        return self._rpc_url

    @property
    def burrow_contract(self):
        return self._burrow_contract

    @property
    def private_key(self):
        return self._private_key

    @property
    def deposit_yocto(self):
        return self._deposit_yocto

    @property
    def priceoracle_contract(self):
        return self._priceoracle_contract

    @property
    def near_contract(self):
        return self._near_contract

    @property
    def signer_account_id(self):
        return self._signer_account_id

    @property
    def burrow_token(self):
        return self._burrow_token

    @property
    def ref_ex(self):
        return self._ref_ex

    @property
    def pyth_oracle_contract_id(self):
        return self._pyth_oracle_contract_id

    @property
    def nearx_token_contract_id(self):
        return self._nearx_token_contract_id

    @property
    def linear_token_contract_id(self):
        return self._linear_token_contract_id

    @property
    def stnear_token_contract_id(self):
        return self._stnear_token_contract_id
