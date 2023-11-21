from abc import ABC,abstractmethod

class BaseAction(ABC):
    @abstractmethod
    def trigger_action(self,message_data:object):
        pass