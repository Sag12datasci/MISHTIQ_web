# Scientific Calculator – Flask Web App

A Flask-based **scientific calculator API + web interface** that supports exact arithmetic using Python’s `Fraction`, advanced math functions, and human-friendly inputs like `square`, `²`, percentages, and trigonometry in **degrees**.

---

## ✨ Features

* **Exact arithmetic** using `fractions.Fraction` for precise results
* **Scientific functions**:

  * Trigonometry: `sin`, `cos`, `tan` (degrees)
  * Inverse trig: `asin`, `acos`, `atan` (returns degrees)
  * Roots: `sqrt`, `cbrt`
  * Logs: `ln` (natural), `log` (base 10)
  * Exponential: `e^(x)`
* **Smart input normalization**:

  * `x square`, `x²`, `x^2` → `x**2`
  * Percent `%` → `/100`
* **Step-style processing** for sum-of-squares expressions
* **JSON API** endpoint for calculations
* **CORS enabled** (usable from frontend apps)

---

## 🗂 Project Structure

```
project/
│── app.py                # Main Flask application
│── templates/
│   └── Geo.html          # Frontend UI
│── static/
│   └── Geo.css           # Stylesheet
│── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

* Python **3.8+**
* pip

### 2️⃣ Install Dependencies

```bash
pip install flask flask-cors
```

### 3️⃣ Run the App

Uncomment the last lines in `app.py`:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Then start the server:

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🔗 API Usage

### Endpoint

```
POST /calculate
```

### Request Body (JSON)

```json
{
  "expr": "(20.21-16.66) square + (21.02-16.66)² - (10.83-16.66) square / 3"
}
```

### Response Example

```json
{
  "steps": [["+", 12.60], ["+", 18.92], ["-", 33.98]],
  "decimal_chain": "12.60 + 18.92 - 33.98",
  "signed_sum": -2.46,
  "denominator": 9.0,
  "result_exact": "-41/156",
  "result_decimal": -0.264089
}
```

---

## 🧠 Expression Rules

* Trigonometric inputs are **in degrees**
* Inverse trigonometric outputs are **in degrees**
* Use `/` for division (last `/` is treated as denominator in sum-of-squares mode)
* Supported power formats:

  * `x square`
  * `x²`
  * `x^2`

---

## 🛡 Security Notes

* `eval()` is sandboxed:

  * `__builtins__` disabled
  * Only allowed math functions exposed

⚠️ **Do not deploy publicly without further hardening.**

---

## 📌 Example Expressions

```
(5 square + 4 square) / 3
sin(30) + cos(60)
ln(10) + log(100)
(20.21-16.66)² + (21.02-16.66)² - (10.83-16.66)² / 3²
```

---

## 📄 License

This project is for **educational and personal use**.

---

## 🙌 Author

Developed using **Flask + Python Fractions** for accurate scientific calculations.


