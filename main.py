import trivia
from dotenv import load_dotenv
from os import getenv
from interactions import Client, Intents, listen, slash_command, ActionRow, ComponentContext, component_callback, SlashContext, Button, ButtonStyle, Embed
from interactions.api.events import MessageCreate
load_dotenv()
intents = Intents.DEFAULT | Intents.MESSAGE_CONTENT
bot = Client(intents=intents)
player_names = []
players = []
questions = []
channels = []
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
  if msg.content.split()[0]==id:
    if players.__contains__(msg.author.id):
      await msg.channel.send('你已經出完題目了')
    elif len(msg.content.split()) < 2:
      await msg.channel.send('請以以下格式輸出\nid 題目內容')
    elif questions.__contains__(msg.content.split()[1]):
      await msg.channel.send('撞題了')
    else:
      print(msg.author.username,"出了",msg.content.split()[1])
      players.append(msg.author.id)
      player_names.append(msg.author.username)
      channels.append(msg.channel)
      questions.append(msg.content.split()[1])
      await msg.channel.send(f'你出了{msg.content.split()[1]}')

@component_callback('gw_start')
async def start_cb(ctx: ComponentContext):
  if len(players) < 2:
    await ctx.send("1個人要玩三小")
  else:
    # shuffle
    print(questions)
    ans = trivia.shuffle(questions)
    print(ans)
    idx = 0
    for channel in channels:
      tmp = []
      tmp.extend(ans)
      tmp.remove(tmp[idx])
      tmp1 = []
      tmp1.extend(player_names)
      tmp1.remove(tmp1[idx])
      ListEmbed = Embed(
        title='猜人名',
        description=f"以下是這次題目的對應\n{tmp1}\n{tmp}",
        color=0x00e51f
      )
      await channel.send(embed=ListEmbed)
      idx += 1
    embed = Embed(
      title="猜人名",
      description="猜人名遊戲，目前玩家人數:"+f'{len(players)},\n{player_names}(已經開始)',
      color=0x00ff00,
    )
    await ctx.edit_origin(content='',embed=embed,components=[]) # remove button
@component_callback('gw_update')
async def upd_cb(ctx: ComponentContext):
  embed = Embed(
    title="猜人名",
    description=f"猜人名遊戲，ID={id}，目前玩家人數:{len(players)},\n{player_names}",
    color=0x00ff00,
  )
  start_btn =  Button(
    style=ButtonStyle.BLUE,
    label="開始",
    custom_id='gw_start',
  )
  update_btn = Button(
    style=ButtonStyle.SUCCESS,
    label="刷新狀態",
    custom_id='gw_update'
  )
  rows: list[ActionRow]=[
    ActionRow(
      start_btn,
      update_btn
    )
  ]
  await ctx.edit_origin(embed=embed,components=rows)
#---------------------------------------------------------------------------------
# Command
#---------------------------------------------------------------------------------
@slash_command(name="猜人名",description="開一個猜人名遊戲")
async def guessWho(ctx: SlashContext):
  global id 
  id = trivia.randomID(6)
  start_btn =  Button(
    style=ButtonStyle.BLUE,
    label="開始",
    custom_id='gw_start',
  )
  update_btn = Button(
    style=ButtonStyle.SUCCESS,
    label="刷新狀態",
    custom_id='gw_update'
  )
  rows: list[ActionRow]=[
    ActionRow(
      start_btn,
      update_btn
    )
  ]
  embed = Embed(
    title="猜人名",
    description=f"猜人名遊戲，ID={id}，目前玩家人數:{len(players)},\n{player_names}",
    color=0x00ff00,
  )

  await ctx.send(embed=embed,components=rows)
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

