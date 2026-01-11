from abc import ABC, abstractmethod

class LongTermMemoryStore(ABC):

    @abstractmethod
    def save(self, entry):
        pass

    @abstractmethod
    def query(self, filters=None):
        pass

    @abstractmethod
    def delete(self, entry_id):
        pass

    @abstractmethod
    def list_all(self):
        pass
