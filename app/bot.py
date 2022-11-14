import discord
from discord.ui import Button, View
from discord.ext import commands
from secretToken import courseID, discordToken
from game import GameBoard

import time
from canvas import assingment_id_extractor, get_due_dates, get_lecture_link
from imageScrape import getImageXKCD
from sheets import writeToSheet

bot=commands.Bot(command_prefix='!', intents=discord.Intents.all())

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
    line = f"Bot Commands: \n\n!help : list of bot commands\n\n!due : Check assignments due\n\n!fs : Check full schedule\n\n!lecture : (In development) Link to Professor's lecture recordings\n\n!oh : Office hour information\n\n!xkcd : A random XKCD comic\n\n!game : Tic Tac Toe game"
    line1 = f"The following commands are for asking questions and answers\n\n!question : put question! before your actual question so it can be recorded to a spreadsheet for future purposes"
    line2 = f"\n\n!answer : put answer! before your answer so it can be recorded to a spreadsheet for future purposes. \n\t**Please answer as a reply to the question**"
    lines = f"```{line}{line1}{line2}```"
    return lines

@bot.event
async def on_ready():
    print('Connecting ')
    print(f"Connecting to {bot.user.name} BOT")
    print('Connection Success')
    await bot.change_presence(status=discord.Status.online, activity=None)
@bot.event
async def on_message(message):
    await message.channel.send("ICS32 Discord Bot Tic-Tac-Toe Game")
    # if message.author == bot.user:
    #     return
    if message.content.startswith('!game'):
        x = GameBoard()
        square1 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="1", row=1)
        square2 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="2", row=1)
        square3 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="3", row=1)
        square4 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="4", row=2)
        square5 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="5", row=2)
        square6 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="6", row=2)
        square7 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="7", row=3)
        square8 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="8", row=3)
        square9 = Button(label=" ", style= discord.ButtonStyle.blurple, custom_id="9", row=3)
        lst = [square1,square2,square3,square4,square5,square6,square7,square8,square9]
        async def button1(interaction):
            position = lst[int(interaction.data["custom_id"])-1]
            position.label = "X"
            x.board[position.custom_id] = "X"
            position.disabled = True
            position.style = discord.ButtonStyle.red
            # await interaction.response.edit_message(view=view)
            if x.checkUserWin():
                await message.channel.send("You Won!")
            r1 = x.checkDraw()
            if r1 == True:
                await interaction.response.edit_message(view=view)
                await message.channel.send("It's a Draw!")
            if r1 == False:
                move = x.aiHard()
                x.board[move] = "O"
                aipos = lst[int(move)-1]
                if x.checkAIWin():
                    await message.channel.send("You Lost!")
                aipos.label = "O"
                aipos.disabled = True
                aipos.style = discord.ButtonStyle.green
                await interaction.response.edit_message(view=view)
        square1.callback = button1
        square2.callback = button1
        square3.callback = button1
        square4.callback = button1
        square5.callback = button1
        square6.callback = button1
        square7.callback = button1
        square8.callback = button1
        square9.callback = button1
        view = View()
        for i in lst:
            view.add_item(i)
        await message.channel.send(view=view)

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

    if message.content.startswith('!lecture'):
        file = open('lecturelink.txt')
        lines = file.readlines()
        file.close()
        for i in lines:
            i = i.replace("'","")
            i = i.replace("(","")
            i = i.replace(")","")
            j = i.split(',,')
            j[1] = j[1].replace("\n","")
            await message.channel.send(f"{j[0]} : {j[1]}")
    
    if message.content.startswith('!oh'):
        await message.channel.send(f"Office hour is at Friday 8:00 to 9:45 in ALP 2210.\nClick on the below link to find where it is located:\n https://goo.gl/maps/BWMbE6cgYJ7ivSKN6")
    
    if message.content.startswith('!reloadA'):
        assignment_ids = assingment_id_extractor(int(courseID))
        assignmentDict = get_due_dates(assignment_ids)
        file = open('scheduled.txt', 'w')
        assignment_names = assignmentDict.keys()
        for i in assignment_names:
            line_to_write = f"{assignmentDict[i][0:10],i}\n"
            file.write(line_to_write)
        file.close()
        await message.channel.send(f"Course Assignments Reloaded")

    if message.content.startswith('!reloadL'):
        assignment_ids = get_lecture_link(int(courseID))
        await message.channel.send(f"Course Lectures Reloaded")
    
    if message.content.startswith('!xkcd'):
        d = getImageXKCD()
        await message.channel.send(d)

    if message.content.startswith('!answer'):
        try:
            questionMessage = await message.channel.fetch_message(message.reference.message_id)
            if questionMessage.content.startswith('!question'):
                messageList = [" "," "," "," "," "," "]
                questionContent = str(questionMessage.content)[10:]
                questionAuthor = str(questionMessage.author)
                questionTime = str(questionMessage.created_at)[:16]

                answerContent = str(message.content)[8:]
                answerAuthor = str(message.author)
                answerTime = str(message.created_at)[:16]

                messageList[0] = questionAuthor
                messageList[1] = questionTime
                messageList[2] = questionContent
                messageList[3] = answerAuthor
                messageList[4] = answerTime
                messageList[5] = answerContent

                content = messageList
                check = writeToSheet(content)
                await message.channel.send(check)
            else:
                await message.channel.send(f"Please reply to a message block that starts with !question.")
        except(AttributeError):
            await message.channel.send(f"Please reply to a message block that starts with !question.")
            

if __name__ == "__main__":
    bot.run(discordToken)