from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        review = request.form['review']
        if not review:
            message = "Please enter a review."
            return render_template('index.html', message=message)
        else:
            model = joblib.load("Models_1/logistic_regression.pkl")
            prediction = model.predict([review])[0]
            return render_template('output.html', prediction=prediction)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
