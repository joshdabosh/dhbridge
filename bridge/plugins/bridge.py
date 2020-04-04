import asyncio, random, re

import hangups, nacre

class Bridge:
    def __init__(self, pearl, config):
        self.pearl = pearl
        self.hangouts = self.pearl.hangouts
        self.config = config
        self.usage = "Usage: {} bridge <chat_id> - ".format(self.pearl.config['format'])
        self.buildHandle()

    def build(self):
        pass
    
    def buildHandle(self):
        messageFilter = nacre.handle.newMessageFilter('^{}\s+bridge(\s.*)$'.format(self.pearl.config['format']))
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if messageFilter(event):
                    await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)


    async def respond(self, event, caller=None):
        if caller=='h':
            incoming = re.match('^{}\s+bridge(\s.*)$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
            conversation = self.hangouts.getConversation(event=event)

            if not str(self.hangouts.getUser(event=event).id_.gaia_id) in self.pearl.admins["h"]:
                await self.hangouts.send("Error: not an admin", conversation)
                return

            t = incoming.group(1)

            if t is None:
                message = self.usage + "where <chat_id> is the id of the chat you wish to bridge with. See /dh conv"
                await self.hangouts.send(message, conversation)
                return
            
            thing = str(t.strip())
            
            self.pearl.DH[thing] = conversation.id_
            self.pearl.HD[conversation.id_] = thing

            await self.hangouts.send('Bridged to Discord channel '+ str(thing), conversation)
            

        if caller == 'd':
            incoming = re.match('^{}\s+bridge(\s.*)$'.format(self.pearl.config['format']), event.content)

            if not incoming:
                return

            t = incoming.group(1)

            if t is None:
                message = self.usage + "where <chat_id> is the id of the chat you wish to bridge with. See /dh conv"
                await self.pearl.send(message, event.channel)
                return

            if not str(event.author.id) in self.pearl.admins["d"]:
                await self.pearl.send("Error: not an admin", event.channel)
                return
            
            thing = t.strip()

            self.pearl.DH[str(event.channel.id)] = thing
            self.pearl.HD[thing] = str(event.channel.id)
            
            await self.pearl.send('Bridged to Hangouts chat ' + str(thing), event.channel)

        self.pearl.save()

        


def load(pearl, config):
    return Bridge(pearl, config)
