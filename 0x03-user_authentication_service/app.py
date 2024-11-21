#!/usr/bin/env python3
""" Flask App
    Author: Yusuf Mustapha Opeyemi
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
