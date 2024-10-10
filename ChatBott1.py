import random
import re

class ChatBot:
    negative_res = ("nothing", "nope", "not", "sorry", "never")
    exit_commands = ("goodbye", "quit", "stop", "bye", "farewell", "exit")

    def __init__(self):
        self.chat_responses = {
            'about_product': r'.*\s*product.*',
            'technical_help': r'.*technical * help.*',
            'about_returns': r'.*\s*return policy.*',
            'about_refund': r'.*\s*refund.*',
            'general_query': r'.*thank * you.*',
        }

    def greet(self): 
        self.name = input("Bot: Hey!!Welcome to our Help Centre.What's your name?\n")
        will_help = input(f"Bot: Hey {self.name},What can I help you with?\n")
        if will_help in self.negative_res:
            print(f"Alright {self.name},have a great day.")
            return
        self.chat()

    def exit(self, reply): 
        for command in self.exit_commands:
            if command in reply:
                print("Thank you for your time.have a good day.")
                return True
            return False 

    def chat(self):
        reply = input("Bot: Kindly tell me your query:").lower()
        while not self.exit(reply):
            reply = input(self.match_reply(reply))

    def match_reply(self, reply):
        for intent, regex_pattern in self.chat_responses.items():
            match_found = re.search(regex_pattern, reply)
            if match_found and intent == 'about_product':
                return self.about_product()
            elif match_found and intent == 'technical_help':
                return self.technical_help()
            elif match_found and intent == 'about_returns':
                return self.about_returns()
            elif match_found and intent == 'about_refund':
                return self.about_refund()
            elif match_found and intent == 'general_query':
                return self.general_query()
        return self.no_match_found()

    def about_product(self):
        responses = ("Bot: Our product is top-demanded and has excellent reviews from our customers.\n",
                   "Bot: You can find all the details about the product on our website.\n")
        return random.choice(responses)

    def technical_help(self):
        responses = ("Bot: If you need some technical support,then you can visit our technical help page.\n",
                   "Bot: You can also reach our technical helpline for immediate help.\n")
        return random.choice(responses)

    def about_returns(self):
        responses = ("Bot: We have a 10-day return policy.Make sure that the product is in its original state and ready the product receipt.\n",
                   "Bot: Our courier partners will come to pick up the item within 3-5 business days after your return request has been received.\n")
        return random.choice(responses)

    def about_refund(self):
        responses = ("Bot: The refund will be initiated to the same account from which the payment was made within 24-48 hours of us receiving the product back.\n",
                  "Bot: It may take 5 business days for the amount to reflect in your account.\n")
        return random.choice(responses)

    def general_query(self):
        responses = ("Bot: Can I help you with something else?\n",
                   "Bot: Is there anything else?\n")
        return random.choice(responses)

    def no_match_found(self):
        responses=("Bot: Sorry,I am unable to understand that.\n",
               "Bot: I didn't quite understand that.Can you repeat the question again?\n")
        return random.choice(responses)

Bot=ChatBot()
Bot.greet()