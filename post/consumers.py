# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.home = "home"
        print(self.home)
        self.home_name = 'chat_%s' % self.home
        print(self.home_name)

        # Join room group
        await self.channel_layer.group_add(
            self.home_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.home_name,
            self.channel_name
        )

    # setelah tekan post
    # masuk fungsi ini dlu, baru dia send ke semua grup
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'votes' in text_data_json:
            num=int(text_data_json['num'])
            votes=int(text_data_json['votes'])
            # Send message to room group
            await self.channel_layer.group_send(
                self.home_name,
                {
                    'type': 'new_votes',
                    'num':num,
                    'votes': votes
                }
            )
        elif 'comment' in text_data_json:
            num=int(text_data_json['num'])
            comment=text_data_json['comment']
            # Send message to room group
            await self.channel_layer.group_send(
                self.home_name,
                {
                    'type': 'new_comments',
                    'num':num,
                    'comment': comment
                }
            )
        elif 'title' in text_data_json:
            title = text_data_json['title']
            content = text_data_json['content']
            votes=0
            # Send message to room group
            await self.channel_layer.group_send(
                self.home_name,
                {
                    'type': 'post_message',
                    'title': title,
                    'content':content,
                    'votes': votes
                }
            )

    # Receive message from room group
    async def post_message(self, event):
        title = event['title']
        content= event['content']
        votes= event['votes']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'title': title,
            'content': content,
            'votes': votes
        }))
    
    # Receive message from room group
    async def new_votes(self, event):
        num= event['num']
        votes= event['votes']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'votes': votes,
            'num': num
        }))

    async def new_comments(self, event):
        num= event['num']
        comment= event['comment']

        await self.send(text_data= json.dumps({
            'num':num,
            'comment':comment
        }))