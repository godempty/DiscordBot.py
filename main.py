import trivia
from dotenv import load_dotenv
from os import getenv
from interactions import Client, Intents, listen, slash_command, ActionRow, ComponentContext, component_callback, SlashContext, Button, ButtonStyle, Embed
from interactions.api.events import MessageCreate
load_dotenv()
intents = Intents.DEFAULT | Intents.MESSAGE_CONTENT
bot = Client(intents=intents)
players = []
contexts = []
channels = []
out = {}
ans = {}
# Components
#---------------------------------------------------------------------------------
join_btn = Button(
   style=ButtonStyle.SUCCESS,
   label="加入",
)
exit_btn = Button(
   style=ButtonStyle.DANGER,
   label="離開",
)
start_btn = Button(
   style=ButtonStyle.PRIMARY,
   label="開始",
)
#---------------------------------------------------------------------------------
# Event
#---------------------------------------------------------------------------------
@listen()
async def on_ready():
    print(f'We have logged in as {bot.user}')

@listen('MessageCreate')
async def on_message(message: MessageCreate):
  msg = message.message
  if msg.author == bot.user:
    return
  if msg.content.startswith(id) and not out[msg.author]:
    out[msg.author]=msg.content.split()[1]
@component_callback('gw_join')
async def join_cb(ctx: ComponentContext):
  if players.__contains__(ctx.author.display_name):
    await ctx.send(f"{ctx.author.mention} You are already in the game.",ephemeral=True)
  else:
    players.append(ctx.author.display_name)
    contexts.append(ctx.author)
    embed = Embed(
      title="猜人名",
      description="猜人名遊戲，目前玩家人數:"+f'{len(players)},\n{players}',
      color=0x00ff00,
    )
    await ctx.edit_origin(embed=embed)
@component_callback('gw_exit')
async def exit_cb(ctx: ComponentContext):
  if not players.__contains__(ctx.author.display_name):
    await ctx.send(f"{ctx.author.mention} You are not in the game.",ephemeral=True)
  else:
    players.remove(ctx.author.display_name)
    contexts.remove(ctx.author)
    print(players)
    embed = Embed(
      title="猜人名",
      description="猜人名遊戲，目前玩家人數:"+f'{len(players)},\n{players}',
      color=0x00ff00,
    )
    await ctx.edit_origin(embed=embed)
@component_callback('gw_start')
async def start_cb(ctx: ComponentContext):
  if len(players) < 2:
    await ctx.send("1個人要玩三小")
  else:
    embed = Embed(
      title="猜人名",
      description="猜人名遊戲，目前玩家人數:"+f'{len(players)},\n{players}(已經開始)',
      color=0x00ff00,
    )
    await ctx.edit_origin(content='',embed=embed,components=[]) # remove button
#---------------------------------------------------------------------------------
# Command
#---------------------------------------------------------------------------------
@slash_command(name="猜人名",description="開一個猜人名遊戲")
async def guessWho(ctx: SlashContext):
  global id 
  id = trivia.randomID(6)
  gwJoinBtn = join_btn
  gwExitBtn = exit_btn
  gwStartBtn = start_btn
  gwJoinBtn.custom_id='gw_join'
  gwExitBtn.custom_id='gw_exit'
  gwStartBtn.custom_id='gw_start'
  rows: list[ActionRow]=[
    ActionRow(
      gwJoinBtn,
      gwExitBtn,
    ),
    ActionRow(
      gwStartBtn,
    )
  ]
  embed = Embed(
    title="猜人名",
    description="猜人名遊戲，目前玩家人數:"+f'{len(players)},\n{players}',
    color=0x00ff00,
  )
  await ctx.send(f'建立遊戲中,id={id}')
  await ctx.channel.send(embed=embed,components=rows)
# @slash_command(name="reset",description="reset")
# async def reset(ctx):
#   bot.re
  
# @slash_command(name="help", description="show all commands")
# async def help(ctx):
#   ret = "```"
#   for cmd in bot.commands:
#     ret+=f'{cmd}\n'
#   ret +="```"
#   await ctx.send(ret)
#----------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
bot.start(getenv('TOKEN'))

