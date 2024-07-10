import sys
from project_paths import PROJECT_ROOT
sys.path.append(PROJECT_ROOT)
from application.src.controller.template_update_handler import templateUpdateHandlerPath
from application.src.accessor.template.template_accessor_factory import TemplateAccessorEnv
from aws_cdk import (
  NestedStack,
  RemovalPolicy,
  aws_lambda as lambda_,
  aws_apigateway as apigateway,
  CfnOutput,
  Duration,
  aws_dynamodb as dynamodb
)
from constructs import Construct

class ConnectStack(NestedStack):
  def __init__(self, scope: Construct, id: str, **kwargs) -> None:
    super().__init__(scope, id, **kwargs)
    self.table = self.create_table()
    self.template_updated_handler = self.create_lambda_handler()
    self.add_permission()
    self.api = self.create_api_gateway()
    self.add_resources()
    CfnOutput(self, 'ApiUrl', value=self.api.url, description='API Gateway URL')
  
  def create_table(self):
    table = dynamodb.Table(
      self, 'TemplateTable',
      partition_key= dynamodb.Attribute(
        name='partitionKey',
        type=dynamodb.AttributeType.STRING
      ),
      billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
      removal_policy=RemovalPolicy.DESTROY)
    return table

  def create_lambda_handler(self):
    environment_variables: TemplateAccessorEnv = {"TEMPLATE_TABLE_NAME": self.table.table_name}

    return lambda_.Function(self, 'TemplateUpdatedHandler',
      runtime = lambda_.Runtime.PYTHON_3_12,
      handler='template_update_handler.TemplateUpdateHandler.handle',
      code=lambda_.Code.from_asset(templateUpdateHandlerPath),
      timeout=Duration.seconds(10),
      environment=environment_variables)

  def create_api_gateway(self):
    return apigateway.RestApi(
      self, 'WhatsAppWebhookApi',
      rest_api_name='WhatsApp Webhook API',
      description='API for WhatsApp Business webhook'
    )
  
  def add_permission(self):
    self.table.grant_read_write_data(self.template_updated_handler)


  def add_resources(self):
    template_updated = self.api.root.add_resource('template-updated').add_method('POST', apigateway.LambdaIntegration(self.template_updated_handler))