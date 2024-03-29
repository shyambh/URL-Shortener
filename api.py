import hashlib
import os
import json

from werkzeug.exceptions import HTTPException
import utils.mysql_connection as mysql_connection
from flask import Flask, request, jsonify, abort, make_response
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


def generate_hash(text: str, length: int):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash[:length]


def make_db_connection():
    return mysql_connection.connect()


def execute_sql(sql: str, *args):
    db_connection = make_db_connection()


def check_if_hash_already_exists(url: str):
    pass


@app.route("/api/shortenurl", methods=["POST"])
def shorten_url():

    try:
        # Max size = 1 MB
        MAX_CONTENT_SIZE = 1 * 1024 * 1024

        content_length = request.headers.get("Content-Length", type=int)

        if content_length is None or content_length is 0:
            response = make_response("No content found", 411)
            abort(response)

        elif content_length > MAX_CONTENT_SIZE:
            response = make_response(
                "The payload size exceeds the max limit of 1 MB", 413
            )
            abort(response)

        elif len(request.get_json()) == 0:
            response = make_response("Long URL missing", 400)
            abort(response)

        elif len(request.get_json()["long_url"]) == 0:
            response = make_response("Long URL has an empty value", 400)
            abort(response)

        url = request.get_json()["long_url"]

        calculated_hash = generate_hash(url, 10)

        db_connection = make_db_connection()

        cursor = db_connection.cursor()
        add_url_query = """
            insert into shortened_urls (long_url, hash) values (%s,%s)
        """
        cursor.execute(add_url_query, (url, calculated_hash))

        db_connection.commit()

        cursor.close()
        db_connection.close()

        return jsonify({"url": f"http://localhost/{calculated_hash}"}), 200

    except HTTPException as e:
        return e

    except Exception as e:
        print(e)
        return "Hmm, looks like something's broken...", 500


if __name__ == "__main__":
    app.run(debug=True)
