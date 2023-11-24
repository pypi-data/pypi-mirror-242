# aiodgram #

## What is this? ##
The module makes it easier for you to use the basic functions of AIOGRAM, such as sending messages/photos/video and start your bot.


## Using ##

Let's import it first:
First, import class TgBot and types from the library (use the 'from `...` import TgBot, types' construct).


Setting class TgBot:

Example:
bot = TgBot(`your token from botFather`, `admin_username`)

In async define:

	await bot.send_message(`chat id`, `text`)

or:

	await bot.send_photo(`chat id`, `photo url`)

or:

	await bot.send_video(`chat id`, `video url`)


## Example used define lib ##

`@bot.dispatcher.message_hundler(commands=['start'])

async def start(message: types.Message):

    user_id = message.from_user.id

    await bot.send_message(user_id, "hello world!")`


## For start your bot, you need ##

bot.start_polling(dispatcher=`bot Dispatcher`, skip_updates=`True or False`, on_startup=`define for start`, on_shutdown=`define for shutdown`).


**ALL PARAMETERS IN start_polling ARE VERY IMPORTANT FOR CORRECT OPERATION YOUR BOT!**


## Developer ##
author: `Darkangel`

my telegram: `t.me/darkangel58414`