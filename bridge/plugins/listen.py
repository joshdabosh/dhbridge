import asyncio, random
import hangups, discord
import nacre, re

class Listen:
    def __init__(self, pearl, config):
        self.pearl = pearl
        self.hangouts = self.pearl.hangouts
        self.config = config
        self.buildHandle()

    def build(self):
        pass
    
    def buildHandle(self):
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)

    async def respond(self, event, caller=None):

        print(self.pearl.HD)
        print()
        print(self.pearl.DH)
        
        if caller == 'h':
            incoming = re.match('^(.*)$', hangups.ChatMessageEvent(event).text)
            
            conversation = self.hangouts.getConversation(event=event)

            conv_id = conversation.id_
            
            if conv_id in self.pearl.HD.keys():
                toSend = incoming.group(1).strip()

                if toSend == None:
                    return
                
                channel = self.pearl.discordClient.get_channel(self.pearl.HD[conv_id])
                
                await self.pearl.send(toSend, channel)

        elif caller == 'd':
            
            pass


def load(pearl, config):
        return Listen(pearl, config)
