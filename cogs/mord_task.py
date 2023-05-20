import markovify
from datetime import datetime
import sys, os, logging
from discord.ext import commands, tasks

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(os.path.realpath(sys.executable))[:-5]
elif __file__:
    application_path = os.path.dirname(__file__)[:-5]

def markov_save(bot):
        try:
            for f in bot.TEXT_RAW:
                print("Trying to save " + f + '.txt')
                with open(application_path + '\\data\corpus\\' + f + '.txt', 'w', encoding="utf-8") as file:
                    file.write(bot.TEXT_RAW[f])
                    print('File ' + application_path + '\\data\corpus\\' + f + '.txt written.')
                print("Making model from " + f)
                bot.TEXT_MODELS[f] = markovify.NewlineText(bot.TEXT_RAW[f], state_size=2, retain_original=False)
            print("Corpus save and model generation successful.")            
        except Exception as e:
            logging.exception(e)            

class TaskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.markovtask.start()

    def cog_unload(self):
        self.markovtask.cancel()    

    @tasks.loop(hours=12.0)
    async def markovtask(self):
        now = datetime.now()
        print(f"Updating Markov models. Time is currently: {now}")
        markov_save(self.bot)

    @markovtask.before_loop
    async def before_markovtask(self):        
        print('Markov task waiting...')
        await self.bot.wait_until_ready()