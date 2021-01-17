#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import logging

from flask import Flask, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/books/')
@swag_from("swagger/get_all_books.yml")
def get_all_books():
    """
    Return all books from database
    """
    return {}

@app.route('/books/', methods=["POST"])
@swag_from("swagger/create_new_book.yml")
def create_new_book():
    """
    Return all books from database
    """
    return {}

@app.route('/books/<book_id>')
@swag_from("swagger/get_book.yml")
def get_book(book_id):
    """
    Return single book based on book id
    """
    return {}

@app.route('/authors/')
@swag_from("swagger/get_all_authors.yml")
def get_all_authors():
    """
    Return all authors from database
    """
    return {}

@app.route('/authors/', methods=["POST"])
@swag_from("swagger/create_new_author.yml")
def create_new_author():
    """
    Return all authors from database
    """
    return {}

@app.route('/authors/<author_id>')
@swag_from("swagger/get_author.yml")
def get_author(author_id):
    """
    Return single author based on author id
    """
    return {}

# We only need this for local development.
if __name__ == '__main__':
    app.run()
