from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import nmap
from bs4 import BeautifulSoup
import requests
import re
import os

TOKEN = os.environ['TOKEN']


def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Push start to work magic 🎩✨", callback_data='start_scraping')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to Blackhat\'s Nmapper 🕵️‍♂️', reply_markup=reply_markup)


def button(update: Update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'start_scraping':
        query.edit_message_text(text="Please enter the target website (HTTPS) you'd like to map 🎯")


def handle_message(update: Update, context):
    website = update.message.text
    context.user_data['website'] = website
    update.message.reply_text("Blackhat's working his magic... 🧙‍♂️")
    
    try:
        nm = nmap.PortScanner()
        nm.scan(website, '80')
        page = requests.get(website)
        soup = BeautifulSoup(page.content, "html.parser")
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup.text, re.I)
        update.message.reply_text(f"Emails found: {emails}")
    except Exception as e:
        update.message.reply_text(f"Blackhat's Nmapper failed to scrape the website due to an error: {str(e)} 😓")
        return

    keyboard = [
        [InlineKeyboardButton("Another scrape? 🔄", callback_data='start_scraping')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Would you like to continue?', reply_markup=reply_markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
