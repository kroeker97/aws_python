from .update_template_use_case import UpdateTemplateUseCase
from ...accessor.template.template_accessor_factory import TemplateAccessorEnv, create_template_accessor
import os


class UpdateTemplateUseCaseEnv(TemplateAccessorEnv):
  pass

def create_update_template_use_case():
  template_accessor = create_template_accessor({"TEMPLATE_TABLE_NAME": os.environ['TEMPLATE_TABLE_NAME']})
  return UpdateTemplateUseCase(template_accessor)