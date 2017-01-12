import discord
import re
from discord.ext import commands
from subprocess import call
from string import printable
from sys import argv

class Events:
    """
    Special event handling.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    forbidden_words = [
        'deflemask',
        
    ]

    async def scan_message(self, message):
        if message.author == self.bot.server.me or self.bot.staff_role in message.author.roles or message.channel == self.bot.helpers_channel:  # don't process messages by the bot or staff or in the helpers channel
            return
        embed = discord.Embed()
        embed.description = message.content
        if message.author.id in self.bot.watching:
            await self.bot.send_message(self.bot.messagelogs_channel, "**Watch log**: {} in {}".format(message.author.mention, message.channel.mention), embed=embed)
        is_help_channel = message.channel.name == "critique"
        msg = ''.join(char for char in message.content.lower() if char in printable)
        contains_invite_link = "discordapp.com/invite" in msg or "discord.gg" in msg
        contains_forbidden_word_mention = any(x in msg for x in self.forbidden_words)
        if contains_invite_link:
            await self.bot.send_message(self.bot.messagelogs_channel, "✉️ **Invite posted**: {} posted an invite link in {}\n------------------\n{}".format(message.author.mention, message.channel.mention, message.content))
        if contains_forbidden_word_mention:
            try:
                await self.bot.delete_message(message)
            except discord.errors.NotFound:
                pass
            await self.bot.send_message(message.author, "Please read the rules in #welcome. You mentioned something you shouldn't have, therefore your message was automatically deleted.", embed=embed)
            await self.bot.send_message(self.bot.messagelogs_channel, "**Forbidden word**: {} mentioned a forbidden word in {} (message deleted)".format(message.author.mention, message.channel.mention), embed=embed)

    async def on_message(self, message):
# Automatically updates when github webhook posts changes to Yumetaro. This shall return sometime.
#        if message.author.name == "GitHub" and message.author.discriminator == "0000":
#            await self.bot.send_message(self.bot.helpers_channel, "Automatically pulling changes!")
#            call(['git', 'pull'])
#            await self.bot.close()
#            return
        await self.bot.wait_until_ready()
        await self.scan_message(message)

    async def on_message_edit(self, message_before, message_after):
        await self.bot.wait_until_ready()
        await self.scan_message(message_after)

def setup(bot):
    bot.add_cog(Events(bot))
