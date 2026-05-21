import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

client = AsyncOpenAI(
    api_key=os.getenv('XAI_API_KEY'),
    base_url='https://api.x.ai/v1'
)

TRIGGER_WORDS = ['astra', 'mizu', 'astramizu']

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online as AstraMizu ✨')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over the stars'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()
    is_mentioned = bot.user.mentioned_in(message)
    has_trigger = any(word in content_lower for word in TRIGGER_WORDS)

    if is_mentioned or has_trigger:
        # Don't process as command if it's a natural chat
        if not message.content.startswith('!'):
            async with message.channel.typing():
                try:
                    response = await client.chat.completions.create(
                        model='grok-4',
                        messages=[
                            {'role': 'system', 'content': 'You are AstraMizu, a cute anime-style AI girl with a friendly, playful personality. You are helpful, witty, and a bit teasing. Use emojis sometimes.'},
                            {'role': 'user', 'content': message.content}
                        ],
                        temperature=0.8,
                        max_tokens=700
                    )
                    reply = response.choices[0].message.content
                    await message.reply(reply)
                except Exception as e:
                    await message.reply("💦 Something went wrong... AstraMizu needs a quick recharge!")
                    print(e)
            return

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms ✨')

@bot.command()
async def hello(ctx):
    await ctx.send('Hi there! I\'m AstraMizu, nice to meet you! 🌟')

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print('❌ DISCORD_TOKEN not found in environment variables!')