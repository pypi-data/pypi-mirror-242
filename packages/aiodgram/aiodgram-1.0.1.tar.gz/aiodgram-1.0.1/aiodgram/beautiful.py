import colorama
from sys import platform
from os import system

class ColorStart:

    """
    This class uou can used from beautifull start your Telegram Bot
    """

    def __init__(self, 
                 dispatcher = None,
                 admin_username: str = None
                 ) -> None:
        
        self.dispatcher = dispatcher
        self.admin_username = admin_username


    
    async def on_startup(self):
        if platform.startswith("win"):
            system("cls")
        else:
            system("clear")


        if self.admin_username == None:
            print(colorama.Fore.GREEN + f"~~~~~~ BOT WAS STARTED @{(await self.dispatcher.bot.get_me()).username} ~~~~~~")
        else:
            print(colorama.Fore.GREEN + f"~~~~~~ BOT WAS STARTED @{(await self.dispatcher.bot.get_me()).username} ~~~~~~")
            print(colorama.Fore.LIGHTGREEN_EX + f"~~~~~~ Bot developer @{self.admin_username} ~~~~~~" + colorama.Fore.RESET)



    async def on_shutdown(self):

        if platform.startswith("win"):
            system("cls")
        else:
            system("clear")
        
        print(colorama.Fore.RED + f"~~~~~~ Bot was stopped! ~~~~~~\n" + colorama.Fore.RESET)