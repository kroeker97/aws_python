from .dynamodb_template_accessor import DynamodbTemplateAccessor

class DynamodbTemplateAccessorEnv:
  TEMPLATE_TABLE_NAME: str

def create_dynamodb_template_accessor(env: DynamodbTemplateAccessorEnv) -> DynamodbTemplateAccessor:
  return DynamodbTemplateAccessor(env.TEMPLATE_TABLE_NAME)