import re

from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

app = Flask(__name__)


@app.route('/is_bankrupt', methods=['POST'])
def example():
    return jsonify(is_bankrupt(request.json))


def is_bankrupt(request):
    try:
        el = {}
        x = 0
        for attribute in attributes:
            el[attribute] = request["data"][x]
            x += 1
        df = pd.DataFrame([el])
        nbyear = request["nbyear"]
        if 1 <= nbyear <= 5:
            if years[5 - nbyear].predict(df) == 0:
                return {"Bankrupt":False, "Information": f"The company will not go bankrupt in {nbyear} year."}
            else:
                return {"Bankrupt":True, "Information": f"The company will probably go bankrupt in {nbyear} year."}
        else:
            return {"Error": "nbyear 1 and 5"}
    except:
        return {"Error": "check your request"}


if __name__ == "__main__":
    years = []
    for x in range(1, 6):
        xgb = load(f'data/{x}year.joblib')
        years.append(xgb)
    attributes = []
    with open("data/attribute.txt", "r") as f:
        x = 1
        temp = f.read().splitlines()
        for line in temp:
            attributes.append(re.sub(r"X[0-9]{1,2}|\[|\]", "", line))
            x += 1

    app.run(debug=True)

import json

request = {"nbyear": 1,
           "data": [0.20055,
                    0.37951,
                    0.39641,
                    2.0472,
                    32.351,
                    0.38825,
                    0.24976,
                    1.3305,
                    1.1389,
                    0.50494,
                    0.24976,
                    0.6598,
                    0.1666,
                    0.24976,
                    497.42,
                    0.73378,
                    2.6349,
                    0.24976,
                    0.14942,
                    43.37,
                    1.2479,
                    0.21402,
                    0.11998,
                    0.47706,
                    0.50494,
                    0.60411,
                    1.4582,
                    1.7615,
                    5.9443,
                    0.11788,
                    0.14942,
                    94.14,
                    3.8772,
                    0.56393,
                    0.21402,
                    1.741,
                    593.27,
                    0.50591,
                    0.12804,
                    0.66295,
                    0.051402,
                    0.12804,
                    114.42,
                    71.05,
                    1.0097,
                    1.5225,
                    49.394,
                    0.1853,
                    0.11085,
                    2.042,
                    0.37854,
                    0.25792,
                    2.2437,
                    2.248,
                    348690.0,
                    0.12196,
                    0.39718,
                    0.87804,
                    0.001924,
                    8.416,
                    5.1372,
                    82.658,
                    4.4158,
                    7.4277]}
# json_req = json.dumps(requests)
# json_req


request2={"nbyear": 1,
          "data": [0.080622,
 1.0208,
 0.13118,
 1.1542,
 -9.2273,
 -0.24848,
 0.080622,
 -0.02034,
 2.3527,
 -0.020763,
 0.082926,
 0.094766,
 0.037078,
 0.080622,
 4271.1,
 0.085457,
 0.97961,
 0.080622,
 0.034267,
 28.227,
 1.6757,
 0.082926,
 0.034267,
 -0.16781,
 -0.16791,
 0.085457,
 35.993,
 7.2508,
 3.6773,
 0.43301,
 0.034805,
 136.8,
 2.6708,
 2.2259,
 0.082705,
 2.3553,
 58.736,
 -0.007143,
 0.035153,
 0.010993,
 0.38002,
 0.035247,
 150.88,
 122.66,
 0.44311,
 0.22486,
 29.256,
 0.076313,
 0.032436,
 0.9619,
 0.85075,
 0.37479,
 -1.1477,
 -0.39484,
 624.0,
 0.035204,
 -3.883,
 0.96474,
 -0.65597,
 12.931,
 2.9758,
 131.98,
 2.7655,
 130.05,
 1.0] }
json.dumps(request2)
