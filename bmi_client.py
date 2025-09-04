from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML Template
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Doctor Pro's BMI Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f5f5f5; }
        h1 { color: #2c3e50; }
        form { background: #fff; padding: 20px; border-radius: 10px; width: 400px; }
        input, select { margin: 10px 0; padding: 8px; width: 100%; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #2c3e50; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #1a242f; }
        .result { margin-top: 20px; padding: 20px; background: #eafaf1; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>Doctor Pro's BMI Calculator</h1>
    <form method="post">
        <label>Age:</label>
        <input type="number" name="age" value="{{ request.form.get('age','') }}" required>
        
        <label>Gender:</label>
        <select name="gender" required>
            <option value="male" {% if request.form.get('gender') == 'male' %}selected{% endif %}>Male</option>
            <option value="female" {% if request.form.get('gender') == 'female' %}selected{% endif %}>Female</option>
        </select>
        
        <label>Lifestyle:</label>
        <select name="lifestyle" required>
            <option value="sedentary" {% if request.form.get('lifestyle') == 'sedentary' %}selected{% endif %}>Sedentary (little to no exercise)</option>
            <option value="light" {% if request.form.get('lifestyle') == 'light' %}selected{% endif %}>Lightly Active (light exercise/sports 1-3 days/week)</option>
            <option value="moderate" {% if request.form.get('lifestyle') == 'moderate' %}selected{% endif %}>Moderately Active (moderate exercise 3-5 days/week)</option>
            <option value="active" {% if request.form.get('lifestyle') == 'active' %}selected{% endif %}>Active (hard exercise 6-7 days/week)</option>
            <option value="very_active" {% if request.form.get('lifestyle') == 'very_active' %}selected{% endif %}>Very Active (physical job or intense exercise)</option>
        </select>
        
        <label>Height (cm):</label>
        <input type="number" name="height" step="0.1" value="{{ request.form.get('height','') }}" required>
        
        <label>Weight (kg):</label>
        <input type="number" name="weight" step="0.1" value="{{ request.form.get('weight','') }}" required>
        
        <button type="submit">Calculate</button>
    </form>

    {% if bmi %}
    <div class="result">
        <h2>Results:</h2>
        <p><b>BMI:</b> {{ bmi }} ({{ category }})</p>
        <p><b>Calories Required:</b> {{ calories }} kcal/day</p>
        <h3>Suggested Diet Plan:</h3>
        <p>{{ diet }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

# Function to classify BMI
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Function to calculate BMR & calorie needs
def calculate_calories(age, gender, weight, height, lifestyle):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    return int(bmr * activity_multipliers[lifestyle])

# Function to suggest diet plan
def diet_plan(category):
    if category == "Underweight":
        return "High-calorie diet: Include nuts, milkshakes, rice, potatoes, peanut butter, and frequent meals."
    elif category == "Normal weight":
        return "Balanced diet: Include fruits, vegetables, whole grains, lean protein, and healthy fats."
    elif category == "Overweight":
        return "Calorie-deficit diet: Focus on salads, lean protein, avoid sugary drinks, eat smaller portions."
    else:
        return "Strict weight-loss diet: High in fiber, lean proteins, avoid fried/junk food, focus on portion control."

@app.route("/", methods=["GET", "POST"])
def index():
    bmi = category = calories = diet = None

    if request.method == "POST":
        age = int(request.form["age"])
        gender = request.form["gender"]
        lifestyle = request.form["lifestyle"]
        height = float(request.form["height"])
        weight = float(request.form["weight"])

        # BMI Calculation
        bmi = round(weight / ((height/100) ** 2), 2)
        category = bmi_category(bmi)
        calories = calculate_calories(age, gender, weight, height, lifestyle)
        diet = diet_plan(category)

    return render_template_string(html, bmi=bmi, category=category, calories=calories, diet=diet, request=request)

if __name__ == "__main__":
    app.run(debug=True)
