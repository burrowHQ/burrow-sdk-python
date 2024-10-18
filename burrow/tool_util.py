from decimal import Decimal


def success(data=None):
    ret = {
        "code": "0",
        "msg": "success",
        "data": data
    }
    return ret


def error(msg, code=None, data=None):
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return ret


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def sum_reducer(sum_r, a):
    return sum_r + a


def shrink_token(value, decimals, fixed=None):
    value_decimal = Decimal(str(value))
    decimals_power = Decimal(10) ** int(decimals)
    result = value_decimal / decimals_power
    if fixed is not None:
        return result.quantize(Decimal(10) ** -fixed)
    else:
        return float(result)


def to_usd(balance, asset):
    price = asset["price"]["usd"]
    if price:
        return float(shrink_token(balance, asset["metadata"]["decimals"] + asset["config"]["extra_decimals"]) * price)
    else:
        return 0


def transform_contract_assets(assets, metadata, prices, ref_prices):
    transformed_assets = {}
    for i, asset in enumerate(assets):
        # print("asset:", asset)
        price = next((p["price"] for p in prices.get("prices") if p.get("asset_id") == asset["token_id"]), None)
        if price is not None:
            usd = float(price.get("multiplier")) / 10 ** (price.get("decimals") - metadata[i]["decimals"])
            price_data = {**price}
        else:
            usd = None
            price_data = {}
        metadata[i].pop("icon", None)
        if usd is None:
            if asset["token_id"] in ref_prices:
                price_usd = float(ref_prices[asset["token_id"]].get("price"))
            else:
                price_usd = 0
        else:
            price_usd = usd
        price_data["usd"] = price_usd
        transformed_asset = {
            **asset,
            "token_id": asset["token_id"],
            "metadata": metadata[i],
            "price": price_data
        }
        transformed_assets[asset["token_id"]] = transformed_asset
    return transformed_assets


def get_total_balance(assets, source):
    total_balances = []
    for token_id, asset in assets.items():
        net_tvl_multiplier = asset["config"]["net_tvl_multiplier"] / 10000
        balance = to_usd(asset[source]["balance"], asset) * net_tvl_multiplier
        # if source == "supplied":
        #     reserved_balance = to_usd(asset["reserved"], asset) * net_tvl_multiplier
        #     balance += reserved_balance
        total_balances.append(balance)
    return sum(total_balances)


if __name__ == "__main__":
    print("############START###########")
