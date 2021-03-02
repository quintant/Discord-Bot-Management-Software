import UILayer.UIController as UIController
import discord
from discord.ext import commands
if __name__ == "__main__":  # Sigurjón Ingi
    
    ex = True
    # while ex:
    #     try:
    bot = commands.Bot(command_prefix=".")
    @bot.event
    async def on_ready():
        x = UIController.UIController(bot)
        ex = x.start()
        quit()
    with open("token.txt", "r") as f:
        TOKEN = f.readlines()
    bot.run(TOKEN[0])
    
        # except Exception:
        #     print("shitter")
        #     ex = False
