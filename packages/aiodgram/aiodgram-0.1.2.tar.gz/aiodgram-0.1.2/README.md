# aiodgram #

## What is this? ##
The module makes it easier for you to use the basic functions of AIOGRAM, such as sending messages/photos/video and start your bot.


## Using ##

Let's import it first:
First, import class TgBot and types from the library (use the 'from `...` import TgBot, types' construct).


Setting class TgBot:

Example:
bot = TgBot(`your token from botFather`)

in async define:

	await bot.send_message(`chat id`, `text`)

or:

	await bot.send_photo(`chat id`, `photo url`)

or:

	await bot.send_video(`chat id`, `video url`)
.


For start your bot, you need write:

bot.start_polling(dispatcher=`bot Dispatcher`, skip_updates=`True or False`, on_startup=`define for start`, on_shutdown=`define for shutdown`).


## Developer ##
author: `Darkangel`

my telegram: `t.me/darkangel58414`