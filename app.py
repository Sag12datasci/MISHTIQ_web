from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from fractions import Fraction
import math
import re


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("Geo.html")



def to_fraction_expr(expr: str) -> str:
    """Convert all integers and decimals into Fraction('...') for exact arithmetic."""
    def repl(m):
        return f"Fraction('{m.group(0)}')"
    return re.sub(r'\b\d+\.\d+|\b\d+\b', repl, expr)


def normalize_expression(expr):

    expr = expr.replace("sin(", "sin(")
    expr = expr.replace("cos(", "cos(")
    expr = expr.replace("tan(", "tan(")

    # Inverse trig (returns degrees)
    expr = expr.replace("asin(", "asin(")
    expr = expr.replace("acos(", "acos(")
    expr = expr.replace("atan(", "atan(")

    # Roots
    expr = expr.replace("sqrt(", "sqrt(")
    expr = expr.replace("cbrt(", "cbrt(")

    # Logs
    expr = expr.replace("ln(", "ln(")
    expr = expr.replace("log(", "log(")

    # Exponential
    expr = expr.replace("e^(", "exp(")

    # Percent
    expr = expr.replace("%", "/100")


    return expr









def calculate(expr):
    expr = normalize_expression(expr)

    
    # ---- NORMALIZATION ----

    # 1. "x square" → "x**2"
    expr = re.sub(
        r'((?:\([^()]*\))|\b[a-zA-Z_]\w*|\b\d+)\s*square\b',
        r'\1**2',
        expr,
        flags=re.IGNORECASE
    )
    expr = re.sub(
        r'((?:\([^()]*\))|\b[a-zA-Z_]\w*|\b\d+)\s*square\b',
        r'\1**2',
        expr,
        flags=re.IGNORECASE
    )

 
    expr = expr.replace("²", "**2")

  
    expr = re.sub(r'(\([^()]*\))\s*2\b', r'\1**2', expr)

   
    expr = expr.replace("^", "**")

    raw = expr

   
    if "/" in raw:
        num_raw, den_raw = raw.rsplit("/", 1)
    else:
        num_raw, den_raw = raw, "1"

  
    if re.fullmatch(r'\s*\d+\s*', den_raw):
        den_raw = den_raw.strip() + "**2"

   
    
    terms = re.findall(
        r'([+-]?\s*(?:\([^()]*\)|\b[a-zA-Z_]\w*)\s*\*\*\s*2)',
        num_raw
    )

    
    if not terms:
        try:
            exact = eval(expr, {"__builtins__": {}}, {
                "math": math,
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "asin": lambda x: math.degrees(math.asin(x)),
                "acos": lambda x: math.degrees(math.acos(x)),
                "atan": lambda x: math.degrees(math.atan(x)),
                "sqrt": math.sqrt,
                "cbrt": lambda x: x**(1/3),
                "ln": math.log,
                "log": math.log10,
                "exp": math.exp
            })

            rounded = round(float(exact), 6)
            return {
                "steps": [],
                "result_exact": str(rounded),
                "result_decimal": rounded
            }
        except Exception as e:
            return {
                "steps": [],
                "result_exact": "Error",
                "result_decimal": "Error"
            }


    print("\nCalculator Output\n")

    values = []
    signed_sum = Fraction(0, 1)


    # ---- PROCESS EACH TERM ----
    for t in terms:
        s = t.lstrip()
        sign = "-" if s.startswith("-") else "+"
        clean = t.lstrip("+- ").strip()

        try:
            val = eval(
                to_fraction_expr(clean),
                {"Fraction": Fraction, "__builtins__": {}}
            )
        except Exception as e:
            print(f"Error evaluating {clean}: {e}")
            continue

        values.append((sign, val))
        signed_sum += (-val if sign == "-" else val)

        print(f"{clean.replace('**', '^')} = {val} ({float(val)})")


    # ---- PRINT BREAKDOWN ----
    print("-" * 32)

    #Print decimal_only chain like: + 2.25 - 0.5 + 1.0
    parts = []
    for i, (sign, v) in enumerate(values):
        dec = f"{float(v):.2f}"
        if i == 0:
            # First term keeps its natural sign
            parts.append(dec if sign == "+" else f"-{dec}")
        else:
            parts.append(f" {sign} {dec}")

    decimal_chain = "".join(parts)
    print(decimal_chain)

    print("-" * 32)

    # ---- DENOMINATOR ----
    try:
        den_val = eval(
            to_fraction_expr(den_raw),
            {"Fraction": Fraction, "__builtins__": {}}
        )
    except Exception as e:
        print(f"Error evaluating denominator {den_raw}: {e}")
        den_val = Fraction(1, 1)


    # ---- FINAL RESULT ----
    result = signed_sum / den_val


    return {
            "steps": [(sign, float(val)) for sign, val in values],
            "decimal_chain": decimal_chain,
            "signed_sum": float(signed_sum),
            "denominator": float(den_val),
            "result_exact": str(result),
            "result_decimal": float(result)
    }

@app.route("/calculate", methods=["POST"])
def api():
    data = request.json
    expr = data.get("expr", "")

    print("Received:", expr)

    return jsonify(calculate(expr))


# if __name__ == "__main__":
#     app.run(debug=True)
# #      app.run(host="0.0.0.0", port=5000, debug=True)

