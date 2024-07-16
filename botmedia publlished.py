import logging
from multiprocessing.resource_sharer import stop
import os
import sys
from telegram import Chat, ChatInviteLink, Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configurazione del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ID del canale a cui inviare i media (es. @NomeCanale)
CHANNEL_ID = '@nome_canale'
# Token del bot
TOKEN = 'bot token'
ADMIN_ID='@dumbn0ra'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Ciao! Usa /share (anonimo) o /shareall (include username) per condividere i media.')

def share(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        shared_message = update.message.reply_to_message
        send_media_to_channel(shared_message, context, anonymous=True)
        update.message.reply_text('Media condiviso anonimamente con successo su {CHANNEL_ID}')
    else:
        update.message.reply_text('Rispondi a un messaggio con media usando /share per condividerlo.')

def shareall(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        shared_message = update.message.reply_to_message
        send_media_to_channel(shared_message, context, anonymous=False)
        update.message.reply_text('Media condiviso con successo su {CHANNEL_ID}')
    else:
        update.message.reply_text('Rispondi a un messaggio con media usando /shareall per condividerlo anonimamente.')

def send_media_to_channel(message, context, anonymous: bool):
    caption = f'Condiviso da @{message.from_user.username} nel gruppo "{message.chat.title}"' if not anonymous else 'Condiviso anonimamente'
    media_group = []

    if message.photo:
        media_group.append(InputMediaPhoto(media=message.photo[-1].file_id, caption=caption))
    elif message.video:
        media_group.append(InputMediaVideo(media=message.video.file_id, caption=caption))

    if media_group:
        context.bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
    else:
        context.bot.send_message(chat_id=CHANNEL_ID, text=caption)

def restart(update: Update, context: CallbackContext):
    update.message.reply_text('Riavvio il bot')

    # Chiudere tutte le richieste di getUpdates
    context.bot_data (Updater);stop()

def info(update: Update, context: CallbackContext):
    bot_info = context.bot.get_me()
    update.message.reply_text(f'Nome: {bot_info.first_name}\nUsername: @{bot_info.username}\nID: {bot_info.id}\nper info o segnalazioni potete contattare {ADMIN_ID}')


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hello", start))
    dispatcher.add_handler(CommandHandler("share", share))
    dispatcher.add_handler(CommandHandler("shareall", shareall))
    dispatcher.add_handler(CommandHandler("restart", restart))
    dispatcher.add_handler(CommandHandler("more", info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
