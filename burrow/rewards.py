import sys
sys.path.append('../')
import asyncio
import requests
import json
from decimal import Decimal
from burrow_handler import ft_contract_call
from tool_util import transform_contract_assets, get_total_balance, shrink_token, sum_reducer, to_usd
from config import GlobalConfig

global_config = GlobalConfig()
token_list = ["usdt.tether-token.near", "17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1", "853d955acef822db058eb8505911ed77f175b99e.factory.bridge.near"]


async def async_ft_contract_call(method, args, contract_name=global_config.burrow_contract):
    loop_ = asyncio.get_event_loop()
    return await loop_.run_in_executor(None, ft_contract_call, method, args, contract_name)


async def get_assets():
    assets = ft_contract_call("get_assets_paged", {})
    # print("assets:", assets)
    token_ids = [id_ for id_, _ in assets]
    # print("token_ids:", token_ids)
    assets_detailed_coroutines = [async_ft_contract_call("get_asset", {"token_id": token_id}) for token_id in token_ids
                                  if not token_id.startswith('shadow_ref_')]
    assets_detailed = await asyncio.gather(*assets_detailed_coroutines)
    # print("assets_detailed:", assets_detailed)
    metadata = await asyncio.gather(*[async_ft_contract_call("ft_metadata", {}, token_id) for token_id in token_ids if
                                      not token_id.startswith('shadow_ref_')])
    # print("metadata:", metadata)
    config = ft_contract_call("get_config", {})
    # print("config:", config)
    prices = ft_contract_call("get_price_data", {}, config["oracle_account_id"])
    # print("prices:", prices)
    ref_prices = fetch_ref_prices("https://raw.githubusercontent.com/NearDeFi/token-prices/main/ref-prices.json")
    # print("ref_prices:", ref_prices)
    return transform_contract_assets(assets_detailed, metadata, prices, ref_prices)


def fetch_ref_prices(url):
    r = fetch(url)
    return json.loads(r)


def fetch(url):
    r = requests.get(url)
    return r.text


def uniq(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def get_decimals(assets, token_id):
    for asset in assets:
        if asset['token_id'] == token_id:
            return


async def get_net_liquidity_apy(assets):
    net_liquidity_farm = ft_contract_call('get_asset_farm', {'farm_id': 'NetTvl'})
    # print("net_liquidity_farm:", net_liquidity_farm)
    total_daily_net_liquidity_rewards = 0
    supplied = 0
    for reward_token_id, farm in net_liquidity_farm['rewards'].items():
        total_daily_net_liquidity_rewards += float(shrink_token(farm['reward_per_day'],
                                                                assets[reward_token_id]['metadata']['decimals'] +
                                                                assets[reward_token_id]['config']['extra_decimals']) *
                                                   assets[reward_token_id]['price']['usd'])
        supplied += float(shrink_token(farm['boosted_shares'], 18))
    # supplied = get_total_balance(assets, 'supplied')
    # borrowed = get_total_balance(assets, 'borrowed')

    total_protocol_liquidity = supplied
    net_liquidity_apy = ((total_daily_net_liquidity_rewards * 365) / total_protocol_liquidity) * 100

    reward_tokens = [reward_token_id for reward_token_id in net_liquidity_farm['rewards']]
    print("a:", total_daily_net_liquidity_rewards * 365)
    print("b:", total_protocol_liquidity)
    print("net_liquidity_apy:", net_liquidity_apy)
    return net_liquidity_apy, reward_tokens


async def get_rewards(assets):
    apy_reward_tvl, reward_tokens_tvl = await get_net_liquidity_apy(assets)

    rewards = []
    for token_id, asset in assets.items():
        apy_base = float(asset['supply_apr']) * 100
        apy_base_borrow = float(asset['borrow_apr']) * 100
        token_id = asset['token_id']
        total_supply_usd = to_usd(asset['supplied']['balance'], asset) + to_usd(asset['reserved'], asset)
        total_supply_usd = total_supply_usd if total_supply_usd > 0 else 0
        total_borrow_usd = to_usd(asset['borrowed']['balance'], asset)
        total_borrow_usd = total_borrow_usd if total_borrow_usd > 0 else 0

        supplied_farm_rewards = next(
            (farm['rewards'] for farm in asset['farms'] if farm['farm_id']['Supplied'] == token_id), {})

        reward_tokens = uniq(
            list(supplied_farm_rewards.keys()) + reward_tokens_tvl
        )

        apy_reward = sum(
            (
                float(reward['reward_per_day']) / (10 ** (assets[reward_token_id]['metadata']['decimals'] +
                                                          assets[reward_token_id]['config']['extra_decimals']))
                * 365
                * next((a.get('price', {}).get('usd', 0) for token_id, a in assets.items() if
                        a['token_id'] == reward_token_id), 0)
                / total_borrow_usd if total_borrow_usd != 0 else 0
                * 100
            )
            for reward_token_id, reward in supplied_farm_rewards.items()
        )

        borrowed_farm_rewards = next(
            (farm['rewards'] for farm in asset['farms'] if 'Borrowed' in farm['farm_id'] and farm['farm_id']['Borrowed'] == token_id), {})

        reward_tokens_borrow = list(borrowed_farm_rewards.keys())
        apy_reward_borrow = sum(
            (
                float(reward['reward_per_day']) / (10 ** (assets[reward_token_id]['metadata']['decimals'] +
                                                          assets[reward_token_id]['config']['extra_decimals']))
                * 365
                * next((a.get('price', {}).get('usd', 0) for token_id, a in assets.items() if a['token_id'] == reward_token_id), 0)
                / total_borrow_usd if total_borrow_usd != 0 else 0
                * 100
            )
            for reward_token_id, reward in borrowed_farm_rewards.items()
        )
        if asset['token_id'] in token_list:
            ret_apy_reward_tvl = apy_reward_tvl
        else:
            ret_apy_reward_tvl = 0.0
        rewards.append({
            'token_id': asset['token_id'],
            'chain': 'NEAR',
            'project': 'Burrow',
            'symbol': asset['metadata']['symbol'],
            'tvl_usd': total_supply_usd - total_borrow_usd,
            'apy_reward': apy_reward,
            'apy_reward_tvl': ret_apy_reward_tvl,
            'apy_base': apy_base,
            'reward_tokens': reward_tokens,
            'total_supply_usd': total_supply_usd,
            'total_borrow_usd': total_borrow_usd,
            'apy_base_borrow': apy_base_borrow,
            'apy_reward_borrow': apy_reward_borrow,
            'reward_tokens_borrow': reward_tokens_borrow,
            'ltv': asset['config']['volatility_ratio']
        })

    return rewards


async def get_rewards_data():
    assets_data = await get_assets()
    # print("assets_data:", assets_data)
    rewards_data = await get_rewards(assets_data)
    # print("rewards_data:", rewards_data)
    return rewards_data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_rewards_data())
    loop.close()
