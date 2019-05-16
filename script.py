from static import *
from node import MainQuestion, SpeakSentence, InputSentence, SolveCase, ChooseSentence


def get_type(raw):
    tmp = raw.split("::")
    return tmp[1]

class Script:
    """
    Quản lý list_node -> kịch bản người dùng, chuyển trạng thái từ node này sang node khác
    """
    def __init__(self, chat_bot):
        file_script = open(SCRIPT_FILE, "r")
        self.list_node = []
        self.chat_bot = chat_bot
        for line in file_script:
            raw_node = line[0:len(line) - 1]
            # print(raw_node)
            type = get_type(raw_node)
            if type == "start":
                node = MainQuestion(raw_node, chat_bot=chat_bot)
            elif type == "speak":
                node = SpeakSentence(raw_node, chat_bot=chat_bot)
            elif type == "input":
                node = InputSentence(raw_node, chat_bot=chat_bot)
            elif type == "solve":
                node = SolveCase(raw_node, chat_bot=chat_bot)
            else:
                node = ChooseSentence(raw_node, chat_bot=chat_bot, type=type)
            self.list_node.append(node)
        self.id_now = 0

    def get_start_node(self):
        if len(self.list_node) == 0:
            return None
        return self.list_node[0]

    def get_node(self):
        if self.id_now == -1:
            return None
        return self.list_node[self.id_now]

    def next_node(self, attribute=None):
        self.id_now = self.list_node[self.id_now].get_next()
        if self.get_node() is not None:
            self.get_node().set_attribute(attribute)

    def reset(self):
        self.__init__(self)
