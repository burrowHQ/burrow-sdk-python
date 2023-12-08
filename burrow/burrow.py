import requests
import json
from loguru import logger
from contract_handler import BurrowHandler
import globals
from config import GlobalConfig

global_config = GlobalConfig()

signer = globals.get_signer_account(global_config.signer_account_id)


def multiply_decimals(decimals: int):
    return int("1" + "0" * decimals)


def handler_decimal(number, index):
    return ("{:.%sf}" % index).format(number)


def storage_balance_of(account_id, token_id):
    burrow_handler = BurrowHandler(signer, token_id)
    ret = burrow_handler.storage_balance_of(account_id)
    return ret


def storage_deposit(account_id, token_id, amount):
    burrow_handler = BurrowHandler(signer, token_id)
    ret = burrow_handler.storage_deposit(account_id, int(amount))
    logger.info("storage_deposit:{}", ret)
    return ret


def get_assets_paged_detailed():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_assets_paged_detailed()
    return ret


def get_asset_farms_paged():
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_asset_farms_paged()
    return ret


def get_account(account_id):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    ret = burrow_handler.get_account(account_id)
    return ret


def get_price_data():
    burrow_handler = BurrowHandler(signer, global_config.priceoracle_contract)
    ret = burrow_handler.get_price_data()
    return ret


def ft_metadata(account_id):
    burrow_handler = BurrowHandler(signer, account_id)
    ret = burrow_handler.ft_metadata()
    return ret


def get_price():
    url = "https://raw.githubusercontent.com/NearDeFi/token-prices/main/ref-prices.json"
    requests.packages.urllib3.disable_warnings()
    ret = requests.get(url=url, verify=False)
    price_data = json.loads(ret.text)
    return price_data


def handle_token_price(price_data_list):
    token_price_data = {}
    price_list = get_price()
    for price_data in price_data_list["prices"]:
        price = price_data["price"]
        if price is None:
            continue
        token_metadata = ft_metadata(price_data["asset_id"])
        p = int(price["multiplier"]) / multiply_decimals((price["decimals"] - token_metadata["decimals"]))
        token_price_data[price_data["asset_id"]] = {"price": p, "symbol": token_metadata["symbol"],
                                                    "decimals": token_metadata["decimals"]}
    for key, value in price_list.items():
        token_price_data[key] = {"price": value["price"], "symbol": value["symbol"], "decimals": value["decimal"]}
    return token_price_data


def handle_extra_decimals():
    assets_data_list = get_assets_paged_detailed()
    extra_decimals = {}
    for assets_data in assets_data_list:
        extra_decimals[assets_data["token_id"]] = assets_data["config"]["extra_decimals"]
    return extra_decimals


def handle_supply_farm_apy(assets_data, token_price_data, extra_decimals):
    supply_farm_apy = "0.00"
    supplied = assets_data["supplied"]["balance"]
    farms = assets_data["farms"]
    token_id = assets_data["token_id"]
    for farm in farms:
        if "Supplied" in farm["farm_id"]:
            for k, v in farm["rewards"].items():
                decimals = token_price_data[k]["decimals"] + extra_decimals[k]
                r = (int(v["reward_per_day"]) / multiply_decimals(decimals)) * float(token_price_data[k]["price"])
                s_decimals = token_price_data[token_id]["decimals"] + extra_decimals[token_id]
                s = int(supplied) / multiply_decimals(s_decimals) * float(token_price_data[k]["price"])
                supply_farm_apy = handler_decimal((r * 365 / s) * 100, 2)
    return supply_farm_apy


