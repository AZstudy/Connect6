import abc

class AIAbstractClass(abc.ABC):
    @abc.abstractmethod
    def action(self, states):
        pass
