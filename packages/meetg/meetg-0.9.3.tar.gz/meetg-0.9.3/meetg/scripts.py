#!/usr/bin/env python3
import os, sys


BOT_MAIN_PY = '''
from meetg.botting import BaseBot
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters, Updater


# Example of your bot
class {name_cc}Bot(BaseBot):

    def init_handlers(self):
        # Define handlers here. See available handlers in the PTB docs:
        # https://python-telegram-bot.readthedocs.io/en/stable/telegram.html#handlers
        handlers = (
            CommandHandler('start', self.reply_start, Filters.chat_type.private),
            MessageHandler(Filters.chat_type.private, self.reply_private),
            MessageHandler(Filters.chat_type.groups, self.reply_group),
        )
        return handlers

    def init_jobs(self, job_queue):
        # Define periodic jobs here. See the PTB docs for JobQueue methods:
        # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html
        job_queue.run_repeating(self.job_do_stuff, 60 * 60)  # each hour

    def reply_start(self, update_obj, context):
        # What to do when /start command received
        chat_id = update_obj.effective_chat.id
        self.send_message(chat_id, '/start received')

    def reply_private(self, update_obj, context):
        # What to do when a private message received
        chat_id = update_obj.effective_chat.id
        text = update_obj.effective_message.text
        answer = f'Text received in private: {{text}}'
        self.send_message(chat_id, answer)

    def reply_group(self, update_obj, context):
        # What to do when a group message received
        chat_id = update_obj.effective_chat.id
        text = update_obj.effective_message.text
        answer = f'Text received in group: {{text}}'
        self.send_message(chat_id, answer)

    def job_do_stuff(self, context=None):
        print('job_do_stuff executed')
'''

MANAGE_PY = '''
import os, sys

from meetg.manage import exec_args


def main():
    src_path = os.path.dirname(os.path.abspath(__file__))
    exec_args(sys.argv, src_path)


if __name__ == '__main__':
    main()
'''

SETTINGS_PY = '''
from meetg.default_settings import *


tg_api_token = ''

db_name = '{name_cc_uncap}DB'
db_name_test = '{name_cc_uncap}TestDB'

bot_class = 'bot.main.{name_cc}Bot'

stats_to = ()  # Telegram IDs where to report bot stats
'''

TEST_REPLY_PY = '''
from meetg.testing import BotTestCase


class ReplyTest(BotTestCase):

    def test_reply_start(self):
        self.bot.receive_message('/start')
        assert self.bot.last_method.name == 'send_message'
        assert self.bot.last_method.args['text'] == '/start received'

    def test_reply_private(self):
        self.bot.receive_message('p uyui')
        assert self.bot.last_method.name == 'send_message'
        assert self.bot.last_method.args['text'] == 'Text received in private: p uyui'

    def test_reply_group(self):
        self.bot.receive_message('g uyui', chat__type='group')
        assert self.bot.last_method.name == 'send_message'
        assert self.bot.last_method.args['text'] == 'Text received in group: g uyui'
'''

PROJECT_CREATED = '''
Project {name} created.

Now fill at least tg_api_token var in {name_lc}/settings.py, and you are ready to go.

To run: python3 manage.py run
To run tests: python3 manage.py test
To start coding, open bot/main.py
'''.strip()


def to_camelcase(string):
    camel_string = ''
    up_next = True
    for idx, char in enumerate(string.strip()):
        if char.isdigit() and idx == 0:
            continue
        if char.isalpha() or char.isdigit():
            if up_next:
                char = char.upper()
            camel_string += char
            up_next = False
        else:
            up_next = True
    return camel_string


def to_lowercase(string):
    lower_string = ''
    for idx, char in enumerate(string.strip()):
        if char.isdigit() and idx == 0:
            continue
        if char.isalpha() or char.isdigit():
            lower_string += char
        else:
            lower_string += ' '
    lower_string = '_'.join(lower_string.strip().split())
    return lower_string.lower()


def create_file(path, content):
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(path, 'w') as f:
        f.write(content.lstrip())


def start_project(name, path):
    name_cc = to_camelcase(name)
    name_lc = to_lowercase(name)
    name_cc_uncap = name_cc[0].lower() + name_cc[1:]

    dir_path = os.path.join(path, name_lc)
    bot_path = os.path.join(dir_path, 'bot')
    tests_path = os.path.join(bot_path, 'tests')

    main_py_content = BOT_MAIN_PY.format(name_cc=name_cc)
    main_py_path = os.path.join(bot_path, 'main.py')
    create_file(main_py_path, main_py_content)

    init_py_path = os.path.join(bot_path, '__init__.py')
    create_file(init_py_path, '')

    test_reply_py_path = os.path.join(tests_path, 'test_reply.py')
    create_file(test_reply_py_path, TEST_REPLY_PY)

    tests_init_py_path = os.path.join(tests_path, '__init__.py')
    create_file(tests_init_py_path, '')

    settings_py_content = SETTINGS_PY.format(name_cc=name_cc, name_cc_uncap=name_cc_uncap)
    settings_py_path = os.path.join(dir_path, 'settings.py')
    create_file(settings_py_path, settings_py_content)

    manage_py_path = os.path.join(dir_path, 'manage.py')
    create_file(manage_py_path, MANAGE_PY)

    print(PROJECT_CREATED.format(name=name, name_lc=name_lc))


def admin():
    path = os.getcwd()
    args = sys.argv

    if len(args) > 2 and args[1] == 'start':
        name = args[2]
        start_project(name, path)
    else:
        print('Usage: meetg-admin start my_project')
