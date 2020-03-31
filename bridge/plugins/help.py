import asyncio
import discord
import nacre, re

class HelpSession:

	def __init__(self, pearl, config):
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildUsage()
		self.buildHandle()

	def build(self):
		pass

	def buildUsage(self):
		self.usage = "Usage: {} command<br>Commands:".format(self.pearl.config['format'])
		for command in self.config['commands']:
			self.usage += '<br><b>{}</b>: {}'.format(command, self.config['commands'][command])

		self.discUsage = discord.Embed(title=("Commands that I understand:"), color=int("ffdead", 16))
		for command in self.config['commands']:
                        self.discUsage.add_field(name=command, value=self.config['commands'][command], inline=False)

                

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}\s+help(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event, caller="h")
		self.pearl.updateEvent.addListener(handle)

	async def respond(self, event, caller=None):
                if caller == 'h':
                        message = self.usage
                        conversation = self.hangouts.getConversation(event=event)
                        await self.hangouts.send(message, conversation)
                elif caller == 'd':
                        incoming = re.match('^{}\s+help(\s.*)?.*$'.format(self.pearl.config['format']), event.content)
                        if not incoming:
                                return

                        await self.pearl.embed(self.discUsage, event.channel)

def load(pearl, config):
	return HelpSession(pearl, config)
