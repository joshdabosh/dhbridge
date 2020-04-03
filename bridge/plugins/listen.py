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
                if not self.hangouts.getUser(event=event).is_self:
                    await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)

    async def respond(self, event, caller=None):
        if caller == 'h':
            incoming = re.match('^(.*)$', hangups.ChatMessageEvent(event).text)
            
            conversation = self.hangouts.getConversation(event=event)

            conv_id = conversation.id_
            
            if conv_id in self.pearl.HD.keys():
                toSend = "<{}>: {}".format(self.hangouts.getUser(event=event).full_name, incoming.group(1).strip())

                if toSend == None:
                    return
                
                channel = self.pearl.discordClient.get_channel(self.pearl.HD[conv_id])
                
                asyncio.run_coroutine_threadsafe(self.pearl.send(toSend, channel), self.pearl.discordClient.loop)

        elif caller == 'd':
            incoming = re.match('^(.*)$', event.content)

            conv_id = event.channel.id
            
            if conv_id in self.pearl.DH.keys():
                toSend = "<{}>: {}".format(event.author.name, incoming.group(1).strip())

                if toSend == None:
                    return
                
                conversation = self.hangouts.getConversation(cid=self.pearl.DH[conv_id])
                
                asyncio.run_coroutine_threadsafe(self.hangouts.send(toSend, conversation), self.pearl.loop)
            
            pass


def load(pearl, config):
        return Listen(pearl, config)
