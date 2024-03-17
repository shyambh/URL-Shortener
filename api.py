import hashlib
import os
import mysql.connector
from flask import Flask, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


def generate_hash(text: str, length: int):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash[:length]


def make_db_connection():
    return mysql.connector.connect(os.getenv("MYSQL_CONNECTION_STRING"))


def execute_sql(sql: str, *args):
    db_connection = make_db_connection()


def check_if_hash_already_exists(url: str):
    pass


@app.route("/api/shortenurl/<string:url>", methods=["POST"])
def shorten_url(url):
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

    return jsonify({"url": f"http://localhost/{calculated_hash}"})


if __name__ == "__main__":
    app.run(debug=True)
