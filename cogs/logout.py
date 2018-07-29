"""
logout.py
@author Ryan Malacina
@SnoringNinja - https://snoring.ninja

Handles logging the bot out of discord
"""

from sys import platform

from discord.ext import commands
from resources.config import ConfigLoader

# When we import dbus, there could be an issue that it's not actually installed if being run through virtualenv
# If that is the case, there is an issue when installing it that system libraries may need to be installed.
# We should really add a FAQ for something like this and set up a testing environment to grab everything that is needed
if platform == "linux" or platform == "linux2":
    import dbus # will only be imported if on linux
elif platform == "win32":
    pass


class Logout:
    """
    Logout cog handles exiting discord and
    shutting down.

    TODO: check if running as a systemd service, and if so, shutdown correctly using dbus
    """
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

    @staticmethod
    def get_system_environment():
        if platform == "linux" or platform == "linux2":
            return True
        elif platform == "win32":
            return False

    @staticmethod
    def systemd_logout(service_name):
            sysbus = dbus.SystemBus()
            systemd = sysbus.get_object('org.freedesktop.systemd1',
                                        '/org/freedesktop/systemd1')

            manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

            # Okay, so we'll just print out the "Shutting down, bye!" message
            # before we run this or logout
            print("SHUTDOWN: linux environment in use, using systemd")
            manager.StopUnit('{0}.service'.format(service_name), 'fail')

    @commands.command(pass_context=True, no_pm=True)
    async def logout(self, ctx):
        """
        Logs the bot out.
        This can only be used by the bot owner.
        """
        user_id = ctx.message.author.id

        # Try to run systemd_logout, and if that fails run the normal logout method
        # The issue here is if they are using systemd but pass in the wrong service name it'll just reboot
        # after logging out - not really our problem though, they should correct that in the bot config and try again
        # We should probably raise more acceptable errors than TypeError (but still keep that one)
        if int(user_id) == self.owner_id:
            await self.bot.say("Shutting down, bye!")
            try:
                if self.get_system_environment():
                    systemd_enabled = ConfigLoader().load_config_setting_boolean('BotSettings', 'systemd_enabled')

                    if systemd_enabled == 'true':
                        # so even if the bot logs out, if the systemd_logout fails the bot is going to come back online
                        # assuming they have the service set to do so
                        systemd_name = ConfigLoader().load_config_setting_string('BotSettings', 'systemd_name')
                        await self.bot.logout()
                        await self.systemd_logout(systemd_name)
                    else:
                        raise TypeError
                else:
                    raise TypeError
            except TypeError:
                print("SHUTDOWN: non-linux environment, skipping systemd check")
                await self.bot.logout()
        return


def setup(bot):
    """This makes it so we can actually use it."""
    bot.add_cog(Logout(bot))
