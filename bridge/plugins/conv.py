import asyncio, random
import hangups
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
        messageFilter = nacre.handle.newMessageFilter('^{}\s+conv(\s.*)?$'.format(self.pearl.config['format']))

        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if messageFilter(event):
                    await self.respond(event, caller="h")
                    
        self.pearl.updateEvent.addListener(handle)

    async def respond(self, event, caller=None):
        if caller == 'h':
            incoming = re.match('^{}\s+conv(\s.*)?.*$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
            conversation = self.hangouts.getConversation(event=event)

            message = ""

            channs = await self.pearl.getChannels()
            
            for sv, cList in channs.items():

                message += f"<b>{str(sv).upper()}</b>\n"
                
                for c in cList:
                    message += f"<b>{c.name}</b> - {c.id}\n"

                await self.hangouts.send(message.strip(), conversation)

                message = ""
                

        elif caller == 'd':
            incoming = re.match('^{}\s+conv(\s.*)?.*$'.format(self.pearl.config['format']), event.content)
            if not incoming:
                return

            


def load(pearl, config):
        return Listen(pearl, config)
