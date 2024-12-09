from flask import Flask, render_template, request
import re

app = Flask(__name__)

def evaluate_password_strength(password):
    """
    Evaluates the strength of a password based on various criteria.
    """
    length = len(password)
    criteria_met = 0

    # Define criteria for password strength
    criteria = {
        "Length >= 8 characters": length >= 8,
        "Contains uppercase letters": bool(re.search(r'[A-Z]', password)),
        "Contains lowercase letters": bool(re.search(r'[a-z]', password)),
        "Contains digits": bool(re.search(r'\d', password)),
        "Contains special characters": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        "No spaces": not bool(re.search(r'\s', password))
    }

    # Check criteria
    for _, passed in criteria.items():
        if passed:
            criteria_met += 1

    # Assign a strength score
    if criteria_met == len(criteria):
        strength = "Strong"
    elif criteria_met >= len(criteria) - 2:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, criteria

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password")
        strength, criteria = evaluate_password_strength(password)
        return render_template("index.html", password=password, strength=strength, criteria=criteria)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
