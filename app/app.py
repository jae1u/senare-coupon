import requests
from flask import Flask, request, render_template
import os
import time

app = Flask(__name__)

COUPON_FILE = os.path.join(os.path.dirname(__file__), "coupons.txt")
UID_COOLDOWNS = {}
COOLDOWN_SECONDS = 600


def load_coupons():
    if not os.path.exists(COUPON_FILE):
        return []
    with open(COUPON_FILE, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def redeem_coupon(UID, coupon_code):
    url = "https://coupon.netmarble.com/api/coupon"
    body = {
        "gameCode": "tskgb",
        "couponCode": coupon_code,
        "langCd": "KO_KR",
        "pid": UID,
    }
    try:
        res = requests.post(url, json=body, timeout=3)
        data = res.json()
        return data.get("errorMessage", "알 수 없는 오류")
    except Exception:
        return "알 수 없는 오류"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        UID = request.form.get("uid", "").strip()
        results = {}
        coupons = load_coupons()
        now = time.time()
        last_used = UID_COOLDOWNS.get(UID, 0)

        if not UID:
            return render_template("index.html", error="UID를 입력하세요.")

        if now - last_used < COOLDOWN_SECONDS:
            remain = int(COOLDOWN_SECONDS - (now - last_used))
            min_, sec = divmod(remain, 60)
            return render_template(
                "index.html", error=f"{min_}분 {sec}초 후에 다시 시도할 수 있습니다."
            )

        UID_COOLDOWNS[UID] = now

        for coupon in coupons:
            msg = redeem_coupon(UID, coupon)
            results[coupon] = msg
        return render_template("result.html", results=results)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
