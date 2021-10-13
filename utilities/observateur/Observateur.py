from abc import abstractmethod

"""source : https://refactoring.guru/fr/design-patterns/observer/python/example"""


class Observer():
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject) -> None:
        """
        Receive update from subject.
        """
        pass
