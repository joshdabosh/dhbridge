import hangups

class Hangouts:
    def __init__(self, client):
        self.client = client

    async def start(self):
        self.users, self.conversations = await hangups.build_user_conversation_list(self.client)

    async def send(self, message, conversation, annotate=True, raw=False):
        if annotate:
            annotationType = 4
        else:
            annotationType = 0

        if raw:
            segments = [hangups.ChatMessageSegment(message)]
        else:
            segments = hangups.ChatMessageSegment.from_str(message)

        request = hangups.hangouts_pb2.SendChatMessageRequest(
                request_header=self.client.get_request_header(),
                event_request_header=conversation._get_event_request_header(),
                message_content=hangups.hangouts_pb2.MessageContent(
                        segment=[segment.serialize() for segment in segments]
                ),
                annotation=[hangups.hangouts_pb2.EventAnnotation(
                        type=annotationType
                )]
        )

        await self.client.send_chat_message(request)

    def getConversation(self, cid=None, event=None):
        if event:
            cid = event.conversation_id.id
        return self.conversations.get(cid)

    def getUser(self, uid=None, event=None):
        if event:
            uid = event.sender_id.gaia_id
        return self.users.get_user(hangups.user.UserID(uid, uid))

    async def getContact(self, username=None):
        userConvoList = await hangups.build_user_conversation_list(self.client) # Basically this lets you get a list of everyone in all your chats
        userList, convoList = userConvoList # This is just extracting data
        userList = userList.get_all() # Same as above
        matches = [] # Now we start looping through data
        for user in userList:
            if username in (user.full_name).lower():
                matches.append(user)
        return matches
    
    async def getConvList(self):
        return self.conversations.get_all()

    async def getGroupChats(self):
        return [c for c in await self.getConvList() if len(c.users) > 2]

    def getConversation(self, cid=None, event=None):
        if event:
            cid = event.conversation_id.id
        return self.conversations.get(cid)
