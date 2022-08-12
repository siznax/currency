# -*- coding:utf-8 -*-

"""Currency"""

__author__ = "siznax"

import decimal
import requests

from flask import Flask, jsonify, abort


app = Flask(__name__)


@app.route("/hello")
def hello():
    """Simple example of an API endpoint"""
    return jsonify({"message": "ohai"})


@app.route("/hello/<string:name>")
def hello_name(name: str):
    """Simple example using an URL parameter"""
    return jsonify({"message": f"ohai {name}"})


@app.route("/rate/<string:cur1>/<string:cur2>")
def get_rate(cur1, cur2):
    """returns conversion rate from cur1 to cur2"""
    res = {"cur1": cur1, "cur2": cur2}
    res.update(api_rate(cur1, cur2))
    return jsonify(res)


@app.route("/value/<string:cur1>/<string:cur2>/<string:val>")
def get_value(cur1, cur2, val):
    """returns value of cur2 in cur1 at API conversion rate"""

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
    """returns conversion rate from API as float"""
    supported = ("usd", "gbp", "eur")

    cur1 = cur1.lower()
    cur2 = cur2.lower()

    if (cur1 not in supported) or (cur2 not in supported):
        abort(404)

    api = ("https://cdn.jsdelivr.net/gh/fawazahmed0/"
           "currency-api@1/latest/currencies/"
           f"{cur1}/{cur2}.json")

    return requests.get(api).json()
