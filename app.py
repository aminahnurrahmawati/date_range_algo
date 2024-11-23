from flask import Flask, jsonify, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# TRansaction Date Simulation
CSV_FILE = "transactions.csv"
if not os.path.exists(CSV_FILE):
    data = {
        "transaction_id": [1, 2, 3, 4, 5],
        "date": ["2024-11-20", "2024-11-21", "2024-11-22", "2024-11-23", "2024-11-24"],
        "amount": [100, 200, 150, 300, 250],
        "description": ["Purchase A", "Purchase B", "Purchase C", "Purchase D", "Purchase E"]
    }
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)

# Route for main page
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint to get transaction based on date range
@app.route("/transactions", methods=["GET"])
def get_transactions():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        return jsonify({"error": "Start date and end date are required"}), 400

    df = pd.read_csv(CSV_FILE)
    df["date"] = pd.to_datetime(df["date"])

    filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    return jsonify(filtered.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
