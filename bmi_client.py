from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simple HTML form
HTML_FORM = """
<!doctype html>
<html lang="en">
  <head>
    <title>BMI Calculator</title>
  </head>
  <body>
    <h1>BMI Calculator</h1>
    <form method="post" action="/bmi">
      <label for="weight">Weight (kg):</label><br>
      <input type="number" step="0.1" id="weight" name="weight" required><br><br>

      <label for="height">Height (m):</label><br>
      <input type="number" step="0.01" id="height" name="height" required><br><br>

      <input type="submit" value="Calculate BMI">
    </form>
    {% if bmi %}
      <h2>Your BMI: {{ bmi }}</h2>
      <h3>Category: {{ category }}</h3>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM)

@app.route("/bmi", methods=["POST"])
def bmi():
    try:
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        return render_template_string(HTML_FORM, bmi=bmi, category=category)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Important: set host='0.0.0.0' so ngrok can forward traffic
    app.run(host="0.0.0.0", port=5000, debug=True)
