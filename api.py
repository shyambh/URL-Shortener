import hashlib
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)


books = [
    {
        "id": 1,
        "title": "Fundamentals of Data Engineering",
        "author": "Joe Reis, Matt Housely",
    },
    {"id": 2, "title": "Tidy First", "author": "Kent Beck"},
]


def generate_hash(text: str, length: int):
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash[:length]


@app.route("/api/shortenurl/<string:url>", methods=["POST"])
def shorten_url(url):
    calculated_hash = generate_hash(url, 10)

    db_connection = mysql.connector.connect(
        user="testuser", password="admin", host="127.0.0.1", database="shorten_url"
    )
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
