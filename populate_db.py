"""Populate PostgreSQL database by sending a POST request for each product in products.json."""

import json

from fastapi.testclient import TestClient

from hash_retail.main import app

client = TestClient(app)

with open("products.json", "r", encoding="utf-8") as input_file:
    json_array = json.load(input_file)

for json_dict in json_array:
    del json_dict["id"]

    create_product_url = app.url_path_for("create_product")
    client.post(url=create_product_url, json=json_dict)
