
import sys
import getopt
import requests
import json


def symbolSwitch(x):
    return {
        "$": "USD",
        "€": "EUR",
        "£": "GBP",
        "¥": "CNY",
    }.get(x, x)


def main(argv):

    opts, args = getopt.getopt(argv, "", ["amount=", "input_currency=", "output_currency="])
    output_currency_stated = False

    for opt, arg in opts:
        if opt == "--amount":
            amount = float(arg)
        elif opt == "--input_currency":
            input_currency = symbolSwitch(arg)
        elif opt == "--output_currency":
            output_currency = symbolSwitch(arg)
            output_currency_stated = True

    api_params = {"base": input_currency}

    if output_currency_stated:
        api_params["symbols"] = output_currency

    data = requests.get("http://api.fixer.io/latest", params=api_params)
    dataJ = json.loads(data.text)

    output_rates = {k: "%.2f" % round(float(v) * amount, 2) for k, v in dataJ["rates"].items()}

    output_final_json = {"input":
                            {"amount": "%.2f" % amount,
                             "currency": input_currency},
                         "output": output_rates}

    print(json.dumps(output_final_json, indent=4, sort_keys=True))


main(sys.argv[1:])
