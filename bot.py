import discord
from discord.ext import commands
from secretToken import canvasToken, canvasUrl, courseID, discordToken
import time
from canvas import assingment_id_extractor, get_due_dates

bot=commands.Bot(command_prefix='!', intents=discord.Intents.default())

def check_time():
    """month,day,hr,min"""
    lst = []
    current_time = list(time.localtime())
    hour = current_time[3]
    month = current_time[1]
    day = current_time[2]
    minute = current_time[4]
    lst.append(month)
    lst.append(day)
    lst.append(hour)
    lst.append(minute)
    return lst


def bot_command():
    """Bot command help"""
    line = f"Bot Commands: \n\n!help : list of bot commands\n\n!due : Check assignments due\n\n!fs : Check full schedule\n\n!lecture : (In development) Link to Professor's lecture recordings\n\n!oh : Office hour information\n\n!xkcd : (In development) A random XKCD comic"
    line1 = f"The following commands are for asking questions and answers\n\n!question : (in development) put question! before your actual question so it can be recorded to a spreadsheet for future purposes"
    line2 = f"\n\n!answer : (in development) put answer! before your answer so it can be recorded to a spreadsheet for future purposes. \n\t**Please answer as a reply to the question**"
    lines = f"```{line}{line1}{line2}```"
    return lines

@bot.event
async def on_ready():
    print('Connecting ')
    print(f"Connecting to {bot.user.name} BOT")
    print('Connection Success')
    await bot.change_presence(status=discord.Status.online, activity=None)

# @bot.event
# async def initial_message():
#     print("Bot Commands")
@bot.event
async def on_message(message):
    # if message.author == bot.user:
    #     return
    if message.content.startswith('!help'):
        await message.channel.send(bot_command())

    if message.content.startswith('!due'):
        file = open('scheduled.txt')
        lines = file.readlines()
        file.close()
        x = check_time()
        month2 = x[0]
        day2 = x[1]
        for i in lines:
            i = i.replace("'","")
            i = i.replace("(","")
            i = i.replace(")","")
            j = i.split(',')
            k = j[0].split("-")
            month1 = k[1]
            day1 = k[2]
            j[1]=j[1].replace("\n","")
            if int(month1) >= int(month2):
                if int(day1) == int(day2)+1:
                    await message.channel.send(f"{j[1]} is due tomorrow")
                if int(day1) == int(day2):
                    await message.channel.send(f"**{j[1]} is/was due today**")
            else:
                await message.channel.send(f"None are due today and tomorrow")

    if message.content.startswith('!fs'):
        file = open('scheduled.txt')
        lines = file.readlines()
        file.close()
        x = check_time()
        month2 = x[0]
        day2 = x[1]
        for i in lines:
            i = i.replace("'","")
            i = i.replace("(","")
            i = i.replace(")","")
            j = i.split(',')
            k = j[0].split("-")
            month1 = k[1]
            day1 = k[2]
            j[1]=j[1].replace("\n","")
            if int(month1) > int(month2):
                await message.channel.send(f"{j[1]} next month at {j[0]}")
            if int(month1) == int(month2):
                if int(day1) >= int(day2):
                    await message.channel.send(f"{j[1]} this month at {j[0]}")

    # if message.content.startswith('!lectures'):
    #     link = links.resource_link
    #     await message.channel.send(link)
    
    if message.content.startswith('!oh'):
        await message.channel.send(f"Friday 8:00 to 9:45 in ALP 2210.\n Click on the below link to find where it is located:\n https://goo.gl/maps/BWMbE6cgYJ7ivSKN6")
    
    if message.content.startswith('!reload'):
        assignment_ids = assingment_id_extractor(int(courseID))
        assignmentDict = get_due_dates(assignment_ids)
        file = open('scheduled.txt', 'w')
        assignment_names = assignmentDict.keys()
        for i in assignment_names:
            line_to_write = f"{assignmentDict[i][0:10],i}\n"
            file.write(line_to_write)
        file.close()
        await message.channel.send(f"Course Assignments Reloaded")

if __name__ == "__main__":
    bot.run(discordToken)