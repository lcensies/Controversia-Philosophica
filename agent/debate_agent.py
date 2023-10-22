from abc import ABC, abstractmethod


class DebateAgent(ABC):
    """
    Abstract base class for debating agents.

    This class defines the interface for agents participating in a debate. Subclasses should implement the
    following methods:
    
    - `select_topic`: Select a debate topic.
    - `reset_context`: Reset the context for the debate.
    - `generate_response`: Generate a response to the opponent's argument.

    Attributes:
    None

    Methods:
    - `select_topic(topic)`: Abstract method to select a debate topic.
    - `reset_context()`: Abstract method to reset the context for the debate.
    - `generate_response(opponent_argument)`: Abstract method to generate a response to the opponent's argument.
    """


    @abstractmethod
    def select_topic(self, topic: str):
        """
        Select a debate topic.

        Parameters:
        topic (str): The topic of the debate.

        Returns:
        None
        """
        pass

    @abstractmethod
    def reset_context(self):
        """
        Reset the context for the debate.

        Returns:
        None
        """
        pass

    @abstractmethod
    def generate_response(self, opponent_argument: str):
        """
        Generate a response to the opponent's argument.

        Parameters:
        opponent_argument (str): The argument presented by the opponent.

        Returns:
        str: The response to the opponent's argument.
        """
        pass