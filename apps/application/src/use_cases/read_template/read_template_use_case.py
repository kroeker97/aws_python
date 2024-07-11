from ...accessor.template.template_accessor import TemplateAccessor

class ReadTemplateUseCase:
  def __init__(self, template_accessor: TemplateAccessor):
    self.template_accessor = template_accessor

  def read_template(self, name: str):
    return self.template_accessor.read_template(name)