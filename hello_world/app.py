import json
import boto3
from decimal import Decimal

def lambda_handler (event, context):
    dynamodb = boto3.resource ("dynamodb")
    table = dynamodb.Table ("VisitorCount")

    try:
        response = table.get_item (Key = {"id": "counter"})
        count = int (response.get ("Item", {}).get ("visit_count", 0)) + 1

        table.update_item (
            Key = {"id": "counter"},
            UpdateExpression = "SET #c = :count",
            ExpressionAttributeNames = {"#c": "visit_count"},
            ExpressionAttributeValues = {":count": Decimal (count)}
        )

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps ({"count": count})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps ({"error": str(e)})
        }
