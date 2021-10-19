import asyncio

from telebot import TeleBot
from telebot.types import Message, CallbackQuery
import os

from carbonAPI import carbonPhoto
from config import Config
from buttons import themes, colors, main_menu, remove_keyboard
from db_connector import sql_con, new_user, \
    updater_theme, updater_color, existing_checker, \
    themeANDcolor

bot = TeleBot(
    token=Config.bot_token,
    parse_mode="Markdown"
)


@bot.message_handler(commands=['start'])
def in_start(message: Message):
    """When users send the '/ start' command"""
    try:
        raw = message.from_user
        user_id, first_name, last_name = raw.id, raw.first_name, raw.last_name

        if not existing_checker(user_id=user_id):
            new_user(user_id=user_id, first_name=first_name, last_name=last_name)
            bot.send_message(chat_id=user_id, text="*🎲 Select a theme:*", reply_markup=themes())
        else:
            checker = themeANDcolor(user_id)['theme']
            if checker is not None:
                msg = bot.send_message(
                    chat_id=user_id,
                    text="*🔺 INFORMATION: 〽️*\n"
                         f"💠 _Theme:_ `{themeANDcolor(user_id)['theme'].title()}`\n"
                         f"💠 _Color:_ `{themeANDcolor(user_id)['color']}`\n"
                         "🔻 @FZBOTS 🥇\n\n"
                         "*SEND YOUR CODE OR CHANGE THEME & COLOR:*",
                    reply_markup=main_menu()
                )
                bot.register_next_step_handler(msg, in_text, msg.message_id)
            else:
                bot.send_message(chat_id=user_id, text="*🔻 Select a theme:*", reply_markup=themes())
    except BaseException as b:
        print("START", b)  # pass


@bot.message_handler(func=lambda message: True, content_types=['text'])
def in_text(message: Message, messageID = None):
    """When users write text"""
    user_id = message.from_user.id
    try:
        if message.text == r"Change Theme & Color 🔵":
            bot.delete_message(chat_id=user_id, message_id=message.message_id)
            msg = bot.send_message(chat_id=user_id, text="🔄 Loading...", reply_markup=remove_keyboard())
            bot.send_message(chat_id = user_id, text = "*🔻 Select a theme:*", reply_markup = themes())
            bot.delete_message(chat_id=user_id, message_id=msg.message_id)
        else:
            checker = themeANDcolor(user_id)['theme']
            if checker is not None:
                msg = bot.send_message(chat_id=user_id, text="⏳ Please wait...", reply_markup=remove_keyboard())

                user_text = message.text
                asyncio.run(carbonPhoto(user_text, user_id))

                with open(f'carboned_{user_id}.jpg', 'rb') as pic:
                    bot.send_photo(
                        chat_id=user_id,
                        photo=pic,
                        caption='*🟢✔️Created By @FZPicodeBot*',
                        reply_markup=main_menu())
                    bot.delete_message(chat_id=user_id, message_id=msg.message_id)
            else:
                bot.send_message(chat_id=user_id, text="*🔻 Select a theme:*", reply_markup=themes())
    except BaseException as b:
        print("TEXT ERROR:", b)  # pass
    except RuntimeError:
        pass
    finally:
        try:
            if os.path.isfile(f'carboned_{user_id}.jpg'):
                file_name = f'carboned_{user_id}.jpg'
                os.unlink(file_name)
            else:
                pass

            if messageID is not None:
                bot.delete_message(chat_id=user_id, message_id=messageID)

        except FileExistsError:
            pass
        except Exception as e:
            print("FILE IN TEXT", e)  # pass


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    """Callback query for call data"""
    try:
        if call.data.startswith("carbon_"):
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

            user_id = call.from_user.id
            new_theme = call.data.split("_")[1]

            updater_theme(user_id=user_id, theme=new_theme)

            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text="*💙 Choose color:*",
                reply_markup=colors()
            )
        elif call.data.startswith("color_"):
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

            user_id = call.from_user.id
            new_color = call.data.split("_")[1]

            updater_color(user_id=user_id, color=new_color)

            msg = bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text="*👨🏻‍💻 SEND YOUR CODE:*",
                reply_markup=None
            )

            bot.register_next_step_handler(msg, in_text, msg.message_id)
    except BaseException as b:
        print("CALLBACK", b)  # pass


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)

    if os.path.isfile('data.db'):
        pass
    else:
        sql_con()
