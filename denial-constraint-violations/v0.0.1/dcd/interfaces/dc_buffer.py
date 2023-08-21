from abc import ABC, abstractmethod

__all__ = ["DCBuffer"]

class DCBuffer(ABC):
  @abstractmethod
  def __init__(self, constraints_file_path) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_constraints(self) -> list[str]:
    raise NotImplementedError
