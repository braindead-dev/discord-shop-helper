# config
prefix = "$"
token = "YOUR_TOKEN"
shop_link = "https://demo.com"
crisp_link = "https://go.crisp.chat/chat/embed/?website_id=[WEBSITE_ID]"

# imports
import discord
from discord.ext import commands
from messages import *
import asyncio
import datetime
from captcha.image import ImageCaptcha

bot = discord.Client()

# mod imports
import random
from random import randint


# defines bot
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

# function when bot is loaded
@bot.event
async def on_ready():
    print("Successfully logged in.")

# help
@bot.command()
async def help(ctx):
    reply = await ctx.reply(content="", embed=ghelp, mention_author=False)
    await reply.add_reaction("✅")

    def check_reply(reaction, user):
        return user == ctx.message.author

    try:
        reaction, user = await bot.wait_for("reaction_add", check=check_reply)
    except asyncio.TimeoutError:
        await reply.delete()
        await ctx.message.delete()
    else:
        if str(reaction.emoji) == "✅":
            await reply.delete()
            await ctx.message.delete()

# shop
@bot.command()
async def shop(ctx): 
    shop = discord.Embed(title="Shop", color = 0x000000)
    shop.add_field(name= 'Main Shop', value = 'shop_link', inline = False)
    reply = await ctx.reply(content="", embed=shop, mention_author=False)

# support
@bot.command()
async def support(ctx):
    support = discord.Embed(title="Support", description="crisp_link",color = 0x000000)
    reply = await ctx.reply(content="", embed=support, mention_author=False)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def getcaptcha(random_num5):
    image = ImageCaptcha(width = 280, height = 90)
    data = image.generate(random_num5)
    image.write(random_num5, str(random_num5)+'.png')

def ChooseWinner(users):
    return random.choice(users)

@bot.command()
@commands.has_role("Giveaway Host")
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = ['Which channel will the giveaway be in?', 'What are you giving away?', 'How long will the giveaway last (in seconds)?','Exclusive to a role? (if none, say "None")']
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.reply(question, mention_author=False)
        try:
            message = await bot.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.reply('You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.')
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.reply(f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}', mention_author=False)
        return
    
    # Storing the variables needed to run the rest of the commands
    channel = bot.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])
    exclusive_role = str(giveaway_answers[3])
    if exclusive_role == "None":
        exclusive_role = False
    if exclusive_role != False:
        try:
            discord.utils.get(ctx.guild.roles, name=exclusive_role)
        except:
            await ctx.reply('This role could not be found.', mention_author=False)

    @bot.event
    async def on_reaction_add(reaction, user):
        if user != bot.user:
            if str(reaction.emoji) == "🤑":

                random_num5 = str(random_with_N_digits(5))
                getcaptcha(random_num5)

                def check(m: discord.Message):
                    return m.content == random_num5

                await user.send("Please complete this captcha within 30 seconds to enter the giveaway.", file=discord.File(str(random_num5)+".png"))
                
                try:
                    await bot.wait_for('message', check = check, timeout = 30.0)
                except asyncio.TimeoutError:
                    await reaction.remove(user)
                else:
                    await user.send("Thank you for verifying. Your entry has been recorded.")

                if exclusive_role != False:
                    role = discord.utils.find(lambda r: r.name == exclusive_role, user.guild.roles)
                    if role not in user.roles:
                        await reaction.remove(user)

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.reply(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.', mention_author=False)

    # Giveaway embed message
    give = discord.Embed(title= "GIVEAWAY", color = 0x000000)
    give.add_field(name= f'{ctx.author.name} is giving away {prize}!', value = f'React with 🤑 to enter!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
    give.set_footer(text = f'Giveaway ends at {end} UTC!')
    my_message = await channel.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🤑")

    # when user reacts, verify him in next minute or reaction is removed. If exclusive_role != False, check user has role

    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    try:
        winner = ChooseWinner(users)
    except:
        nonepick = discord.Embed(title = "No one picked", description="No one could be picked for this giveaway.", color = 0x000000)
        my_message = await channel.send(embed = nonepick)

    # Announces the winner
    winning_announcement = discord.Embed(title = 'THE GIVEAWAY IS OVER!!!', color = 0x000000)
    winning_announcement.add_field(name = f'Prize: {prize}', value = f'**Winner**: {winner.mention}\n**Number of Entrants**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await channel.send(embed = winning_announcement)


@bot.command()
@commands.has_role("Giveaway Host")
async def reroll(ctx, channel: discord.TextChannel):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly

    sender_message = ctx.message
    try:
        objects = sender_message.content.split(" ")
        id_num = int(objects[2])

    except:
        await ctx.send("Invalid format.")

    try:
        new_message = await channel.fetch_message(id_num)
    except:
        await ctx.send("Incorrect id.")
        return
    
    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    try:
        winner = ChooseWinner(users)
    except:
        nonepick = discord.Embed(title = "No one picked", description="No one could be picked for this giveaway.", color = 0x000000)
        my_message = await channel.send(embed = nonepick)

    # Announces the new winner to the server
    reroll_announcement = discord.Embed(color = 0x000000)
    reroll_announcement.set_author(name = f'This giveaway has been re-rolled!')
    reroll_announcement.add_field(name = f'New Winner:', value = f'{winner.mention}', inline = False)
    await channel.send(embed = reroll_announcement)

snipe_message_author = {}
snipe_message_content = {}

@bot.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content

@bot.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(name = "Sniped Content", description = snipe_message_content[channel.id], color = 0x000000)
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except KeyError: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")


bot.run(token)

