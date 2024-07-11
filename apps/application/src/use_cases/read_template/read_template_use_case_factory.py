from .read_template_use_case import ReadTemplateUseCase
from ...accessor.template.template_accessor_factory import TemplateAccessorEnv, create_template_accessor
import os


class ReadTemplateUseCaseEnv(TemplateAccessorEnv):
  pass

def create_read_template_use_case():
  template_accessor = create_template_accessor({"TEMPLATE_TABLE_NAME": os.environ['TEMPLATE_TABLE_NAME']})
  return ReadTemplateUseCase(template_accessor)