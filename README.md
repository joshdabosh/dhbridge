# DHBRIDGE


## WHAT
Two way bridge between Hangouts and Discord using [hangups](https://github.com/tdryer/hangups) and [discord.py](https://github.com/Rapptz/discord.py).


## WHY
Discord > Hangouts, but not according to my friends

## HOW
The code is really messy and it's basically just me mixing together [pearl](https://github.com/defund/pearl) and [amber](https://github.com/joshdabosh/amber).

I modified Pearl and (among many other things) shoved it onto an auxilary thread to get it to run in tandem with Amber.

## USAGE
In any servers (Hangouts / Discord) that a dhbridge bot is in, you can run `/dh help` to get a list of all the options.

`/dh admin <user>` - Gives admin permissions to `<user>` might be.
- In Hangouts, specify `user` either by using their name or gaia ID
- In Discord, specify `user` either by `@` mentioning them or by using their Discord ID

`/dh bridge <chat_id>` - Bridges the current chat to the chat `chat_id`. Use `/dh conv` to get a list of possible `chat_id`s.
- In Hangouts, `chat_id` will be the chat ID of the Discord channel you want to bridge to
- In Discord, `chat_id` will be the chat ID of the Hangouts chat

`/dh conv` - Sends a list of all conversations one can bridge to from the current chat.
- In Hangouts, dhbridge will return a list of all discord channels it has access to, by server
- In Discord, dhbridge will return a list of all Hangouts chats it is in

## SETUP
You will need a Google Hangouts account and a Discord bot token.

First, create three files, `DH.json`, `HD.json`, and `admins.json`

Then, make a directory, `private/`, and create three fYet the in `private/`, `auth.json`, `token.txt`, and `discToken.txt`.

Put into auth.json:

```
{
    "email": "your@email.here",
    "password": "yourpasswordhere",
    "secret": "",
    "token": "private/token.txt"
    "disc_token": "private/discToken.txt"
}
```

If you have 2FA enabled, add it as the `secret` field. If not, just leave it blank.

Put your Discord bot token inside `private/discToken.txt`.

### RUN
CD into the `bridge/` directory.

Install dependencies with a `pip3 install -r requirements.txt`, and then run with `python3 pearl.py`!

If dhbridge throws an error when generating the token, manually create one from these [instructions](https://github.com/tdryer/hangups/issues/350#issuecomment-323553771) and place it in `token.txt`. A copy of `manual_login.py` can be found in this repository as this seems to happen quite often.


Alternatively, simply build and run the provided Dockerfile.


## CONTRIBUTE
If you have any suggestions or issues, feel free to open an issue / PR and I'll be happy to take a look at it.
