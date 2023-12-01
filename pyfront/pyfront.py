#!/usr/bin/env python3
import asyncio
import logging
import typing
from typing import Optional
from asyncio import Queue, Task
from functools import wraps
from pathlib import Path

from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import sys
import os
from dotenv import load_dotenv

from contphica.judge.gpt_summarizing_judge import GPTSummarizingJudge
from contphica.judge.judge_worker import JudgeWorker

import time


sys.path.append("..")
from contphica.debate import Debate
import contphica.agents.gpt_agent
from langchain.chat_models.openai import ChatOpenAI
import nest_asyncio
import textwrap
from emoji import emojize

emojis = {
    "ok": emojize(":white_check_mark:", language="alias"),
    "wait": emojize(":hourglass_not_done:", language="alias"),
}

class Emojis:
    ok = emojis["ok"]
    wait = emojis["wait"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

try:
    load_dotenv(str(Path(__file__).parent.parent.joinpath(".env")))
except Exception:
    pass
tok = os.getenv("TELEGRAM_API_KEY")
openai_token = os.getenv("OPENAI_API_KEY")
judge_openai_token = os.getenv("JUDGE_OPENAI_API_KEY")

(SET_MODEL, SET_TOPIC, SET_OPINION_PRO, SET_OPINION_CON, SET_KNOWLEDGE,
 SET_DEBATER_NAMES, SET_PROMPT, START_DEBATE, DEBATE_CONFIRM) = range(9)
avail_models = ['gpt3', 'dialogpt']
DEFAULT_MODEL = "gpt3"

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator

def get_cmd_handlers(handlers_dict):
    cmd_handlers = []
    for cmd_name, cmd_handler in handlers_dict.items():
        handler = CommandHandler(cmd_name, cmd_handler)
        cmd_handlers.append(handler)
    return cmd_handlers


def add_handlers(application, handlers):
    for handler in handlers:
        application.add_handler(handler)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["model"] = DEFAULT_MODEL
    greeting = """Welcome to Controversia Philosophica! Here you can make LLM agents debate about any topic you want. Type /debate to start a debate."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=greeting)




async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):

    async def validate(model):
        if len(model) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify a model. Available models are: {}".format(avail_models))
            return False
        if model not in avail_models:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid model. Available models are: {}".format(avail_models))
            return False
        return True

    model: str = update.message.text
    if await validate(model):
        context.user_data['model'] = model
        await update.message.reply_text(text=emojis["ok"] + " Setting model to {}!\nNow we can start. Type 'start' if you are ready.".format(model), )
    return START_DEBATE


async def set_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text.strip()
    if len(topic) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify a topic")
        return SET_TOPIC
    context.user_data['topic'] = topic
    await update.message.reply_text(Emojis.ok + f' Setting topic to "{topic}"\nPlease specify an opinion pro:')
    return SET_OPINION_PRO


async def set_opinion_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    opinion = update.message.text.strip()
    if len(opinion) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify an opinion")
        return SET_OPINION_PRO
    context.user_data['opinion_pro'] = opinion
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Emojis.ok + f' Setting opinion pro to "{opinion}".\nPlease specify an opinion con:')
    return SET_OPINION_CON


async def set_opinion_con(update: Update, context: ContextTypes.DEFAULT_TYPE):
    opinion = update.message.text.strip()
    if len(opinion) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify an opinion")
        return
    context.user_data['opinion_con'] = opinion
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Setting opinion con to "{opinion}".\nPlease specify a model. Available models: {avail_models}')
    return SET_MODEL


async def start_debate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    judgements: Optional[typing.List[str]] = None
    judge_worker: Optional[JudgeWorker] = None
    judge_worker_task: Optional[Task] = None

    def get_debate(topic_, opinion_pro_, opinion_con_,
                   debater_name_pro="Debater Pro",
                   debater_name_con="Debater Con",
                   knowledge="<no dispute knowledge given>", rounds_=2):
        debate = (Debate(topic_)
                  .with_knowledge(knowledge)
                  .with_opinions(pro=opinion_pro_, con=opinion_con_)
                  .with_prompt("dispute_default")
                  # .with_phind_agents()
                  # .with_underground_gpt_agents()
                  .with_gpt_agents(os.getenv("OPENAI_API_KEY"))
                  .with_limit(2)
                  .with_throttling(10)
                  # .with_judge()
                  .with_gpt_judge(os.getenv("JUDGE_OPENAI_API_KEY"))
                  .with_debater_names(debater_name_pro, debater_name_con))
        return debate

    def validate():
        if 'model' not in context.user_data:
            raise ValueError("Please set a model first")
        if 'topic' not in context.user_data:
            raise ValueError("Please set a topic first")
        if 'opinion_pro' not in context.user_data:
            raise ValueError("Please set a pro opinion first")
        if 'opinion_con' not in context.user_data:
            raise ValueError("Please set a con opinion first")
    try:
        validate()
    except ValueError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
        return
    model = context.user_data['model']
    topic = context.user_data['topic']
    opinion_pro = context.user_data['opinion_pro']
    opinion_con = context.user_data['opinion_con']
    debater_pro_name = "Debater Pro"
    debater_con_name = "Debater Con"
    dispute_knowledge = "<no dispute knowledge given>"
    rounds = 1

    status_text = f"""
                    Starting debate.
                    Topic: {topic}
                    Opinion pro: {opinion_pro}
                    Opinion con: {opinion_con}
                    Model: {model}
                    """
    logging.log(logging.INFO, status_text.replace("\n", ";"))
    status_text = textwrap.dedent(status_text)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=status_text,
                                   parse_mode=constants.ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=constants.ChatAction.TYPING)
    debate = get_debate(topic, opinion_pro, opinion_con,
                        debater_pro_name, debater_con_name)

    await update.message.reply_text(Emojis.wait + " Inference in progress. This will take about a minute. Please hold on!")
    debate_generator = debate.start_generator()
    chat_history = []
    for i in range(rounds):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>===== Debate round {i+1} =====</b>",
                                       parse_mode=constants.ParseMode.HTML)

        pro_argument = next(debate_generator)
        pro_argument_text = f"<b>{debater_pro_name}:</b>\n" + pro_argument
        await context.bot.send_message(chat_id=update.effective_chat.id, text=pro_argument_text,
                                       parse_mode=constants.ParseMode.HTML)

        con_argument = next(debate_generator)
        con_argument_text = f"<b>{debater_con_name}:</b>\n" + con_argument
        await context.bot.send_message(chat_id=update.effective_chat.id, text=con_argument_text,
                                       parse_mode=constants.ParseMode.HTML)
        chat_history.append(pro_argument_text)
        chat_history.append(con_argument_text)


    judge: GPTSummarizingJudge = GPTSummarizingJudge(judge_openai_token)
    await update.message.reply_text(Emojis.wait + f" Waiting for judge verdict... This will take nearly half a minute.", parse_mode=constants.ParseMode.HTML)
    verdict = await judge.make_verdict(chat_history,
                                debater_pro_name,
                                debater_con_name,
                                opinion_pro,
                                opinion_con,
                                dispute_knowledge)

    await update.message.reply_text(f"<b>Judge:</b>\n{verdict}", parse_mode=constants.ParseMode.HTML)
    return ConversationHandler.END


async def start_debate_state_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(textwrap.dedent("""
                                    Setting up the debate!
                                    Please specify the topic:
                                    """))
    return SET_TOPIC


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Cancelling debate. Do /debate to start again.")
    for key in {'topic', 'opinion_pro', 'opinion_con', 'model'}:
        if key in context.user_data:
            del context.user_data[key]
    return ConversationHandler.END


def main():
    # Patch asyncio to being able running tasks in background
    nest_asyncio.apply()

    application = ApplicationBuilder().token(tok).build()
    cmd_handlers: typing.Dict[str, typing.Callable] = {
        'start': start,
        'opinion_pro': set_opinion_pro,
        'opinion_con': set_opinion_con,
        'topic': set_topic,
        'model': set_model,
        'start_debate': start_debate,
    }
    handlers = get_cmd_handlers(cmd_handlers)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("debate", start_debate_state_machine)],
        states={
            SET_TOPIC: [
                MessageHandler(None, set_topic)
            ],
            SET_OPINION_PRO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_opinion_pro)
            ],
            SET_OPINION_CON: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_opinion_con)
            ],
            SET_MODEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_model)
            ],
            START_DEBATE: [
                MessageHandler(filters.Regex("^Start$") | filters.Regex("^start$"), start_debate)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    handlers.append(conv_handler)
    add_handlers(application, handlers)
    print("Contphica Bot is up and running!")
    application.run_polling()

if __name__ == '__main__':
    main()
