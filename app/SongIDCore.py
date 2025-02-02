import telegram, json, time, os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, MessageQueue
import sentry_sdk


ver='1.0.0-beta3'
botName=f'SongID'
botVer=f'{botName} {ver}'
botAt=f'@SongIDBot'
botUsername='SongIDbot'
downloadDIR='downloads'


# Initialise the logger and format it's output
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)
logger = logging.getLogger(__name__)


#  Load environment variables
env = {
    'sentry_dsn': os.getenv('SONGID_SENTRY_DSN'),
    'telegram': {
        'bot_token': os.getenv('SONGID_TELEGRAM_BOT_TOKEN'),
        'dev_id': os.getenv('SONGID_TELEGRAM_DEV_ID'),
        'dev_username': os.getenv('SONGID_TELEGRAM_DEV_USERNAME')
    },
    'acr': {
        'clear': {
            'host': os.getenv('SONGID_ACR_CLEAR_HOST'),
            'access_key': os.getenv('SONGID_ACR_CLEAR_ACCESS_KEY'),
            'access_secret': os.getenv('SONGID_ACR_CLEAR_ACCESS_SECRET'),
            'recognize_type': os.getenv('SONGID_ACR_CLEAR_RECOGNIZE_TYPE'),
            'timeout': os.getenv('SONGID_ACR_CLEAR_TIMEOUT')
        },
        'noisy': {
            'host': os.getenv('SONGID_ACR_NOISY_HOST'),
            'access_key': os.getenv('SONGID_ACR_NOISY_ACCESS_KEY'),
            'access_secret': os.getenv('SONGID_ACR_NOISY_ACCESS_SECRET'),
            'recognize_type': os.getenv('SONGID_ACR_NOISY_RECOGNIZE_TYPE'),
            'timeout': os.getenv('SONGID_ACR_NOISY_TIMEOUT')
        },
        'hum': {
            'host': os.getenv('SONGID_ACR_HUM_HOST'),
            'access_key': os.getenv('SONGID_ACR_HUM_ACCESS_KEY'),
            'access_secret': os.getenv('SONGID_ACR_HUM_ACCESS_SECRET'),
            'recognize_type': os.getenv('SONGID_ACR_HUM_RECOGNIZE_TYPE'),
            'timeout': os.getenv('SONGID_ACR_HUM_TIMEOUT')
        }
    }
}

token = env['telegram']['bot_token']
devid = env['telegram']['dev_id']
devusername = env['telegram']['dev_username']
sentry_dsn = env['sentry_dsn']

sentry_sdk.init(
dsn=sentry_dsn,
release=ver,
sample_rate=1.0,
traces_sample_rate=1.0,
attach_stacktrace=True,
with_locals=True
)


# Load data/userdata.json into the variable 'userdata'
with open('data/userdata.json') as f:
    userdata = json.load(f)




#  Initialise the required telegram bot data
u=Updater(token=token, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
dp = u.dispatcher



# Log the users previous message (debugging)
def logusr(update):
    if hasattr(update.message, 'text'):
        message = update.message.text
    else:
        message = '[No message]'
    logger.info(f'[@{update.effective_chat.username}][{update.effective_chat.first_name} {update.effective_chat.last_name}][U:{update.effective_chat.id}][M:{update.effective_message.message_id}]: {message}')


# Send a message to the user
def botsend(update, context, msg):
    if hasattr(update.message, 'reply_text'):
        update.message.reply_text(str(msg)+f'\n\n<i>{botAt} <code>{ver}</code></i>', parse_mode=telegram.ParseMode.HTML)

def devsend(update, context, msg):
    if '{update.message.text}' in msg:
        if hasattr(update.message, 'text'):
            msg = update.message.text
        else:
            msg = '[No message]'
    context.bot.send_message(devid, f'User @{update.effective_user.username} ({update.effective_chat.id}): \'{msg}\'')


# Send a message to the user and log the message sent
def logbotsend(update, context, msg):
    update.message.reply_text(str(msg)+f'\n\n<i>{botAt} <code>{ver}</code></i>', parse_mode=telegram.ParseMode.HTML)
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')


# Log a message the bot has sent anonymously
def logbot(update, msg):
    logger.info(f'[@{botUsername}][{botName}][M:{update.effective_message.message_id}]: {msg}')




logger.info('Loaded: SongIDFramework')
