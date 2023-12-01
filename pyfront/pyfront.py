#!/usr/bin/env python3

import logging
import typing
from functools import wraps
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import sys
import os
sys.path.append("..")
from contphica.debate import Debate
import textwrap

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

tok = os.getenv("TELEGRAM_API_KEY")
openai_token = os.getenv("OPENAI_API_KEY")

(SET_MODEL, SET_TOPIC, SET_OPINION_PRO, SET_OPINION_CON, SET_KNOWLEDGE, SET_DEBATER_NAMES, SET_PROMPT, START_DEBATE) = range(8)


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
    greeting = """Welcome to Controversia Philosophica! Here you can make LLM agents debate about any topic you want."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=greeting)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    avail_models = ['gpt3', 'dialogpt']

    async def validate():
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify a model")
            return False
        if context.args[0] not in avail_models:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid model. Available models are: {}".format(avail_models))
            return False
        return True
    if await validate():
        model = context.args[0]
        context.user_data['model'] = model
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Setting model to {}".format(model))


@send_action(constants.ChatAction.TYPING)
async def set_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify a topic")
        return
    topic = ' '.join(context.args)
    context.user_data['topic'] = topic
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Setting topic to "{}"'.format(topic))


async def set_opinion_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify an opinion")
        return
    opinion = ' '.join(context.args)
    context.user_data['opinion_pro'] = opinion
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Setting opinion pro to "{}"'.format(opinion))


async def set_opinion_con(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify an opinion")
        return
    opinion = ' '.join(context.args)
    context.user_data['opinion_con'] = opinion
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Setting opinion con to "{}"'.format(opinion))


@send_action(constants.ChatAction.TYPING)
async def startdebate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def get_debate(topic_, opinion_pro_, opinion_con_,
                   debater_name_pro="Debater Pro",
                   debater_name_con="Debater Con",
                   knowledge="<no dispute knowledge given>"):
        debate = (Debate(topic_)
                  .with_knowledge(knowledge)
                  .with_opinions(pro=opinion_pro_, con=opinion_con_)
                  .with_prompt("dispute_default")
                  .with_gpt_agents(token=openai_token)
                  .with_limit(2)
                  .with_debater_names(debater_name_pro, debater_name_con))
        return debate

    # def validate():
    #     if 'model' not in context.user_data:
    #         raise ValueError("Please set a model first")
    #     if 'topic' not in context.user_data:
    #         raise ValueError("Please set a topic first")
    #     if 'opinion_pro' not in context.user_data:
    #         raise ValueError("Please set a pro opinion first")
    #     if 'opinion_con' not in context.user_data:
    #         raise ValueError("Please set a con opinion first")
    # try:
    #     validate()
    # except ValueError as e:
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
    #     return
    # model = context.user_data['model']
    # topic = context.user_data['topic']
    # opinion_pro = context.user_data['opinion_pro']
    # opinion_con = context.user_data['opinion_con']
    topic = 'The death penalty should be abolished'
    opinion_pro = 'The death penalty is a barbaric practice that has no place in modern society'
    opinion_con = 'The death penalty is a necessary deterrent to crime'
    model = 'gpt3'

    status_text = f"""
                    Starting debate.
                    Topic: {topic}
                    Opinion pro: {opinion_pro}
                    Opinion con: {opinion_con}
                    Model: {model}
                    """
    status_text = textwrap.dedent(status_text)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=status_text,
                                   parse_mode=constants.ParseMode.HTML)
    await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=constants.ChatAction.TYPING)
    debate = get_debate(topic, opinion_pro, opinion_con)
    for i, (pro_argument, con_argument) in enumerate(debate.start_generator()):
        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=constants.ChatAction.TYPING)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>===== Debate round {i+1} =====</b>",
                                       parse_mode=constants.ParseMode.HTML)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>Pro:</b>\n" + pro_argument,
                                       parse_mode=constants.ParseMode.HTML)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>Con:</b>\n" + con_argument,
                                       parse_mode=constants.ParseMode.HTML)


def main():
    application = ApplicationBuilder().token(tok).build()
    cmd_handlers: typing.Dict[str, typing.Callable] = {
        'start': start,
        'opinion_pro': set_opinion_pro,
        'opinion_con': set_opinion_con,
        'topic': set_topic,
        'model': set_model,
        'start_debate': startdebate,
    }
    handlers = get_cmd_handlers(cmd_handlers)
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler("start_debate", start)],
    #     states={
    #         SET_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_topic)],
    #         SET_OPINION_PRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_opinion_pro)],
    #         SET_OPINION_CON: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_opinion_con)],
    #         SET_MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_model)],
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )

    add_handlers(application, handlers)
    application.run_polling()

if __name__ == '__main__':
    main()
