#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import unittest
from unittest.mock import patch, MagicMock

from api import candidate

class TestHelloModule(unittest.TestCase):

    @patch("boto3.resource")
    @patch("json.loads")
    def test_postCandidate_returns_success(self, json_mock, boto3_mock):
        boto3_mock.Table.return_value = None 
        json_mock.return_value = {}
        result = candidate.post_candidate({}, None)
        json_mock.assert_called_once()

    @patch("boto3.client")
    @patch("json.dumps")
    def test_getCandidate_returns_success(self, json_mock, boto3_mock):
        mock_paginator = MagicMock()
        boto3_mock.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value = []
        result = candidate.get_candidate("test", None)
        json_mock.assert_called_once_with([])