def list_token_data():
    ret_data_list = []
    assets_data_list = get_assets_paged_detailed()
    extra_decimals = handle_extra_decimals()
    price_data_list = get_price_data()
    token_price_data = handle_token_price(price_data_list)
    ret_farm_data = {}
    farm_data_list = get_asset_farms_paged()
    for farm_data in farm_data_list:
        if "NetTvl" in farm_data:
            for farm in farm_data:
                if "NetTvl" == farm:
                    continue
                else:
                    farm_rewards = farm["rewards"]
                    for reward_token, farm_reward in farm_rewards.items():
                        ret_farm_data[reward_token] = {"reward_per_day": farm_reward["reward_per_day"],
                                                       "boosted_shares": farm_reward["boosted_shares"]}
    reward_per_day = (int(ret_farm_data["token.burrow.near"]["reward_per_day"]) / 1000000000000000000) * float(
        token_price_data["token.burrow.near"]["price"]) * 365
    boosted_shares = int(ret_farm_data["token.burrow.near"]["boosted_shares"]) / 1000000000000000000
    net_tvl_apy = reward_per_day / boosted_shares
    for assets_data in assets_data_list:
        token_id = assets_data["token_id"]
        if token_id not in token_price_data:
            continue
        total_supplied_balance = int(assets_data["supplied"]["balance"]) + int(assets_data["reserved"]) + int(
            assets_data["prot_fee"])
        token_decimals = token_price_data[token_id]["decimals"] + assets_data["config"]["extra_decimals"]
        total_supplied_balance = handler_decimal(total_supplied_balance / multiply_decimals(token_decimals), 6)
        total_burrow_balance = handler_decimal(
            int(assets_data["borrowed"]["balance"]) / multiply_decimals(token_decimals), 6)
        borrow_apy = "0.00"
        can_borrow = assets_data["config"]["can_borrow"]
        if can_borrow:
            borrow_apy = handler_decimal(float(assets_data["borrow_apr"]) * 100, 2)
        net_tvl_multiplier = assets_data["config"]["net_tvl_multiplier"]
        if net_tvl_multiplier != 0:
            net_tvl_multiplier = net_tvl_multiplier / 10000
        available_liquidity = float(total_supplied_balance) - float(total_burrow_balance)
        supply_farm_apy = handle_supply_farm_apy(assets_data, token_price_data, extra_decimals)
        ret_data = {
            "token": token_id,
            "symbol": token_price_data[token_id]["symbol"],
            "price": token_price_data[token_id]["price"],
            "base_apy": handler_decimal(float(assets_data["supply_apr"]) * 100, 2),
            "net_liquidity_apy": handler_decimal(float(net_tvl_apy * net_tvl_multiplier) * 100, 2),
            "supply_farm_apy": supply_farm_apy,
            "borrow_apy": borrow_apy,
            "supply_apy": handler_decimal(
                float(assets_data["supply_apr"]) * 100 + float(net_tvl_apy * net_tvl_multiplier) * 100 + float(
                    supply_farm_apy), 2),
            "total_supplied_balance": total_supplied_balance,
            "total_supplied_price": handler_decimal(
                float(total_supplied_balance) * float(token_price_data[token_id]["price"]), 6),
            "total_burrow_balance": total_burrow_balance,
            "total_burrow_price": handler_decimal(
                float(total_burrow_balance) * float(token_price_data[token_id]["price"]), 6),
            "available_liquidity_balance": handler_decimal(available_liquidity - available_liquidity * 0.001, 6),
            "available_liquidity_price": handler_decimal(
                (available_liquidity - available_liquidity * 0.001) * float(token_price_data[token_id]["price"]), 6)
        }
        ret_data_list.append(ret_data)
    return ret_data_list


def deposit(token_id, amount, is_collateral):
    burrow_handler = BurrowHandler(signer, token_id)
    if is_collateral:
        extra_decimals = handle_extra_decimals()
        max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
        ret = burrow_handler.deposit_collateral(amount, max_amount)
        logger.info("deposit_collateral:{}", ret)
    else:
        ret = burrow_handler.deposit(amount)
        logger.info("deposit:{}", ret)
    return ret


def burrow(token_id, amount):
    burrow_handler = BurrowHandler(signer, token_id)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.burrow(max_amount)
    logger.info("burrow:{}", ret)
    return ret


def withdraw(token_id, amount):
    burrow_handler = BurrowHandler(signer, token_id)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.withdraw(max_amount)
    return ret


def repay_from_wallet(token_id, amount):
    burrow_handler = BurrowHandler(signer, token_id)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.repay_from_wallet(amount, max_amount)
    logger.info("repay_from_wallet:{}", ret)
    return ret


def repay_from_supplied(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.repay_from_supplied(max_amount, token_id)
    logger.info("repay_from_supplied:{}", ret)
    return ret


def near_withdraw(amount):
    burrow_handler = BurrowHandler(signer, global_config.near_contract)
    ret = burrow_handler.near_withdraw(amount)
    logger.info("repay_from_wallet:{}", ret)
    return ret


def increase_collateral(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.burrow_contract)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.increase_collateral(token_id, max_amount)
    logger.info("increase_collateral:{}", ret)
    return ret


def decrease_collateral(token_id, amount):
    burrow_handler = BurrowHandler(signer, global_config.priceoracle_contract)
    extra_decimals = handle_extra_decimals()
    max_amount = str(int(amount) * multiply_decimals(extra_decimals[token_id]))
    ret = burrow_handler.decrease_collateral(token_id, max_amount)
    logger.info("decrease_collateral:{}", ret)
    return ret


def get_assets():
    burrow_handler = BurrowHandler(signer, global_config.priceoracle_contract)
    ret = burrow_handler.get_assets()
    return ret


def send_message(message):
    url = "http://127.0.0.1:8400/api/message/send"
    requests.packages.urllib3.disable_warnings()
    json_p = {
        "content": json.dumps(message),
        "product": "oracle",
        "level": "medium",
        "email": True,
        "telegram": True,
        "slack": True,
        "type": "alert"
    }
    ret_message = requests.post(url=url, verify=False, json=json_p).content
    ret_message = json.loads(ret_message)
    print("ret_message:", ret_message)
    return ret_message


logger.add("burrow.log")
if __name__ == "__main__":
    print("############START###########")
    a = [{"alarmType":"PRICE_ZERO","source":"coingecko","coin":"wrap.near","extraMsg":"{\"coingecko\":0,\"binance\":1.928,\"binanceFutures\":1.93,\"huobi\":1.9295,\"cryptocom\":null,\"kucoin\":1.9293,\"gate\":1.928,\"chainlink\":0}","startTime":"2023-11-21T07:14:49.374Z"}]
    b = json.dumps(a)
    print(b)
