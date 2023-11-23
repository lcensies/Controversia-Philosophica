from contphica.agents.debate_agent import DebateAgent
from os import environ

# from langchain.schema import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
# from gpt4_openai import GPT4OpenAI
from langchain.memory import ConversationSummaryBufferMemory


#boilerplate code
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

hf = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    device = 0,
    pipeline_kwargs={"max_new_tokens": 1000},
)
DEFAULT_LLM = hf
#end of boilerplate
pipe = HuggingFacePipeline(pipeline =hf_pipe)

class GptDebateAgent(DebateAgent):

    def __init__(self, prompt: str = None):
        llm = DEFAULT_LLM
        # llm = GPT4OpenAI(token=environ.get("OPENAPI_SESSION_TOKEN"))
        memory = ConversationSummaryBufferMemory(memory_key="chat_history",return_messages=True, llm=llm)
        super().__init__(llm=llm, memory=memory, prompt=prompt)