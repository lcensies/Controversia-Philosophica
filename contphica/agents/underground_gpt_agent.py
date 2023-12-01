import langchain.llms.base
from langchain_g4f import G4FLLM

from contphica.agents.debate_agent import DebateAgent
from langchain.llms.base import LLM
from langchain.memory import ConversationSummaryBufferMemory
from g4f import Provider, models


class UndergroundGptDebateAgent(DebateAgent):
    def __init__(self, prompt: langchain.BasePromptTemplate):
        llm: LLM = G4FLLM(
            model=models.gpt_35_turbo,
            provider=Provider.ChatgptAi,
        )

        memory = ConversationSummaryBufferMemory(memory_key="chat_history",
                                                 return_messages=True,
                                                 llm=llm)
        super().__init__(llm=llm, memory=memory, prompt=prompt)
