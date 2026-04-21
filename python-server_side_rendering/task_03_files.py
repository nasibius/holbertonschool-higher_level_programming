from flask import Flask, render_template, request
import json
import csv

app = Flask(__name__)


def read_json_products():
    with open("products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def read_csv_products():
    products = []
    with open("products.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(
                {
                    "id": int(row["id"]),
                    "name": row["name"],
                    "category": row["category"],
                    "price": float(row["price"]),
                }
            )
    return products


@app.route("/products")
def products():
    source = request.args.get("source", "").lower()
    product_id = request.args.get("id")
    error = None
    products_list = []

    if source == "json":
        products_list = read_json_products()
    elif source == "csv":
        products_list = read_csv_products()
    else:
        error = "Wrong source"
        return render_template("product_display.html", products=[], error=error)

    if product_id is not None:
        try:
            wanted_id = int(product_id)
            products_list = [p for p in products_list if int(p.get("id", -1)) == wanted_id]
            if not products_list:
                error = "Product not found"
        except ValueError:
            error = "Product not found"
            products_list = []

    return render_template("product_display.html", products=products_list, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
