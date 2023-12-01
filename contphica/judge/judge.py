from string import Template
from typing import Union

from langchain.chains import LLMChain
from langchain.llms.base import LLM
from langchain.prompts import Prompt, PromptTemplate
from langchain_g4f import G4FLLM
from g4f import models, Provider

# Prompt adopted from https://github.com/baaivision/JudgeLM/blob/main/judgelm/serve/gradio_web_server_judgelm.py
# With enhancements
SYSTEM_TEMPLATE = " [System]\n {sys_prompt} \n\n [Reference Answer]\n {reference} \n\n [Question]\n {topic} \n\n [Previous judgement] {previous_judgement} \n\n[The Start of Agent 1's Answer]\n {answer_1}\n\n[The End of Agent 1's  Answer]\n\n[The Start of Agent 2's Answer]\n {answer_2} \n\n[The End of Agent 2's Answer]\n\n"

SYSTEM_PROMPT = """You are Iudex - the most xobjective and accurate judge and evaluator of AI agents. \n
Evaluate two AI agents' performance in competitive debates on user question below. 
Rate their responses for helpfulness, relevance, accuracy, and level of detail on a scale of 1 to 10.
If section [Previous judgement] is present in question, use it as additional context formed from your previous observations.
Scores from previous judgements should be accumulated with current and might exceed 10. 
Provide two scores (Agent 1 and Agent 2) on one line, then give an unbiased explanation of your evaluation
on the next line, ensuring response order doesn't influence your judgment.
"""

REFERENCE = """
7 9
Agent 1’s answer is accurate and relevant to the question, but it lacks depth and detail. It correctly states that modern AI models can process large amounts of data and make predictions or decisions based on that data, which is a form of intelligence. However, it fails to address the nuances of understanding, which is a complex concept that goes beyond mere data processing.

On the other hand, Agent 2’s answer is more detailed and nuanced. It correctly points out that while modern AI models can process and analyze vast amounts of data, this does not necessarily mean that they have understanding. It further explains that understanding requires a deeper level of comprehension and knowledge that AI models currently lack. This answer provides a more comprehensive response to the question, hence the higher score.
"""

DEFAULT_JUDGE_LLM: LLM = G4FLLM(
    model=models.gpt_35_turbo,
    provider=Provider.GeekGpt,
)


class Judge:
    _prompt: Union[Prompt, str]
    _reference: str
    _model: LLM

    def __init__(self, model: LLM = DEFAULT_JUDGE_LLM,
                 prompt: Union[Prompt, str] = SYSTEM_PROMPT,
                 reference: str = REFERENCE):
        self._model = model
        self._prompt = prompt
        self._reference = reference

    # TODO: replace previous judgement with llmchain

    async def async_evaluate(self,
                             topic: str,
                             initiator_answer: str,
                             responder_answer: str,
                             previous_judgement: str) -> str:
        # TODO: switch to llmchains if possible (currenly there is a problem
        # with template substitution)
        # formatted = Template(SYSTEM_TEMPLATE).safe_substitute(question=question,
        #                                                       answer_1=initiator_answer,
        #                                                       answer_2=responder_answer,
        #                                                       prompt=self._prompt,
        #                                                       reference=REFERENCE,
        #                                                       previous_judgement=previous_judgement)
        #
        # res: str = self._model(formatted)
        #
        prompt = PromptTemplate(
            input_variables=["sys_prompt", "topic", "reference", "previous_judgement", "answer_1", "answer_2"],
            template=SYSTEM_TEMPLATE,
        )
        chain = LLMChain(llm=self._model, prompt=prompt)

        res = await chain.arun(sys_prompt=SYSTEM_PROMPT,
                               topic=topic,
                               reference=REFERENCE,
                               previous_judgement=previous_judgement,
                               answer_1=initiator_answer,
                               answer_2=responder_answer)

        return res
