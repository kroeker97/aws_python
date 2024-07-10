# template_update_handler.py
import os
from ..use_cases.update_template.update_template_use_case_factory import create_update_template_use_case

templateUpdateHandlerPath = os.path.dirname(__file__)

class TemplateUpdateHandler:
  def __init__(self):
    pass

  def handle(self, event, context):
    update_template_use_case = create_update_template_use_case()
    update_template_use_case.update_template(event)
    print("Test:", event, context)
    return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Hello World!"
        }
  