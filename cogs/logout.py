from sys import platform

from discord.ext import commands
from resources.config import ConfigLoader

# Note: please see the README for issues that can arise when install dbus
if platform == "linux" or platform == "linux2":
    import dbus
elif platform == "win32":
    pass


class Logout:
    """
    Handles all logout functionality, depending on which platform the bot is running on.
    """
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = ConfigLoader().load_config_setting_int('BotSettings', 'owner_id')

    @staticmethod
    def get_system_environment():
        """
        Check which platform the bot is running under.
        Return True if Linux, False if Windows

        :return:
        """
        if platform == "linux" or platform == "linux2":
            return True
        elif platform == "win32":
            return False

    @staticmethod
    def systemd_logout(service_name):
        """
        Attempt to stop the service that is running the bot so that the logout is successful and doesn't
        restart, which is something that can be configured when using systemd.

        :param service_name: the systemd service name that the bot is running under
        :type service_name: str
        """
        sysbus = dbus.SystemBus()
        systemd = sysbus.get_object('org.freedesktop.systemd1',
                                    '/org/freedesktop/systemd1')

        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

        # Okay, so we'll just print out the "Shutting down, bye!" message
        # before we run this or logout
        print("SHUTDOWN: linux environment in use, using systemd")

        # This will fail if the user/group running the bot requires authentication to run systemctl commands
        try:
            manager.StopUnit('{0}.service'.format(service_name), 'fail')
        except dbus.exceptions.DBusException:
            print("Unable to shutdown the service, likely due to requiring authentication.")

    @commands.command(pass_context=True, no_pm=True)
    async def logout(self, ctx):
        """
        This function is designed to logout the bot out depending on the environment in use.  It still makes use of
        the logout functionality built right into discord.py, but with an extra step if using a linux environment.

        It is important to note that the systemd_logout functionality won't work if the user/group the bot is running
        under requires authentication to run the following: systemctl stop SERVICENAME

        Please keep that in mind.

        :param ctx: discord.py Context
        :return:
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

                    if systemd_enabled:
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
                print("SHUTDOWN: non-linux environment, systemd not enabled, or something failed.")
                await self.bot.logout()
        return


def setup(bot):
    """Required to allow the bot to access anything in here as a command."""
    bot.add_cog(Logout(bot))
