import asyncio, random

import nacre, re

class Listen:
    def __init__(self, pearl, config):
        self.pearl = pearl
        self.hangouts = self.pearl.hangouts
        self.config = config
        self.buildHandle()
        self.admins = []

    def build(self):
        pass
    
    def buildHandle(self):
        messageFilter = nacre.handle.newMessageFilter('^{}\s+listen\s+(\s.*)?$'.format(self.pearl.config['format']))
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if messageFilter(event):
                    await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)

    async def respond(self, event, caller=None):

        
        if caller == 'h':
            incoming = re.match('^{}\s+listen\s+(\s.*)?.*$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
            conversation = self.hangouts.getConversation(event=event)

        else:
            pass


def load(pearl, config):
        return Listen(pearl, config)
