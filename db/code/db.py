import boto3
import db.code.models as models
import os
import logging

from crhelper import CfnResource
from sqlalchemy import create_engine

db_cluster_arn = os.getenv('DB_CLUSTER_ARN')
secret_arn = os.getenv('DB_SECRET_ARN')
database_name = os.getenv('DB_NAME')

#sending responses to CloudFormation and providing exception,
#timeout trapping, and detailed configurable logging
helper = CfnResource(
    json_logging=False,
    log_level='WARNING',
    boto_level='CRITICAL'
)


def handler(event, context):
    helper(event, context)

# Create database if it does not exist
def create_db():
    rds_client = boto3.client('rds-data')
    DB_Exists = False

    # Check if DB database_exists
    sql = "SELECT datname FROM pg_database WHERE datistemplate = false"
    response = rds_client.execute_statement(
        resourceArn = db_cluster_arn,
        secretArn = secret_arn,
        database = 'postgres',
        sql = sql)

    for record in response['records']:
        if record[0]['stringValue'] == database_name:
            DB_Exists = True
            logging.info("Database already exists.")

    # Create Database
    if not DB_Exists:
        logging.info("Database not found, creating it.")
        sql = 'CREATE DATABASE ' + database_name
        response = rds_client.execute_statement(
            resourceArn = db_cluster_arn,
            secretArn = secret_arn,
            database = 'postgres',
            sql = sql)

# Create Tables
def create_tables():
    db_connection_string = 'postgresql+auroradataapi://:@/' + database_name
    engine = create_engine(
        db_connection_string,
        echo=True,
        connect_args=dict(aurora_cluster_arn=db_cluster_arn, secret_arn=secret_arn))
    models.create_tables(engine)


# Create Database and tables
@helper.create
def create(event, context):
    logging.info(event)
    logging.info("******** Starting DB Migration *********")
    create_db()
    create_tables()
    logging.info("******** DB Migration Completed *********")

@helper.update
def update(event, context):
    logging.info("******** DB Migration Update *********")
    logging.info(event)

@helper.delete
def delete(event, context):
    logging.info("******** DB Migration Completed delete *********")
    logging.info(event)
