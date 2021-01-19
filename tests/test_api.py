#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from unittest.mock import patch, Mock

import requests
from flask import Flask
from flask_testing import LiveServerTestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from api.books_catalog_api import app
from api.models import create_tables

author_id = 1

class BooksCatalogAPITests(LiveServerTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10

        return app

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        self.db = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
        create_tables(engine)

    @patch("api.books_catalog_api.get_sqlalchemy_session")
    def test_root_path(self, mock_db):
        mock_db.__enter__.return_value = self.db
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_non_existing_path(self):
        response = app.test_client().get("/non-existing")
        self.assertEqual(response.status_code, 404)

    @patch("api.books_catalog_api.get_sqlalchemy_session")
    def test_create_author(self, mock_db):
        mock_db.__enter__.return_value = self.db
        response = app.test_client().post(
            "/authors/",
            json={
                'first_name': "Damian",
                'last_name': "Ziobro",
            }
        )
        print(f"DAMIAN: {response.data}")
        author_id = response.json.get('author_id')
        self.assertEqual(response.status_code, 200)

    @patch("api.books_catalog_api.get_sqlalchemy_session")
    def test_get_all_books_return(self, mock_db):
        mock_db.__enter__.return_value = self.db
        response = app.test_client().get("/books/")
        self.assertEqual(response.status_code, 200)

    @patch("api.books_catalog_api.get_sqlalchemy_session")
    def test_get_all_authors_return(self, mock_db):
        mock_db.__enter__.return_value = self.db
        response = app.test_client().get("/authors/")
        self.assertEqual(response.status_code, 200)


    #TODO - improve coverage
    #@patch("api.books_catalog_api.get_sqlalchemy_session")
    #def test_create_book(self, mock_db):
        #mock_db.__enter__.return_value = self.db
        #response = app.test_client().post(
            #"/books/",
            #json={
                #'title': "Test title",
                #'description': "test description",
                #'author_id': 1,
            #}
        #)
        #print(f"DAMIAN: {response.data}")
        #self.assertEqual(response.status_code, 200)

