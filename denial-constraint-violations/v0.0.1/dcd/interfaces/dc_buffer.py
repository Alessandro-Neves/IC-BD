from abc import ABC, abstractmethod

class IDCBuffer(ABC):
  @abstractmethod
  def __init__(self, constraints_file_path) -> None:
    raise NotImplementedError
  
  @abstractmethod
  def get_all(self) -> list[list[str]]:
    raise NotImplementedError
