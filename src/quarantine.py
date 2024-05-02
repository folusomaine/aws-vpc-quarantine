import json
from aws_lambda_powertools.logging import Logger

logger = Logger()

def lambda_handler(event, context):
    # TODO implement
    logger.info(event)
    logger.info(context)
    logger.info("Hello from Lambda!")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
