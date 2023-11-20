from datetime import datetime
import requests
import time
import base64


# (´･ω･`) This is our Message class, it's where we store all the info about a Discord message!
class Message:
    """Message value to better use messages"""
    def __init__(self, content, id, channelid, author, mentions, timestamp, replied_to=None, attachments=None):
        self.content = content
        self.id = id
        self.channelid = channelid
        self.author = author
        self.mentions = mentions
        self.timestamp = timestamp
        self.replied_to = replied_to  # (≧∇≦)b This is the new part! It holds the message we replied to!
        self.attachments = attachments

    class Author:
        # (・_・;) This is our Author class, it's kind of like a mini-version of a Discord user!
        def __init__(self, username, id):
            self.username = username
            self.id = id

    class Mention:
        # (o_o) Mentions! When someone tags you in a message, this is where it gets noted.
        def __init__(self, username, id):
            self.username = username
            self.id = id

    class Attachment:
        def __init__(self, url, name):
            self.url = url
            self.name = name

# (∩︵∩) And here's our Account class, it's like... your passport to do things in Discord!
class Account:
    """Stores account token to do things like send messages"""
    def __init__(self, token=str):
        response = requests.get('https://discord.com/api/v9/users/@me', headers={"authorization": token})
        if response.status_code != 200: raise TypeError('Invalid Token')
        self.token = token
        idsplitp = token.split('.')
        id = base64.b64decode(idsplitp[0])
        self.id = int(id.decode())

    # (´･Д･)」Let's find the most recent message in a channel, shall we?
    def recent_message(self, channelid):
        """gets the most recent message in the channel provided"""
        channelid = str(channelid)
        response = requests.get(url=f"https://discord.com/api/v9/channels/{channelid}/messages?limit=1", headers={"authorization": self.token})
        return parse_json(json=response.json())

    # Here we get all the guilds (servers) you're in! (⊙ヮ⊙)
    def guilds(self):
        """Gets all guilds the user is in"""
        guilds = []
        response = requests.get(url="https://discord.com/api/v10/users/@me/guilds", headers={"authorization": self.token})
        for guild in response.json():
            guilds.append(guild['id'])
        return guilds

    # Finding all channels in a guild can be tough... (＞﹏＜)
    def channels(self, guildid):
        """all channels in a guild the user has access to"""
        guildid = str(guildid)
        channels = []
        response = requests.get(url=f"https://discord.com/api/v10/guilds/{guildid}/channels",headers={"authorization": self.token})
        for channel in response.json():
            try:
                channels.append(channel["id"])
            except:
                time.sleep(5)  # (^_^メ) Gotta rest a bit if there's too much info!

        return channels

    # (っ˘̩╭╮˘̩)っ Here's how we find the message before a given one...
    def before_message(self, message):
        """gets the message before the provided message"""
        response = requests.get(url=f"https://discord.com/api/v9/channels/{message.channelid}/messages?before={message.id}", headers={"authorization": self.token})
        return parse_json(response.json())

    # Let's send a message! (ง'̀-'́)ง
    def send_message(self, content, channelid):
        """Sends a message in the following channel"""
        channelid = str(channelid)
        try:
            requests.post(url=f"https://discord.com/api/v9/channels/{channelid}/messages", headers={"authorization": self.token}, data={'content': content})
            return(True)
        except:
            return(False)

    # Let's reply to a compliment! (|-|)>
    def reply_message(self, message=Message, content='None'):
        """Reply's to the provided message!"""
        requests.post(url=f"https://discord.com/api/v9/channels/{message.channelid}/messages",
                      headers={"authorization": self.token}, json={'content': content, 'message_reference': {"message_id": message.id}})

    def get_messages(self, channelid, amount):
        messages = []
        channelid = str(channelid)
        amount = str(amount)

        response = requests.get(url=f"https://discord.com/api/v9/channels/{channelid}/messages?limit={amount}", headers={"authorization": self.token})
        for message_json in response.json():
            messages.append(parse_json(message_json, True))
        return(messages)



# Parsing JSON like a boss! (︶︹︺)
def parse_json(json, iop=False):
    if not json:
        return(None)

    if iop is True:
        message_data = json
    else:
        message_data = json[0]

    timestamp = datetime.fromisoformat(message_data.get("timestamp", "1970-01-01T00:00:00")[:-6])

    author_data = message_data.get("author", {})
    author = Message.Author(
        id=author_data.get("id", "0"),
        username=author_data.get("username", "Unknown")
    )
    attachments = []
    if message_data.get('attachments', None) != []:
        for attachment in message_data.get('attachments', None):
            attachments.append(Message.Attachment(url=attachment['url'], name=attachment['filename']))

    mentions_data = message_data.get("mentions", [])
    mentions = [Message.Mention(
        id=mention.get("id", "0"),
        username=mention.get("username", "Unknown")
    ) for mention in mentions_data]

    # Here's the new bit! We check if there's a replied-to message and handle it! (･o･)
    replied_to_data = message_data.get("referenced_message", None)
    replied_to = parse_json([replied_to_data]) if replied_to_data else None

    message = Message(
        content=message_data.get("content", "None"),
        id=message_data.get("id", "0"),
        channelid=message_data.get("channel_id", "0"),
        author=author,
        mentions=mentions,
        timestamp=timestamp,
        replied_to=replied_to,  # Adding the replied-to message here! ヽ(´▽｀)/
        attachments=attachments
    )

    return message


# Don't forget to put your token! (づ｡◕‿‿◕｡)づ
# account = Account(token="TOKEN")