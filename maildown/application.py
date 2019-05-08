from cleo.application import Application
from maildown import commands

application = Application()

application.add(commands.InitCommand())
application.add(commands.VerifyCommand())
application.add(commands.SendCommand())
