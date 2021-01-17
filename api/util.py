#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 damian <damian@damian-desktop>
#
# Distributed under terms of the MIT license.

import os
import boto3
from sqlalchemy import create_engine

def get_account_id():
    """
    Return AccountId of current AWS account
    """
    return boto3.client('sts').get_caller_identity().get('Account')

def get_sqlalchemy_engine():

    account_id = get_account_id()
    region = os.getenv("region")
    env = os.getenv("ENV")
    db_name = os.getenv("db_name")

    cluster_arn = f"arn:aws:rds:{region}:{account_id}:cluster:{env}-simple-book-catalog-auroradbcluster-ewg3wz2s9f48"
    secret_arn = f"arn:aws:secretsmanager:{region}:{account_id}:secret:{env}-simple-book-catalog-AuroraClusterSecret-SQlHtO"

    engine = create_engine(f'postgresql+auroradataapi://:@/{db_name}',
                           echo=True,
                           connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))

    #TODO - remove me later
    with engine.connect() as conn:
        for result in conn.execute("select * from pg_catalog.pg_tables"):
            print(result)
    return engine
