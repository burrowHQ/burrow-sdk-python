#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
from burrow.burrow_handler import storage_balance_of, get_assets_paged_detailed, get_asset_farms_paged, get_account, \
    get_price_data, list_token_data, deposit, burrow, withdraw, repay_from_wallet, repay_from_supplied, \
    storage_deposit, near_withdraw, increase_collateral, decrease_collateral, send_message, account_stake_booster, \
    account_unstake_booster, account_farm_claim_all, health_factor, max_supply_balance, max_burrow_balance, \
    max_withdraw_balance, max_adjust_balance, max_repay_from_wallet, max_repay_from_account, account_apy, \
    supply_health_factor, burrow_health_factor, repay_from_account_health_factor, withdraw_health_factor
import logging
from burrow.tool_util import success, error, is_number
from burrow.circulating_supply import update_marketcap
from loguru import logger


service_version = "20240112.01"
Welcome = 'Welcome to burrow SDK API server, ' + service_version
app = Flask(__name__)


@app.route('/')
def hello_world():
    return Welcome


@app.route('/storage_balance_of', methods=['POST'])
def handle_storage_balance_of():
    try:
        request_data = request.get_json()
        account_id = request_data["account_id"]
        token_id = request_data["token_id"]
    except Exception as e:
        return error("The required field is empty", "1002")
    try:
        ret = storage_balance_of(account_id, token_id)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/storage_deposit', methods=['POST'])
def handle_storage_deposit():
    try:
        request_data = request.get_json()
        account_id = request_data["account_id"]
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    try:
        ret = storage_deposit(account_id, token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_assets_paged_detailed', methods=['GET'])
def handle_get_assets_paged():
    try:
        ret = get_assets_paged_detailed()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_asset_farms_paged', methods=['GET'])
def handle_get_asset_farms_paged():
    try:
        ret = get_asset_farms_paged()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_account/<account_id>', methods=['GET'])
def handle_get_account(account_id):
    try:
        ret = get_account(account_id)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/get_price_data', methods=['GET'])
def handle_get_price_data():
    try:
        ret = get_price_data()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/list_token_data', methods=['GET'])
def handle_list_token_dta():
    try:
        ret = list_token_data()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/supply', methods=['POST'])
def handle_supply():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        is_collateral = request_data["is_collateral"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "" or is_collateral is None or is_collateral == "":
        return error("The required field is empty", "1002")
    try:
        ret = deposit(token_id, amount, is_collateral)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/burrow', methods=['POST'])
def handle_burrow():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = burrow(token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/withdraw', methods=['POST'])
def handle_withdraw():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = withdraw(token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_wallet', methods=['POST'])
def handle_repay_from_wallet():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = repay_from_wallet(token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_supplied', methods=['POST'])
def handle_repay_from_supplied():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = repay_from_supplied(token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/near_withdraw', methods=['POST'])
def handle_near_withdraw():
    try:
        request_data = request.get_json()
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if amount is None or amount == "":
        return error("The required field is empty", "1002")
    try:
        ret = near_withdraw(amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/increase_collateral', methods=['POST'])
def handle_increase_collateral():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = increase_collateral(token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/decrease_collateral', methods=['POST'])
def handle_decrease_collateral():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = decrease_collateral(token_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/send_message', methods=['POST'])
def handle_send_message():
    try:
        request_data = request.get_json()
        message = request_data["message"]
        ret = send_message(message)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/v1/circulating-supply', methods=['GET'])
def handle_circulating_supply():
    try:
        ret = update_marketcap()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_stake_booster', methods=['POST'])
def handle_account_stake_booster():
    try:
        request_data = request.get_json()
        amount = request_data["amount"]
        duration = request_data["duration"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    try:
        ret = account_stake_booster(amount, duration)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_unstake_booster', methods=['POST'])
def handle_account_unstake_booster():
    try:
        ret = account_unstake_booster()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_farm_claim_all', methods=['POST'])
def handle_account_farm_claim_all():
    try:
        ret = account_farm_claim_all()
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/health_factor/<account_id>', methods=['GET'])
def handle_health_factor(account_id):
    try:
        ret = health_factor(account_id)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_supply_balance/<account_id>/<token>', methods=['GET'])
def handle_max_supply_balance(account_id, token):
    try:
        ret = max_supply_balance(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_burrow_balance/<account_id>/<token>', methods=['GET'])
def handle_max_burrow_balance(account_id, token):
    try:
        ret = max_burrow_balance(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_withdraw_balance/<account_id>/<token>', methods=['GET'])
def handle_max_withdraw_balance(account_id, token):
    try:
        ret = max_withdraw_balance(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_adjust_balance/<account_id>/<token>', methods=['GET'])
def handle_max_adjust_balance(account_id, token):
    try:
        ret = max_adjust_balance(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_repay_from_wallet/<account_id>/<token>', methods=['GET'])
def handle_max_repay_from_wallet(account_id, token):
    try:
        ret = max_repay_from_wallet(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/max_repay_from_account/<account_id>/<token>', methods=['GET'])
def handle_max_repay_from_account(account_id, token):
    try:
        ret = max_repay_from_account(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/account_apy/<account_id>/<token>', methods=['GET'])
def handle_account_apy(account_id, token):
    try:
        ret = account_apy(account_id, token)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/supply_health_factor', methods=['POST'])
def handle_supply_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        is_collateral = request_data["is_collateral"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "" or is_collateral is None or is_collateral == "":
        return error("The required field is empty", "1002")
    try:
        if is_collateral:
            ret = supply_health_factor(token_id, account_id, amount, True)
        else:
            ret = health_factor(account_id)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/burrow_health_factor', methods=['POST'])
def handle_burrow_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = burrow_health_factor(token_id, account_id, amount, True)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/increase_collateral_health_factor', methods=['POST'])
def handle_increase_collateral_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = supply_health_factor(token_id, account_id, amount, True)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/decrease_collateral_health_factor', methods=['POST'])
def handle_decrease_collateral_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = supply_health_factor(token_id, account_id, amount, False)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/withdraw_health_factor', methods=['POST'])
def handle_withdraw_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = withdraw_health_factor(token_id, account_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_wallet_health_factor', methods=['POST'])
def handle_repay_from_wallet_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = burrow_health_factor(token_id, account_id, amount, False)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


@app.route('/repay_from_account_health_factor', methods=['POST'])
def handle_repay_from_account_health_factor():
    try:
        request_data = request.get_json()
        token_id = request_data["token_id"]
        amount = request_data["amount"]
        account_id = request_data["account_id"]
        if not is_number(amount):
            return error("Amount Non numeric", "1003")
    except Exception as e:
        return error("The required field is empty", "1002")
    if token_id is None or token_id == "":
        return error("The required field is empty", "1002")
    try:
        ret = repay_from_account_health_factor(token_id, account_id, amount)
        return success(ret)
    except Exception as e:
        msg = str(e.args)
        return error(msg, "1001")


logger.add("burrow.log")
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.logger.info(Welcome)
    app.run(host='0.0.0.0', port=8100, debug=False)
