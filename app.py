#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
from burrow.burrow import storage_balance_of, get_assets_paged_detailed, get_asset_farms_paged, get_account, get_price_data, list_token_data, deposit, burrow, withdraw, repay_from_wallet, repay_from_supplied, storage_deposit, near_withdraw, increase_collateral, decrease_collateral, send_message
import logging
from burrow.tool_util import success, error


service_version = "202311121.01"
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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
        if not amount.isnumeric():
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


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.logger.info(Welcome)
    app.run(host='0.0.0.0', port=8100, debug=False)
