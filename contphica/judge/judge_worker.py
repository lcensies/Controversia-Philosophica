import logging
import typing
from asyncio import Queue
from typing import List

from contphica.debate import Debate
from contphica.judge.judge import Judge, DEFAULT_JUDGE_LLM

LAST_JOB = (None, None)


class JudgeWorker:
    _judge: Judge
    _debate: Debate
    _answers_queue: Queue = Queue()
    _results_queue: Queue = Queue()
    _is_active: bool = True

    def __init__(self, debate: Debate):

        self._debate = debate
        self._judge = debate.judge

    async def start(self):
        while self._is_active:
            initiator_answer: str
            responder_answer: str
            (initiator_answer, responder_answer) = await self._answers_queue.get()

            logging.debug("Starting judge worker")
            if not initiator_answer:
                await self.stop()
                return

            judgement: str = """This is first round, no judgements are done yet. This round of debates is first,
              points of views and performance are going to be identified now."""

            judgement = await self._judge.async_evaluate(
                self._debate.topic,
                initiator_answer,
                responder_answer,
                previous_judgement=judgement
            )

            self._answers_queue.task_done()
            await self._results_queue.put(judgement)

    async def stop(self):
        await self._results_queue.put(None)
        self._is_active = False

    async def add_debate_results(self, initiator_answer: str, responder_answer: str):
        await self._answers_queue.put((initiator_answer, responder_answer))

    async def finalize(self) -> List[str]:
        await self._answers_queue.put((None, None))
        logging.debug("Finalizing judgements")
        # await judge_worker_task
        judgements: typing.List[str] = []
        judgement = await self._results_queue.get()
        while judgement:
            judgements.append(judgement)
            self._results_queue.task_done()
            judgement = await self._results_queue.get()
        self._results_queue.task_done()
        return judgements
