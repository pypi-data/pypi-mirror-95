from abc import ABC, abstractmethod


class Game(ABC):

    @abstractmethod
    def play(self):
        pass