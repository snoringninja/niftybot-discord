"""
logout.py
@author Ryan Malacina
@SnoringNinja - https://snoring.ninja

Handles logging the bot out of discord
"""

from sys import platform

from discord.ext import commands
from resources.config import ConfigLoader

if platform == "linux" or platform == "linux2":
    import dbus # will only be imported if on linux
elif platform == "win32":
    pass

"""
import dbus
sysbus = dbus.SystemBus()
systemd = sysbus.get_object('org.freedesktop.systemd1',
                        '/org/freedesktop/systemd1')

manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

def stop_job(pwd):
        job = manager.StopUnit('niftybot.service', 'fail')
        print("stop job has run.")

"""


class Logout:
    # pylint: disable=too-few-public-methods
    """
    Logout cog handles exiting discord and
    shutting down.

    TODO: check if running as a systemd service, and if so, shutdown correctly using dbus
    """
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

    @staticmethod
    def systemd_logout(service_name):
            sysbus = dbus.SystemBus()
            systemd = sysbus.get_object('org.freedesktop.systemd1',
                                        '/org/freedesktop/systemd1')

            manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

            # I wonder if we should run DisableUnit here, and then on bot startup
            # check for linux and reenable the service so that we can still use
            # the normal bot logout method - need to look into that
            manager.StopUnit('{0}.service'.format(service_name), 'fail')
            print("SHUTDOWN: linux environment in use, using systemd")

    @commands.command(pass_context=True, no_pm=True)
    async def logout(self, ctx):
        """
        Logs the bot out.
        This can only be used by the bot owner.

        This will not work if they are using systemd to reboot the bot on shutdown or crash.
        We need to implement the systemd_shutdown function into this if they are using systemd to manage
        """
        user_id = ctx.message.author.id

        await self.bot.say("Shutting down, bye!")

        if int(user_id) == self.owner_id:
            try:
                await self.bot.logout()
                await self.systemd_logout("niftybot") # hardcoded for now
            except TypeError: # okay, not linux, so just do normal logout
                print("SHUTDOWN: non-linux environment, skipping systemd check")
                await self.bot.logout()

        return


def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(Logout(bot))
