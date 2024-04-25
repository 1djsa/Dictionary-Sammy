# test-bot(bot class)
# This example requires the 'members' and 'message_content' privileged intents to function.
import os
import discord
import random
import requests
from discord.ext import commands
from bot_logic import gen_pass

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# command prefix 
bot = commands.Bot(command_prefix='>', description=description, intents=intents)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def get_dog_image_url():    
    url1 = 'https://random.dog/woof.json'
    res1 = requests.get(url1)
    data1 = res1.json()
    return data1['url']
# def get_meme_image_url():    
#     url = 'https://apimeme.com'
#     res = requests.get(url)
#     data = res.json()
#     return data['url']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# adding two numbers
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

# spamming word
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        
# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if num == 1:
        await ctx.send('It is Head!')
    if num == 2:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1,6)
    if nums == 1:
        await ctx.send('It is 1!')
    elif nums == 2:
        await ctx.send('It is 2!')
    elif nums == 3:
        await ctx.send('It is 3!')
    elif nums == 4:
        await ctx.send('It is 4!')
    elif nums == 5:
        await ctx.send('It is 5!')
    elif nums == 6:
        await ctx.send('It is 6!')

@bot.command(name='ask', help="Ask")
async def ask(ctx):
    await ctx.send('What do you wanna ask?')

    def check(m):
        return m.channel == ctx.message.channel and m.author == ctx.message.author
    
    try:
        message = await bot.wait_for('message', check=check, timeout=30.0)
    except:
        return
    else:
        # get data from ai
        api_url = 'http://127.0.0.1:11434/api/generate'
        # api_url = 'http://128.199.68.74:11434/api/generate'
        print(message.content)
        response = requests.post(api_url,json={
            "model": "phi",
            "prompt": message.content,
            "stream": False
        })

        res_message = response.json()['response']

        if res_message == "":
            await ctx.send("Please ask other question and make sure it in english")
        else:
            while len(res_message) > 2000:
                await ctx.send(res_message[:2000])
                res_message = res_message[2000:]
        # await ctx.send(f'Your facorite color is {message.content}!')

@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)
#adding kalimat.txt
@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)
#reading kalimat.txt
@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)
    
# random local meme image
@bot.command()
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)


@bot.command()
async def dog(ctx):
    dog_url = get_dog_image_url()
    await ctx.send(dog_url)
# @bot.command()
# async def meme(ctx):
#     meme_url = get_meme_image_url()
#     await ctx.send(meme_url)
    # img_name = random.choice(os.listdir('meme'))
    # with open(f'meme/{img_name}', 'rb') as f:
    # with open(f'meme/meme1.jpg', 'rb') as f:
    #     # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
    #     picture = discord.File(f)
    # await ctx.send(file=picture)
# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def tips(ctx):
    await ctx.send("https://www.biofarma.co.id/id/announcement/detail/8-tips-menjaga-kesehatan-dari-polusi-udara")

@bot.command()
async def ide(ctx):
    await ctx.send(" Menggunakan masker agar tidak terkena polusi\n Berjalan kaki jika ingin pergi ke tempat yang dekat\n Menggunakan transportasi umum untuk berpergian\n Jika bisa menggunakan alat transportasi listrik\n Tidak merokok\n Menanam tumbuhan / pohon di sekitar rumah")

bot.run('TOKEN')
