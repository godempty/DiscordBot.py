import trivia
from dotenv import load_dotenv
from os import getenv
import discord
load_dotenv()
bot = discord.Bot()

# Components
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Class
#---------------------------------------------------------------------------------
class GuessWhoGame():
  def __init__(self):
    self.players = []
    self.started = False
  
  
#---------------------------------------------------------------------------------
# Event
#---------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
#---------------------------------------------------------------------------------
# Command
#---------------------------------------------------------------------------------
@bot.command(name="猜人名",description="開一個猜人名遊戲")
async def guessWho(ctx):
  message = discord.Message(embed=GuessWhoEmbed,components=[GW_action_row])
  await ctx.respond(f'Start a new game,id={trivia.randomID(6)}',view=GuessWhoUI())

@bot.command(name="help", description="show all commands")
async def help(ctx):
  ret = "```"
  for cmd in bot.commands:
    ret+=f'{cmd}\n'
  ret +="```"
  await ctx.respond(ret)
#----------------------------------------------------------------------------------
bot.run(getenv('TOKEN'))

