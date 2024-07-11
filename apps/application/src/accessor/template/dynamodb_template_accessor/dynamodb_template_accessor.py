import boto3
from boto3.dynamodb.conditions import Key
from ..template_accessor import TemplateAccessor

class DynamodbTemplateAccessor(TemplateAccessor):
  def __init__(self, table_name):
    dynamodb = boto3.resource("dynamodb")
    self.table = dynamodb.Table(table_name)
  
  def read_template(self, name: str):
    response = self.table.query(
      KeyConditionExpression=Key('partitionKey').eq('Test')
    )
    if len(response.get('Items')) <= 0:
      return None
    
    data = response.get('Items')[0].get('data')
    
    return data
  
  def put_template(self, name: str, template: dict):
    return self.table.put_item(
      Item={
        'partitionKey': name,
        'data': template
      }
    )