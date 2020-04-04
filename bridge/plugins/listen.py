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
        messageFilter = nacre.handle.newMessageFilter('^(?!{})\s*(.*)'.format(self.pearl.config['format']))
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if not self.hangouts.getUser(event=event).is_self and messageFilter(event):
                    await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)

    async def respond(self, event, caller=None):
        if caller == 'h':
            incoming = re.match('^(?!{})\s*(.*)$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
            
            conversation = self.hangouts.getConversation(event=event)

            conv_id = conversation.id_
            
            if conv_id in self.pearl.HD.keys():
                toSend = "**{}:** {}".format(self.hangouts.getUser(event=event).full_name, incoming.group(1).strip())

                try:
                    channel = self.pearl.discordClient.get_channel(int(self.pearl.HD[conv_id]))
                    assert channel != None
                except (AssertionError, ValueError):
                    self.pearl.HD.pop(conv_id, 1)
                    self.pearl.DH = {k:v for k,v in self.pearl.HD.items() if str(v) != str(conv_id)}

                    await self.hangouts.send("Error sending message, bridge has been deleted.", conversation)

                    self.pearl.save()

                    return
                
                asyncio.run_coroutine_threadsafe(self.pearl.send(toSend, channel), self.pearl.discordClient.loop)

        elif caller == 'd':
            incoming = re.match('^(?!{})\s*(.*)$'.format(self.pearl.config['format']), event.content)

            if not incoming:
                return
            
            conv_id = str(event.channel.id)
            
            if conv_id in self.pearl.DH.keys():
                toSend = "<b>{}:</b> {}".format(event.author.name, incoming.group(1).strip())
                
                try:
                    conversation = self.hangouts.getConversation(cid=self.pearl.DH[conv_id])
                except KeyError:
                    self.pearl.DH.pop(conv_id, 1)
                    self.pearl.HD = {k:v for k,v in self.pearl.HD.items() if str(v) != str(conv_id)}

                    await self.pearl.send("Error sending message, bridge has been deleted.", event.channel)

                    self.pearl.save()

                    return
                    
                asyncio.run_coroutine_threadsafe(self.hangouts.send(toSend, conversation), self.pearl.loop)


def load(pearl, config):
        return Listen(pearl, config)
