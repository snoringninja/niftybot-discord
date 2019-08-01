# Niftybot-Discord - Discord bot built on [Discord.py](https://github.com/Rapptz/discord.py)  
  
### Click [here](https://snoring.ninja/niftybot-discord) for documentation  

## About Branches
Welcome to the Dev-3.x branch.  This branch is here to track the implementation of the changes required by the
discord.py rewrite, which overhauled quite a few things to how the bot works.  This branch is highly likely to be broken
at any given time as we make changes.

Dev-2.x is still around, and is where bug fixes for the current release will be made before merging to master.  That
branch can effectively be seen as maintenance mode now, as the 3.x branch is the branch that will contain the latest and
most updated code that is required for the latest discord.py release.  

Please don't push anything against 2.x at this point unless it's a bug fix; all new features, etc. should be pushed
against the 3.x branch.

Thanks!
  
---

Important:  
You may run into an issue when installing on Linux (honestly not sure about Windows at this point and is something that 
needs to be looked into) with installing the python(3)-dbus module. To properly install (especially on Linux), you will 
likely need to make sure that all neccessary packages are installed on the machine.  Normally, from what we've 
experienced, we had to install glib-2 before it would properly execute the install for python(3)-dbus.
