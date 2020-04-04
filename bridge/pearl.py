import asyncio, importlib, json, os

from threading import Thread

import hangups

import discord

import nacre

import lockfile

class Pearl:
    def __init__(self, auth, config):
        self.auth = auth
        self.config = config
        self.client = hangups.client.Client(self.authenticate())
        self.admins = json.load(open("admins.json"))

        self.DH = json.load(open("DH.json"))
        self.HD = json.load(open("HD.json"))
        
        self.hangouts = nacre.hangouts.Hangouts(self.client)
        self.updateEvent = nacre.event.Event()
        self.discordClient = discord.Client()
        self.load()

    def authenticate(self):
        authenticator = nacre.auth.Authenticator(self.auth['email'], self.auth['password'], self.auth['secret'])
        token = hangups.RefreshTokenCache(os.path.join(os.getcwd(), self.auth['token']))
        return hangups.get_auth(authenticator, token)

    def load(self):        
        self.plugins = {}

        plugins = self.config['plugins']

        for name in plugins:
            path = os.path.join(os.getcwd(), plugins[name]['path'])
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.plugins[name] = module.load(self, plugins[name])
            self.plugins[name].build()

    def run2(self):
        self.client.on_connect.add_observer(self.hangouts.start)
        self.client.on_state_update.add_observer(self.updateEvent.fire)
        self.loop = asyncio.new_event_loop()

        self.loop.run_until_complete(self.client.connect())

    def run(self):
        t = Thread(target=self.run2)
        t.daemon = True
        t.start()

        print("started hangouts")

        self.startDiscord()


    def save(self):
        with lockfile.LockFile("DH.json"):
            f = open("DH.json", 'w')
            f.write(json.dumps(self.DH))
            f.close()

        with lockfile.LockFile("HD.json"):
            f = open("HD.json", "w")
            f.write(json.dumps(self.HD))
            f.close()

    def saveAdmins(self):
        with lockfile.LockFile("admins.json"):
            f = open("admins.json", "w")
            f.write(json.dumps(self.admins))
            f.close()


    def startDiscord(self):
        @self.discordClient.event
        async def on_ready():
            print("started discord")

        @self.discordClient.event
        async def on_message(message):
            if message.author == self.discordClient.user:
                return

            #print("Message received from %s: %s" %( message.author, message.content))

            c = message.content

            # this loop is terrible but it's only a few plugins
            # so it SHOULD be fine
            for _, p in self.plugins.items():
                await p.respond(message, caller='d')

        self.discordClient.run(open(self.auth["disc_token"]).read())

    async def send(self, message, channel):
        await channel.send(message)

    async def embed(self, embed, channel):
        await channel.send(embed=embed)

    async def getChannels(self):
        text_channel_list = {}
        for server in self.discordClient.guilds:
            text_channel_list[server] = server.text_channels

        return text_channel_list

    async def getServers(self):
        return self.discordClient.guilds

def main():
    config = json.load(open('config.json'))
    auth = json.load(open(config['auth']))
    bridge = Pearl(auth, config)

    bridge.run()

if __name__ == '__main__':
    main()
