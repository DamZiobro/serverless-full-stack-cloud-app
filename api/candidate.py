#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import json
import logging
import uuid
import os
import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("candidate")

def post_candidate(event, context):
    """
    POST candidate to DynamoDB
    """
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ.get('CANDIDATE_TABLE'))

    body = json.loads(event.get('body'))
    if body:
        body['id'] = str(uuid.uuid4())
        table.put_item(Item=body)

    resp = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    logger.warning(f"resp: {resp}")

    return resp

def get_candidate(event, context):
    """
    Get candidates from DynamoDB
    """
    dynamodb = boto3.client('dynamodb')
    paginator = dynamodb.get_paginator('scan')
    params = {"TableName": os.environ.get('CANDIDATE_TABLE')}

    items = []
    for page in paginator.paginate(**params):
        items.append(page['Items'])

    resp = {
        "statusCode": 200,
        "body": json.dumps(items)
    }
    logger.info(f"resp: {resp}")

    return resp


if __name__ == "__main__":
    post_candidate(None, None)
    get_candidate(None, None)
