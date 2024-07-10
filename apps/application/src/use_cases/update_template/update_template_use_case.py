from ...accessor.template.template_accessor import TemplateAccessor

class UpdateTemplateUseCase:
  def __init__(self, template_accessor: TemplateAccessor):
    self.template_accessor = template_accessor

  def update_template(self, body: dict):
    self.template_accessor.put_template('Test', body)