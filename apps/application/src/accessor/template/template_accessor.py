from abc import ABC, abstractmethod

class TemplateAccessor(ABC):
  @abstractmethod
  def put_template(self, name: str, template: dict):
    pass

  @abstractmethod
  def read_template(self, name: str):
    pass