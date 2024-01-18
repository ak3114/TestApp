import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import pandas as pd


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Use /about or /help to ask questions.")

async def about(update: Update, context):
    question = ' '.join(context.args)
    answer = get_answer_from_sheet(question)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

async def help(update: Update, context):
    question = ' '.join(context.args)
    answer = get_answer_from_sheet(question)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

# google Sheets integration


def get_answer_from_sheet(question):
    try:
        # Google Sheet URL
        SHEET_ID = '1qh8osnsTByNAi8S7IgtgEqEko6xGG71UH73zLWN5FWA'
        SHEET_NAME = 'Sheet1'
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

        # read data into a Pandas DataFrame
        df = pd.read_csv(url)

        target_question = question.strip() # Remove leading and trailing whitespaces from the questions
        
        # find the row with the question and return the corresponding answer
        df['Questions'] = df['Questions'].str.strip() # Remove leading and trailing whitespaces from the Questions column

        if target_question in df['Questions'].values:
            matching_row = df[df['Questions'] == target_question]
            if not matching_row.empty:
                # Assuming 'Answer' is the column name
                answer = matching_row['Answer'].values[0]
                return answer
        else:
            return "Sorry, I couldn't find an answer to that question."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Main code
if __name__ == '__main__':
    application = ApplicationBuilder().token(
        '6556831140:AAEwsGuiuywLcKpP21LMCujzJs5pqR9EzWk').build()

    start_handler = CommandHandler('start', start)
    about_handler = CommandHandler('about', about)
    help_handler = CommandHandler('help', help)

    application.add_handler(start_handler)
    application.add_handler(about_handler)
    application.add_handler(help_handler)

    # Handle unknown commands
    unknown_handler = MessageHandler(filters.COMMAND, lambda update, context: context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command."
    ))
    application.add_handler(unknown_handler)

    application.run_polling()
