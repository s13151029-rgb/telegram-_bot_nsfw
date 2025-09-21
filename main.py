from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

def channel_post_handler(update: Update, context: CallbackContext):
    chat_id = update.channel_post.chat_id
    pesan = update.channel_post.text
    print(f"Pesan channel diterima dari chat ID {chat_id}: {pesan}")

    context.bot.send_message(chat_id=chat_id, text=f"ID channel ini adalah: {chat_id}")

def main():
    BOT_TOKEN = "8167264410:AAHYQgPVe_HyqIQLxZ6yuGFABWCw5Bb-P74"
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(MessageHandler(Filters.chat_type.channel, channel_post_handler))
    
    updater.start_polling()
    print("Bot berjalan, siap mendeteksi pesan di channel...")
    updater.idle()

if name == "main":
    main()
