import asyncio, random, re

import hangups, nacre

class Admin:
    def __init__(self, pearl, config):
        self.pearl = pearl
        self.hangouts = self.pearl.hangouts
        self.config = config

        self.usage = "Usage: {} admin <user> - ".format(self.pearl.config['format'])
        self.buildHandle()

    def build(self):
        pass
    
    def buildHandle(self):
        messageFilter = nacre.handle.newMessageFilter('^{}\s+admin(\s.*)?$'.format(self.pearl.config['format']))
        async def handle(update):
            if nacre.handle.isMessageEvent(update):
                event = update.event_notification.event
                if messageFilter(event):
                    await self.respond(event, caller="h")
        self.pearl.updateEvent.addListener(handle)

    async def IDrespond(self, matches, conversation):
        if len(matches) == 0:
            message = "No one seems to match the identifier."
            await self.hangouts.send(message, conversation)
            return

        message = "There are multiple users that match the identifier:"
        for user in matches:
            message += "<br><b>{}</b>: {}".format(user.full_name, user.id_.gaia_id)

        await self.hangouts.send(message, conversation)

    async def respond(self, event, caller=None):
        if caller== 'h':
            incoming = re.match('^{}\s+admin(\s.*)?.*$'.format(self.pearl.config['format']), hangups.ChatMessageEvent(event).text)
            conversation = self.hangouts.getConversation(event=event)

            ident = incoming.group(1)

            if ident is None:
                message = self.usage + "where <user> is either the gaia ID or name of the to-be Hangouts admin"
                await self.hangouts.send(message, conversation)
                return

            if not str(self.hangouts.getUser(event=event).id_.gaia_id) in self.pearl.admins['h']:
                message = "Error: not an admin"
                await self.hangouts.send(message, conversation)
                return

            ident = ident.strip().lower()

            if ident.isnumeric():
                uid = ident
            else:
                matches = await self.hangouts.getContact(ident)

                if len(matches) != 1:
                    self.IDrespond(matches, conversation)
                    return

                uid = str(matches[0].id_.gaia_id)

            if not uid in self.pearl.admins['h']:
                self.pearl.admins['h'].append(uid)
                await self.hangouts.send("Added Hangouts admin with ID "+uid, conversation)
            else:
                await self.hangouts.send("User {} is already a Hangouts admin".format(uid), conversation)
                
        else:
            incoming = re.match('^{}\s+admin(\s.*)?.*$'.format(self.pearl.config['format']), event.content)
            if not incoming:
                return

            ident = incoming.group(1)

            if ident is None:
                message = self.usage + "where <user> is an @ mention or UID of the to-be Discord admin"
                await self.pearl.send(message, event.channel)
                return

            if not str(event.author.id) in self.pearl.admins['d']:
                message = "Error: not an admin"
                await self.pearl.send(message, event.channel)
                return

            ident = ident.strip().lower()

            if ident.isnumeric():
                uid = str(ident)
            else:
                uid = str(event.mentions[0].id)
                """
                    message = "Must mention to-be admin"
                    await self.pearl.send(message, event.channel)
                    return

                """
            if not uid in self.pearl.admins['d']:
                self.pearl.admins['d'].append(uid)
                await self.pearl.send("Added Discord admin with ID `"+uid+"`", event.channel)
            else:
                await self.pearl.send("User `{}` already a Discord admin".format(uid), event.channel)

        self.pearl.saveAdmins()

            
def load(pearl, config):
        return Admin(pearl, config)
