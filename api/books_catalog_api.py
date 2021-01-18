#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import logging

from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from util import get_sqlalchemy_session
from models import Author, Book

app = Flask(__name__)
swagger = Swagger(app)

#deliberately set as global variable in order to reduce Database connections
#in lambdas
global SESSION
SESSION = get_sqlalchemy_session()

@app.route('/books/')
@swag_from("swagger/get_all_books.yml")
def get_all_books():
    """
    Return all books from database
    """
    query = SESSION.query(Book).order_by("title")
    logging.info(f"GET book: {book}")
    books = []
    for book in query:
        books.append({
            "book_id": book.book_id,
            "title": book.title,
            "description": book.description,
            "author": book.author,
        })

    logging.info(f"GET all books: \n{books}")
    return jsonify(books)

@app.route('/books/', methods=["POST"])
@swag_from("swagger/create_new_book.yml")
def create_new_book():
    """
    Create new book in the database
    """
    title = request.json.get("title")
    description = request.json.get("description")
    author_id = request.json.get("author_id")

    if not title or not description or not author_id:
        return jsonify({'error': 'Please provide title, description, author_id in the body'}), 400

    query = SESSION.query(Author).filter_by(author_id=author_id)
    author = query.first()
    if not author:
        return jsonify({'error': f'Author with id {author_id} not found'}), 404

    book = Book(
        title=title,
        description=description,
        author=author,
    )
    SESSION.add(book)
    SESSION.commit()

    logging.info(f"POST book: {book}")

    return jsonify({
        "book_id": book.book_id,
        "title": book.title,
        "description": book.description,
        "author": book.author,
    })

@app.route('/books/<book_id>')
@swag_from("swagger/get_book.yml")
def get_book(book_id):
    """
    Return single book based on book id
    """
    query = SESSION.query(Book).filter_by(book_id=int(book_id))
    book = query.first()
    logging.info(f"GET book: {book}")
    if not book:
        return jsonify({'error': f'Book with id {book_id} not found'}), 404

    return jsonify({
        "book_id": book.book_id,
        "title": book.title,
        "description": book.description,
        "author": book.author,
    })

@app.route('/authors/')
@swag_from("swagger/get_all_authors.yml")
def get_all_authors():
    """
    Return all authors from database
    """
    query = SESSION.query(Author).order_by("last_name")
    authors = []
    for author in query:
        authors.append({
            "author_id": author.author_id,
            "first_name": author.first_name,
            "last_name": author.last_name,
        })

    logging.info(f"GET all authors: \n{authors}")
    return jsonify(authors)

@app.route('/authors/', methods=["POST"])
@swag_from("swagger/create_new_author.yml")
def create_new_author():
    """
    Create new author in the database
    """
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    if not first_name or not last_name:
        return jsonify({'error': 'Please provide first_name and last_name in the body'}), 400


    author = Author(first_name=first_name, last_name=last_name)
    SESSION.add(author)
    SESSION.commit()

    logging.info(f"POST author: {author}")

    return jsonify({
        "author_id": author.author_id,
        "first_name": author.first_name,
        "last_name": author.last_name,
    })

@app.route('/authors/<author_id>')
@swag_from("swagger/get_author.yml")
def get_author(author_id):
    """
    Return single author based on author id
    """
    query = SESSION.query(Author).filter_by(author_id=int(author_id))
    author = query.first()
    logging.info(f"GET author: {author}")
    if not author:
        return jsonify({'error': f'Author with id {author_id} not found'}), 404

    return jsonify({
        "author_id": author.author_id,
        "first_name": author.first_name,
        "last_name": author.last_name,
    })

# We only need this for local development.
if __name__ == '__main__':
    app.run()
