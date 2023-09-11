import discord

# help command
ghelp = discord.Embed(title="Help", color = 0x000000)
ghelp.add_field(name= 'Create', value = '`$giveaway` - Set up a new giveaway. This command can only be accessed by users with the "Giveaway Host" role.', inline = False)
ghelp.add_field(name= 'Reroll', value = """`$reroll '#channel_name' 'message_id'` - Rerolls the specified giveaway to select a new winner. This command can only be accessed by users with the "Giveaway Host" role.""", inline = False)
ghelp.set_footer(text = 'braindead-dev on github')




