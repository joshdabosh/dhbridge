import asyncio, importlib, json, os

import hangups, discord
import nacre


class Pearl:
        def __init__(self, auth, config):
                self.auth = auth
                self.config = config
                self.client = hangups.client.Client(self.authenticate())
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

        def run(self):
                self.client.on_connect.add_observer(self.hangouts.start)
                self.client.on_state_update.add_observer(self.updateEvent.fire)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.client.connect())
                loop.close()

        def startDiscord(self):
                @self.discordClient.event
                async def on_ready():
                        print("logged in alright")

                @self.discordClient.event
                async def on_message(message):
                        if message.author == self.discordClient.user:
                                return

                        print("Message received from %s: %s" %( message.author, message.content))

                        c = message.content

                self.discordClient.run(open(self.auth["disc_token"]).read())

        async def send():
            await channel.send(message)

def main():
        config = json.load(open('config.json'))
        auth = json.load(open(config['auth']))
        bridge = Pearl(auth, config)
        bridge.startDiscord()
        bridge.run()
        

if __name__ == '__main__':
	main()
