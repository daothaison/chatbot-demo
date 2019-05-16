import sys
from script import Script
from flask import jsonify
from static import *
import time
from user import User


class Bot:
    """
    Một Bot sẽ quản lý user, script, trả ra response cho người dùng khi script xử lý thông tin xong
    """
    def __init__(self):
        self.stop = False
        self.user = User()
        self.script = Script(self)
        self.list_speaks = []
        self.born_time = time.time()

    def reset_time(self):
        self.born_time = time.time()

    def check_over_time(self):
        if time.time() - self.born_time > SESSION_LIVE_TIME:
            return True
        return False

    def solved(self, prob, ok):
        pass

    def speak(self, sentence):
        return sentence
        # return jsonify({"answer": sentence})

    def listen(self):
        sentence = sys.stdin.readline()
        sentence = sentence[0:len(sentence) - 1]
        return sentence
        # return jsonify({"answer": sentence})

    def next_sentence(self, input=None):
        script = self.script
        if self.stop:
            return jsonify({"answer": "STOP"})
        node = script.get_node()
        if node is None:
            self.script.reset()
            return self.next_sentence()
        if not node.type == "speak":
            self.list_speaks = []
        if node.type == "speak":
            ans = self.speak(node.get_speak_sentence())
            script.next_node()
            self.list_speaks.append(ans)
            if script.get_node() is None or not script.get_node().type == "speak":
                return self.list_speaks
            return self.next_sentence()
        elif node.type == "start":
            if input is None:
                input = ""
            sentence = input
            if not node.check_question(sentence):
                ans = self.speak(START_CONVERSATION_SENTENCE)
                return ans
            else:
                script.next_node()
        elif node.type == "input":
            if input is None:
                return None
            input = input
            if node.check_input(input):
                script.next_node(input)
            else:
                return self.speak(ERROR_INPUT)
        elif node.type == "solve":
            answer = node.solve()
            self.solved(node.func, answer)
            script.next_node(answer)
        else:
            if input is None:
                return None
            input = node.select_a_choose(input.lower())
            # print(node.type, bot.user_request)
            if input is None:
                return self.speak(ERROR_CHOOSE)
            else:
                input = input
                if node.type == "choose_req":
                    self.user.set_request(self.user.request + (input + "::"))
                script.next_node(input)
        return self.next_sentence()
