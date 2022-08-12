# -*- coding:utf-8 -*-

"""Currency"""

__author__ = "siznax"

import decimal
import requests

from flask import Flask, jsonify, abort


app = Flask(__name__)


@app.route("/rate/<string:cur1>/<string:cur2>")
def get_rate(cur1, cur2):
    """returns conversion rate from cur1 to cur2 as JSON response"""
    res = {"cur1": cur1, "cur2": cur2}
    res.update(api_rate(cur1, cur2))
    return jsonify(res)


@app.route("/value/<string:val>/<string:cur1>/<string:cur2>")
def get_value(val, cur1, cur2):
    """returns value of cur1 in cur2 at API conversion rate as JSON response"""

    decimal.getcontext().rounding = decimal.ROUND_HALF_UP  # EURO rounding

    try:
        dec = decimal.Decimal(val)
    except decimal.InvalidOperation:
        abort(404)

    rate = api_rate(cur1, cur2)[cur2]

    ans = dec * decimal.Decimal(rate)

    res = {"cur1": cur1, "cur2": cur2}
    res.update({
        "val1": str(dec.quantize(decimal.Decimal("1.00"))),
        "val2": str(ans.quantize(decimal.Decimal("1.00")))})

    return jsonify(res)


def api_rate(cur1, cur2):
    """returns conversion rate from API as json"""
    supported = ("usd", "gbp", "eur")

    cur1 = cur1.lower()
    cur2 = cur2.lower()

    if (cur1 not in supported) or (cur2 not in supported):
        abort(404)

    api = ("https://cdn.jsdelivr.net/gh/fawazahmed0/"
           "currency-api@1/latest/currencies/"
           f"{cur1}/{cur2}.json")

    return requests.get(api).json()
