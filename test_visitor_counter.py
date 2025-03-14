import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import json
from decimal import Decimal

sys.path.insert (0, os.path.abspath (os.path.dirname (__file__)))

from visitor_counter_function import lambda_handler

@patch ("visitor_counter_function.boto3.resource")
def test_lambda_handler_success (mock_dynamodb_resource):
    mock_table = MagicMock ()
    mock_dynamodb_resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {"Item": {"visit_count": 5}}

    mock_table.update_item.return_value = {}

    event = {"httpMethod": "GET"}
    response = lambda_handler (event, None)

    print ("\nLambda Response:", response)

    assert response ["statusCode"] == 200
    assert json.loads (response ["body"])["count"] == 6  

@patch ("visitor_counter_function.boto3.resource")
def test_lambda_handler_dynamodb_failure (mock_dynamodb_resource):
    mock_table = MagicMock ()
    mock_dynamodb_resource.return_value.Table.return_value = mock_table

    mock_table.get_item.side_effect = Exception ("DynamoDB error")

    event = {"httpMethod": "GET"}
    response = lambda_handler (event, None)

    print ("\nLambda Response:", response)

    assert response ["statusCode"] == 500
    assert "error" in json.loads (response ["body"])
