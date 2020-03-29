import asyncio, random, re

import hangups, nacre

class Admin:
    def __init__(self, pearl, config):
        self.pearl = pearl
        self.hangouts = self.pearl.hangouts
        self.config = config
        self.buildHandle()
        self.admins = []

    def build(self):
        pass
    
    def buildHandle(self):
        messageFilter = nacre.handle.newMessageFilter('^{}\s+admin(\s.*)?$'.format(self.pearl.config['format']))
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if messageFilter(event):
                    await self.respond(event)
        self.pearl.updateEvent.addListener(handle)

    async def respond(self, event):
        incoming = re.match('^{}\s+admin(\s.*)?.*$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
        conversation = self.hangouts.getConversation(event=event)

        await self.hangouts.send('lol SIKE you got baited - contact josh if you want actual admin', conversation)


def load(pearl, config):
        return Admin(pearl, config)
