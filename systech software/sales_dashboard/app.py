from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import matplotlib.pyplot as plt
import io
import base64
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'secret_key_for_demo'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Simulated credentials for login
users = {"admin": "password123", "user": "userpass"}


# Simulate sales data
products = ["AssetExpert", "EasyTDS", "EASYREPORTS", "myPDFSigner", "HRM THREAD"]
employees = ["Shanana", "Sindhu", "Sunny", "Shubham", "Nithan"]
months = [f"2024-{str(m).zfill(2)}" for m in range(1, 13)]

product_sales_data = [{"Product": p, "Month": m, "Sales": random.randint(100, 500)} 
                      for p in products for m in months]
employee_sales_data = [{"Employee": e, "Month": m, "Sales": random.randint(2000, 8000)} 
                       for e in employees for m in months]

df_product_sales = pd.DataFrame(product_sales_data)
df_employee_sales = pd.DataFrame(employee_sales_data)

# Helper function to convert plots to images
def plot_to_img(fig):
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username  # Set session
            print("Session set:", session["user"])  # Debug log
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials. Try again.")
    return render_template("login.html", error=None)


@app.route("/dashboard")
def dashboard():
    # is
    
    # Top 5 products by sales
    top_products = df_product_sales.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    top_products.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Top 5 Products")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    img_top_products = plot_to_img(fig)

    # Monthly sales trend
    monthly_sales = df_product_sales.groupby("Month")["Sales"].sum()
    fig, ax = plt.subplots()
    monthly_sales.plot(ax=ax, color="green")
    ax.set_title("Monthly Sales Trend")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    img_monthly_trend = plot_to_img(fig)

    # Employee sales summary
    employee_summary = df_employee_sales.groupby("Employee")["Sales"].sum().reset_index()

    return render_template("index.html", 
                           img_top_products=img_top_products, 
                           img_monthly_trend=img_monthly_trend, 
                           employee_summary=employee_summary.to_dict(orient="records"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
@app.route("/monthly")
def monthly():
  # Ensure the user is logged in
  # return redirect(url_for("login"))
    return render_template("monthly.html") 
@app.route("/product")
def product():
    if "user" not in session:  # Ensure the user is logged in
        return redirect(url_for("login"))
    return render_template("product.html")  # Ensure product.html exists


if __name__ == "__main__":
    app.run(debug=True)
  # Make sure login.html exists in the templates folder
 # Ensure monthly.html exists


