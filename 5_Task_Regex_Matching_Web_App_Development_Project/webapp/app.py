# Inside app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import secrets  # Import the secrets module for generating a secure secret key
import re

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Disable Flask's session management
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Set a secret key for CSRF protection

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Check CSRF token before processing the form data
        if request.form.get("csrf_token") != session.get("csrf_token"):
            return "CSRF Token Invalid"

        test_string = request.form.get("test_string")
        regex_pattern = request.form.get("regex_pattern")
        matched_strings = perform_regex_matching(test_string, regex_pattern)

        # Redirect to the results page with the matched strings
        return redirect(url_for("results",
                                test_string=test_string,
                                regex_pattern=regex_pattern,
                                matched_strings=",".join(matched_strings)))

    # Generate a new CSRF token for each request
    session["csrf_token"] = secrets.token_hex(16)

    return render_template("index.html", csrf_token=session["csrf_token"])

# Route for displaying results
@app.route("/results")
def results():
    test_string = request.args.get("test_string")
    regex_pattern = request.args.get("regex_pattern")
    matched_strings = request.args.get("matched_strings").split(",")  # Split the matched strings into a list

    return render_template("results.html",
                           test_string=test_string,
                           regex_pattern=regex_pattern,
                           matched_strings=matched_strings)

# Function to perform regex matching
def perform_regex_matching(test_string, regex_pattern):
    import re
    matches = re.findall(regex_pattern, test_string)
    return matches
# Route for email validation
@app.route("/validate_email", methods=["POST"])
def validate_email():
    if request.method == "POST":
        email = request.form.get("email")

        # Perform basic email validation (you can implement more sophisticated validation)
        is_valid = validate_email_format(email)

        # Return a JSON response indicating whether the email is valid
        return jsonify({"is_valid": is_valid})

# Function to perform basic email format validation
def validate_email_format(email):
    # Regular expression for a simple email format validation
    email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    return bool(re.match(email_pattern, email))

if __name__ == "__main__":
     # Set the host and port
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)
