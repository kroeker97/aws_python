import boto3
from ..template_accessor import TemplateAccessor

class DynamodbTemplateAccessor(TemplateAccessor):
  def __init__(self, table_name):
    dynamodb = boto3.resource("dynamodb")
    self.table = dynamodb.Table(table_name)
  
  def read_template(self, name: str):
    return super().read_template(name)
  
  def put_template(self, name: str, template: dict):
    return super().put_template(name, template)