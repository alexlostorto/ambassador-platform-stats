import requests

from src.credentials import getCredentials
from src.config import getJSON
from src.inputs import chooseOptions


class Stats():
    def __init__(self):
        self.textToFind = ""
        self.totalMessages = 0
        self.totalTextCount = 0
        self.statistics = {"users": {}, "stats": {}, "words": {}}
        self.options = {
            'daily-messages': False,
            'text-count': False
        }
        self.countOptions = {
            'order': 'desc',
            'order-by': 'id',
            'limit': 200,
            'before-message': '',
        }
        chooseOptions(self.options)

    def getURL(self):
        url = self.config.get('url')
        url = url.replace("{DIALOG}", self.dialog)
        url = url.replace("{ORDER}", self.countOptions.get('order'))
        url = url.replace("{ORDER_BY}", self.countOptions.get('order-by'))
        url = url.replace("{LIMIT}", str(self.countOptions.get('limit')))
        url += "&beforeMessageId=" + str(self.countOptions.get('before-message')) if self.countOptions.get('before-message') else ""
        return url

    def getMessages(self):
        self.token, self.dialog = getCredentials()
        self.config = getJSON()
        self.method = self.config.get('method')
        self.headers = self.config.get('headers')
        self.headers.update({"Authorization": f"Bearer {self.token}"})

        self.messages = []
        
        while True:
            r = requests.get(url=self.getURL(), headers=self.headers)
            if r.status_code == 200:
                response = r.json()
                self.messages.extend(response['data']['messages'])
                print(f"[LOG] {len(response['data']['messages'])} messages added")
                if len(self.messages) >= response['data']['total']:
                    break
                self.countOptions['before-message'] = response['data']['messages'][-1]['id']
            else:
                print(f"[ERROR] {r.status_code}")
                print(f"[ERROR] {r.text}")
                break

    def countMessages(self):
        self.getMessages()
        self.longestMessage = {"length": 0, "message": ""}
        self.shortestMessage = {"length": float('inf'), "message": ""}

        if self.options['text-count']:
            self.textToFind = input("Text to count: ")

        for message in self.messages:
            date = message.get('created_at')[0:10]
            userID = message.get('user').get('id')
            username = message.get('user').get('name')
            message = message.get('content').get('text')

            if not username or not message:
                print(f"[ERROR] username or message not found.")
                continue

            if userID not in self.statistics['users']:
                self.statistics['users'][userID] = username

            if date not in self.statistics['stats']:
                self.statistics['stats'][date] = {"messages": {}, "text": {}, "words": {}}

            words = len(message.split(' '))
            self.longestMessage = {"length": words, "message": message} if self.longestMessage["length"] < words else self.longestMessage
            self.shortestMessage = {"length": words, "message": message} if self.shortestMessage["length"] > words else self.shortestMessage
            self.statistics['stats'][date]['messages'][userID] = self.statistics['stats'][date]['messages'].get(userID, 0) + 1
            self.statistics['stats'][date]['words'][userID] = self.statistics['stats'][date]['words'].get(userID, 0) + words

            if self.options['text-count'] and self.textToFind.lower() in message.lower():
                self.statistics['stats'][date]['text'][userID] = self.statistics['stats'][date]['text'].get(userID, 0) + 1

        self.printStatistics()

    def printStatistics(self):
        self.printDailyMessages()

        print("\n---TOTAL MESSAGES---")
        self.printTotalMessagesPerUser()
        self.printTotalMessages()
        self.printTotalTextPerUser()
        self.printTotalText()
        print("\n---TOTAL WORDS---")
        self.printTotalWordsPerUser()
        self.printTotalWords()
        # self.printMessageLengths()
        print("\n---MOST COMMON WORDS---")
        self.printMostCommonWords(5)
        print("\n---LEAST COMMON WORDS---")
        self.printLeastCommonWords(5)

    def printDailyMessages(self):
        if not self.options['daily-messages']: return
        for date, stats in self.statistics['stats'].items():
            print(f"\n{date}")
            for userID, number in stats['messages'].items():
                print(f"{self.statistics['users'][userID]}: {number: ,}")
            if not self.options['text-count']: continue
            for userID, number in stats['text'].items():
                print(f"Times {self.statistics['users'][userID]} said '{self.textToFind}': {number: ,}")

    def printTotalMessagesPerUser(self):
        for userID, username in self.statistics['users'].items():
            messages = sum(date['messages'].get(userID, 0) for date in self.statistics['stats'].values())
            print(f"{username}: {messages: ,}")

    def printTotalTextPerUser(self):
        if not self.options['text-count']: return
        for userID, username in self.statistics['users'].items():
            messages = sum(date['text'].get(userID, 0) for date in self.statistics['stats'].values())
            print(f"Times {username} said '{self.textToFind}': {messages: ,}")
    
    def printTotalWordsPerUser(self):
        for userID, username in self.statistics['users'].items():
            words = sum(date['words'].get(userID, 0) for date in self.statistics['stats'].values())
            print(f"{username}: {words: ,}")

    def printTotalMessages(self):
        self.totalMessages = sum(sum(date['messages'].values()) for date in self.statistics['stats'].values())
        print(f"Total messages: {self.totalMessages: ,}")
    
    def printTotalText(self):
        if not self.options['text-count']: return
        self.totalText = sum(sum(date['text'].values()) for date in self.statistics['stats'].values())
        print(f"Total times '{self.textToFind}' was said: {self.totalText: ,}")

    def printTotalWords(self):
        self.totalWords = sum(sum(date['words'].values()) for date in self.statistics['stats'].values())
        print(f"Total words: {self.totalWords: ,}")

    def printMessageLengths(self):
        print(f"Shortest message: {self.shortestMessage} words")
        print(f"Longest message: {self.longestMessage} words")

    def printMostCommonWords(self, number):
        for word, count in reversed(sorted(self.statistics['words'].items(), key=lambda item: item[1])[-number:]):
            print(f"{word}: {count}")

    def printLeastCommonWords(self, number):
        for word, count in sorted(self.statistics['words'].items(), key=lambda item: item[1])[:number]:
            print(f"{word}: {count}")
