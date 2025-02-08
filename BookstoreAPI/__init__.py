import azure.functions as func
import logging
import json
import os
from azure.cosmos import CosmosClient

from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT")
KEY = os.getenv("COSMOS_DB_KEY")
DATABASE_NAME = "books-db"
CONTAINER_NAME = "books"

print(f"ENDPOINT: {ENDPOINT}")
print(f"KEY: {KEY[:5]}********")

client = CosmosClient(ENDPOINT, KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request...")

    if req.method == "POST":
        book_data = req.get_json()
        container.create_item(body=book_data)
        return func.HttpResponse(json.dumps({"message": "Book added"}), status_code=201)

    if req.method == "GET":
        return func.HttpResponse("Hello from Bookstore API!", status_code=200)

    return func.HttpResponse("Invalid request", status_code=400)
