from flask import Flask, render_template, request
app = Flask(__name__)


def convert(num):
    decimal = int(num)
    mappings = {1000: "M", 900: 'CM', 500: "D", 400: 'CD', 100: "C",
                90: 'XC', 50: "L", 40: 'XL', 10: "X", 9: 'IX', 5: "V", 4: 'IV', 1: "I"}
    result = ""
    for k, v in mappings.items():
        value = decimal // k
        result += v * value
        decimal %= k
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num = request.form.get("number")
        if not num.isdigit() or not (0 < int(num) < 4000):
            return render_template("index.html", not_valid=True, developer_name="codebenders")

        return render_template("result.html", number_decimal=num, developer_name="codebenders", number_roman=convert(num))
    else:
        return render_template("index.html", not_valid=False, developer_name="codebenders")


if __name__ == "__main__":
    app.run("0.0.0.0", port=80)
    # app.run(debug=True)
