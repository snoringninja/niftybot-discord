# Niftybot-Discord - Discord bot built on [Discord.py](https://github.com/Rapptz/discord.py)  
## THIS BRANCH IS NOW IN MAINTENANCE MODE.
### All changes, outside of critical bug fixes, should be made aginst the dev-3.0 branch moving forward. Thank you.
  
### Click [here](https://snoring.ninja/niftybot-discord) for documentation  

## About Branches
The only branch that is guaranteed to work is the master branch, as this is the branch where releases are built
from.  If you wish to contribute, please submit pull requests against the relevant branch, making sure that you have
actually tested your changes before submitting.  While any given development branch is not guaranteed to work, we
should make an effort to submit working changes that don't break anything - if your change does break something,
it is expected that that will be noted in the pull request or relevant commits where it breaks.  

---
Some things the bot ships with:

 * Server based configuration files
 * Require terms acceptance before allowing command usage
 * SQLite database that ships with GW2 tables for the GW2 api cog (GW2 table is outdated, not being updated)
 * Multiple pre-written cogs
 * Basic documentation inside each class
 * requirements.txt for PIP3 install
 * Allow bot admins per server who can configure plugins
 * Syntax replacement for common messages
 * and more!

TODO(s):
 * Code cleanup and class merging where applicable
 * Continuing documentation, both within the code and on the documentation site

We're constantly working on the bot, which means cogs may come and go, or may undertake drastic overhauls.  
Wish to help out? Please check out the [issues](https://github.com/snoringninja/niftybot-discord/issues) and 
submit a pull request with your changes!  
Wish to build a cog for the bot? Please do so, and submit a pull request!

* The included niftybot.db has the tables needed to function
* use the included requirements file to install any required dependencies (pip3 install -r requirements.txt)

Important:  
You may run into an issue when installing on Linux (honestly not sure about Windows at this point and is something that needs to be looked into) with installing the python(3)-dbus module. To properly install (especially on Linux), you will likely need to make sure that all neccessary packages are installed on the machine.  Normally, from what we've experienced, we had to install glib-2 before it would properly execute the install for python(3)-dbus.
