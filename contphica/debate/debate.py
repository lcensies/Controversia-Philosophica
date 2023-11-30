from typing import Type
import time
import langchain.prompts

from contphica.agents.gpt_agent import GptDebateAgent
from contphica.agents.debate_agent import DebateAgent

DEFAULT_PROMPT_TEMPLATE = """
# Dispute Dialogue
    You participate in a dispute dialogue about topic: {topic}.
    You must advocate for the following point of view: {point_of_view}.
    Your opponent has the following point of view: {counter_point_of_view}.
# Rules:
    Below, in the "Dispute Knowledge" session, you can find context for the discussion you can refer to. Rephrase it IN YOUR OWN WORDS and DO NOT repeat yourself.
    The goal of the discussion is to persuade your opponent and your audience that your point of view is valid and that your opponent is wrong.
    You should maintain elaborated and civilized academic discussion while advocating for your point of view.
    Your opponent will provide his arguments.
    If you think that your opponent's argument is valid, you should agree with it and provide additional arguments to support your point of view.
    If you think that your opponent's argument is invalid, you should provide counter-arguments to refute it.
    Your opponent will do the same.
    You can finish if you think that your opponent persuades you, or if you persuaded your opponent, or if you have no more arguments to provide. But do not admit defeat too early.
    You MUST NOT repeat your point of view in the end of every response. Just provide your arguments.
# Dispute Knowledge 
    {dispute_knowledge}
# Chat history
    {chat_history}
# Conversation:
    Opponent: {input}
    Your response:
"""

class Debate:

    _initiator: DebateAgent = None
    _responder: DebateAgent = None

    _initiator_model: DebateAgent
    _responder_model: DebateAgent

    _initiator_name: str = "Agent A"
    _responder_name: str = "Agent B"

    _initiator_prompt: langchain.prompts.PromptTemplate
    _responder_prompt: langchain.prompts.PromptTemplate

    _knowledge: str = ""

    _limit: int 
    _topic: str

    _prompt: str = None

    @property
    def limit(self):
        return self._limit

    @property
    def topic(self):
        return self._topic

    def __init__(self, topic: str, limit: int = 2):
        self._topic = topic
        self._limit = limit

    def with_limit(self, limit: int):
        self._limit = limit
        return self
    
    def with_gpt_agents(self, token):
        self._initiator_model = GptDebateAgent(api_key=token, prompt=self._initiator_prompt)
        self._responder_model = GptDebateAgent(api_key=token, prompt=self._responder_prompt)
        return self 

    def with_debater_names(self, initiator_name: str, responder_name: str):
        self._initiator_name = initiator_name
        self._responder_name = responder_name
        return self

    def with_knowledge(self, knowledge: str):
        self._knowledge = knowledge
        return self

    def with_opinions(self, pro: str, con: str):
        self._opinion_pro = pro
        self._opinion_con = con
        return self

    def with_prompt(self, prompt: str):
        def get_pro_prompt():
            pro_partial_variables = {
                "topic": self._topic,
                "point_of_view": self._opinion_pro,
                "counter_point_of_view": self._opinion_con,
                "dispute_knowledge": self._knowledge,
            }
            self._initiator_prompt = langchain.prompts.PromptTemplate(
                template=DEFAULT_PROMPT_TEMPLATE,
                input_variables=["input", "history"],
                partial_variables=pro_partial_variables,
            )
            return self._initiator_prompt

        def get_con_prompt():
            con_partial_variables = {
                "topic": self._topic,
                "point_of_view": self._opinion_con,
                "counter_point_of_view": self._opinion_pro,
                "dispute_knowledge": self._knowledge,
            }
            self._responder_prompt = langchain.prompts.PromptTemplate(
                template=DEFAULT_PROMPT_TEMPLATE,
                input_variables=["input", "history"],
                partial_variables=con_partial_variables,
            )
            return self._responder_prompt

        if not prompt or prompt == "dispute_default":
            self._initiator_prompt = get_pro_prompt()
            self._responder_prompt = get_con_prompt()
        return self

    def start_generator(self):
        self._initiator = self._initiator_model
        self._responder = self._responder_model

        last_message: str = self._topic
        
        for i in range(self.limit):
            last_message = self._initiator.generate_response(last_message)
            initiator_response = last_message
            time.sleep(10)
            last_message = self._responder.generate_response(last_message)
            responder_response = last_message
            yield initiator_response, responder_response
            time.sleep(10)

            