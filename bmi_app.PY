from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>BMI CaLawdulator</title>
</head>
<body>
    <h2>BMI CaLawdulator</h2>
    <form id="bmiForm">
        Password: <input type="password" id="password"><br><br>
        Weight (kg): <input type="number" id="weight" step="any"><br><br>
        Height (cm): <input type="number" id="height" step="any"><br><br>
        <button type="button" onclick="calculateBMI()">Calculate BMI</button>
    </form>

    <h3 id="result"></h3>

    <script>
        function calculateBMI() {
            const pw = document.getElementById('password').value;
            if (pw !== "bebus69") {
                document.getElementById('result').innerHTML = "Incorrect password!";
                return;
            }

            const weight = document.getElementById('weight').value;
            const height = document.getElementById('height').value;

            fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ weight: weight, height: height })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML =
                    "BMI: " + data.bmi + "<br>Category: " + data.category;
            })
            .catch(error => {
                document.getElementById('result').innerHTML = "Error: " + error;
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/calculate", methods=["POST"])
def calculate_bmi():
    data = request.get_json()
    try:
        weight = float(data.get("weight", 0))
        height = float(data.get("height", 0)) / 100
        if height <= 0:
            return jsonify({"bmi": "Error", "category": "Invalid height"})
        bmi = round(weight / (height**2), 2)
        if bmi < 18.5:
            category = "Patli Gend, khana khale"
        elif bmi < 25:
            category = "Aaaaaht model maal sexy gend"
        elif bmi < 30:
            category = "Kitna khayega lawdeeeee mota madarchod"
        else:
            category = "iske baad ab sidha cardiac disease hai lawde khana ram khaaa , kaam zyada karle bhadveeeee mareeegaaa!!!!"
    except Exception as e:
        return jsonify({"bmi": "Error", "category": str(e)})
    return jsonify({"bmi": bmi, "category": category})

if __name__ == "__main__":
    app.run(debug=True)
