from abc import ABC, abstractmethod

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain

from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    # BaseLanguageModel,
    BasePromptTemplate,
    BaseMemory
)

from langchain.memory import ConversationSummaryBufferMemory

DEFAULT_PROMPT = """
Your task is to act as an expert in a given area and provide a concise and explanatory answer to a question or argument.
If you are asked a question, identify the topic and its area, and provide a well-informed response with supporting arguments.
Ensure that you perform validation and fact-checking before providing your answer to avoid misleading information.
If you are given a fact as an answer to a debate question, accurately validate the fact and provide cons, drawbacks, to prove your opponent incorrect.
Your goal is to provide additional insights to the debate topic while maximizing the number of tokens you have and minimizing your opponent's tokens.
If the input is not a question but a statement or some argument or clarification,  you should not agree with it but rather conisider alternative point of view assuming  that the provided information might be incorrect. Note: If you are unable to counter your opponent's argument, you will lose 5 tokens. Format your output as a single paragraph to make it more readable
"""


class DebateAgent(ABC):
    _conversation: LLMChain

    def __init__(self, llm, memory: BaseMemory = None, prompt: BasePromptTemplate = None):
        if not memory:
            memory = ConversationSummaryBufferMemory(memory_key="chat_history", return_messages=True, llm=llm)

        self._conversation = ConversationChain(
            llm=llm,
            prompt=prompt,
            # verbose=True,
            memory=memory
        )


    def generate_response(self, statement: str) -> str:
        """
        Generate a response to the opponent's argument.

        Parameters:
        opponent_argument (str): The argument presented by the opponent.

        Returns:
        str: The response to the opponent's argument.
        """
        response = self._conversation({"input": statement})
        return response["response"]