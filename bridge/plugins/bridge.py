import asyncio, random, re

import hangups, nacre

class Bridge:
    def __init__(self, pearl, config):
        self.pearl = pearl
        self.hangouts = self.pearl.hangouts
        self.config = config
        self.buildHandle()
        self.pearl.admins = []
        self.pearl.DH = {}
        self.pearl.HD = {}

    def build(self):
        pass
    
    def buildHandle(self):
        messageFilter = nacre.handle.newMessageFilter('^{}\s+bridge(\s.+)+.*$'.format(self.pearl.config['format']))
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if messageFilter(event):
                    await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)


    async def respond(self, event, caller=None):
        if caller=='h':
            incoming = re.match('^{}\s+bridge(\s.+)+.*$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
            conversation = self.hangouts.getConversation(event=event)

            thing = incoming.group(1).strip()

            self.pearl.DH[thing] = conversation.id_
            self.pearl.HD[conversation.id_] = thing
            
            await self.hangouts.send(thing, conversation)
            

        if caller == 'd':
            incoming = re.match('^{}\s+bridge(\s.+)+.*$'.format(self.pearl.config['format']), event.content)

            if not incoming:
                return
            
            thing = incoming.group(1).strip()

            self.pearl.DH[event.channel.id] = thing
            self.pearl.HD[thing] = event.channel.id
            await self.pearl.send(thing, event.channel)

        


def load(pearl, config):
    return Bridge(pearl, config)
