import langchain.llms.base

from contphica.agents.debate_agent import DebateAgent
from os import environ

# from langchain.schema import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
# from gpt4_openai import GPT4OpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.memory import ConversationSummaryBufferMemory


class GptDebateAgent(DebateAgent):
    def __init__(self, api_key, prompt: langchain.BasePromptTemplate):
        llm: BaseChatModel = ChatOpenAI(openai_api_key=api_key)
        memory = ConversationSummaryBufferMemory(memory_key="chat_history",
                                                 return_messages=True,
                                                 llm=llm)
        super().__init__(llm=llm, memory=memory, prompt=prompt)