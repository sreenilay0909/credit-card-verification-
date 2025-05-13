from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file and force key columns to string to avoid type issues
df = pd.read_csv('creditcard_data.csv', dtype={
    'name': str,
    'Card Number': str,
    'Security Code': str,
    'phone_number':str
})

print("CSV Columns:", df.columns)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    # Get form data
    name = request.form['name']
    card_number = request.form['card_number']
    security_code = request.form['security_code']
    phone_number = request.form['phone_number']


    # Debug prints: show form data
    print("\n=== Form Data ===")
    print(f"Name: {name}")
    print(f"Card Number: {card_number}")
    print(f"Security Code: {security_code}")
    print(f"Phone Number: {phone_number}")

    # Debug prints: show first 5 rows of CSV key columns
    print("\n=== First 5 rows of CSV ===")
    print(df[['name', 'Card Number', 'Security Code','phone_number']].head())

    # Perform the matching, using .strip() and .lower() for case-insensitive match
    match = df[
        (df['name'].str.strip().str.lower() == name.strip().lower()) &
        (df['Card Number'].str.strip() == card_number.strip()) &
        (df['Security Code'].str.strip() == security_code.strip()) &    
        (df['phone_number'].str.strip() == phone_number.strip())


    ]

    # Debug prints: show if match is found
    print("\n=== Match Found ===")
    print(match)

    if not match.empty:
        return render_template('success.html')
    else:
        error = 'Verification failed. Please check your details.'
        return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
