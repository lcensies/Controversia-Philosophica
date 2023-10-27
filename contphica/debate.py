from contphica.agents.gpt_agent import GptDebateAgent
from contphica.agents.debate_agent import DebateAgent
from typing import Type

class Debate:

    _initiator: DebateAgent = None
    _responder: DebateAgent = None

    _initiator_model: Type[DebateAgent] = GptDebateAgent
    _responder_model: Type[DebateAgent] = GptDebateAgent

    _initiator_name: str = "Socratease"
    _responder_name: str = "Confuncius"

    _limit: int 
    _question: str

    _prompt: str = None

    @property
    def limit(self):
        return self._limit

    @property
    def question(self):
        return self._question

    def __init__(self, question: str, limit: int = 2):
        self._question = question
        self._limit = limit

    def with_limit(self, limit: int):
        self._limit = limit
        return self
    
    def with_gpt_agents(self):
        self._initiator_model = GptDebateAgent
        self._responder_model = GptDebateAgent
        return self 

    def with_names(self, initiator_name: str, responder_name: str):
        self._initiator_name_ = initiator_name
        self._responder_name_ = responder_name
        return self

    def with_prompt(self, prompt: str):
        self.prompt_ = prompt
        return self

    def start(self):
        self._initiator = self._initiator_model() 
        self._responder = self._responder_model()

        last_message: str = self._question
        
        print(f"Topic: {last_message}")

        for i in range(self.limit):
            print(f"---------- Round {i + 1} ----------\n\n")
            
            last_message = self._initiator.generate_response(last_message)
            print(f"{self._initiator_name}: {last_message}")

            print('\n')

            last_message = self._responder.generate_response(last_message)
            print(f"{self._responder_name}: {last_message}")

            print('\n\n')

            