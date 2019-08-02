import discord
from discord.ext import commands

from resources.database import DatabaseHandler
from resources.config import ConfigLoader
from resources.bot_resources import BotResources


class BotCommands(commands.Cog):
    """
    Class to control multiple different functions that
    have no place in other classes.
    """
    def __init__(self, bot):
        self.bot = bot
        self.prefix = ConfigLoader().load_config_setting('BotSettings', 'command_prefix')

    @commands.guild_only()
    @commands.command(name='accept')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def add_accepted_user(self, ctx, member: discord.Member=None):
        """
        If a user accepts the bot terms of service, and has not
        already accepted the terms of service, this will enter them
        into the database so they won't need to accept the terms again.
        """
        member = ctx.message.author
        member_id = ctx.message.author.id
        channel = ctx.message.channel

        has_accepted = BotResources().check_accepted(member_id)
        if has_accepted:
            return await channel.send("You've already accepted my terms of service.")
        else:
            query = """INSERT INTO accepted_users (discord_id) VALUES (?)"""
            DatabaseHandler().insert_into_database(query, (str(member_id), ))
            return await channel.send("{0.mention}: thanks for accepting. You may now " \
                                      "use commands.".format(member))

    @commands.command(pass_context=True, no_pm=True, name='nick')
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def change_username(self, ctx, username: str):
        """
        Change the bot username.
        """
        member_id = ctx.message.author.id
        channel = ctx.message.channel

        if (member_id == ctx.message.server.owner_id
                or int(member_id) == ConfigLoader().load_config_setting_int(
                    'BotSettings',
                    'owner_id'
                )
           ):
            await self.bot.change_nickname(ctx.message.server.me, username)
            return await channel.send("Changed my username!")

    @commands.command(pass_context=True, no_pm=True, name="help")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.guild)
    async def get_help(self, ctx, member: discord.Member=None):
        """
        Return the link for the bot documentation.
        """
        member = ctx.message.author
        channel = ctx.message.channel

        return await channel.send(
            "{0.mention}: Please see https://docs.snoring.ninja " \
            "for now.".format(member)
        )


def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(BotCommands(bot))
