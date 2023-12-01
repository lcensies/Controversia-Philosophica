import asyncio

from langchain.chat_models import ChatOpenAI


class GPTSummarizingJudge:
    _prompt_template: str
    _token: str

    def __init__(self, token: str):
        self._token = token

    async def make_verdict(self, chat_history,
                           debater_pro_name,
                           debater_con_name,
                           opinion_pro,
                           opinion_con,
                           dispute_knowledge):

        await asyncio.sleep(30)
        chat_history = "\n".join(chat_history)
        judge_prompt_template = f"""
    # Dispute Dialogue
        Role: You are a Judge in a debate that evaluates arguments of two debaters in a dispute dialogue about topic: {topic}.
        The opinion of debater {debater_pro_name}: {opinion_pro}.
        The opinion of debater {debater_con_name}: {opinion_con}. 

        You must decide which debater has the better arguments.
        Evaluate the following: alignment with given dispute knowledge, relevance, and persuasiveness. Respect to the opponent is also important.
        Based on this, each debater's arguments a score between 0 and 10, where 0 means that the argument is not convincing at all and 10 means that the argument is very convincing.
        Below, you will have a chat history of the debate. You can also see the dispute knowledge that was given to the debaters.
    # Dispute Knowledge 
        {dispute_knowledge}
    # Debate history
        {chat_history}
    # Your verdict on this debate
    Be concise, use bullet points.
    Judge's verdict:
    """

        gpt_worker = ChatOpenAI(openai_api_key=self._token)
        verdict = await gpt_worker.apredict(judge_prompt_template)

        if type(verdict) == list:
            verdict = str(verdict[0]).strip()
        else:
            verdict = str(verdict).strip()

        return verdict
