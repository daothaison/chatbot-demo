import checker
import services


class Node:
    """
    abstract Node : là một node trong script, set_next, get_next -> chuyển trạng thái trong script
    """
    def __init__(self, raw, chat_bot, type=None, id=-1):
        self.type = type
        self.id = id
        self.next = None
        self.raw = raw
        self.chat_bot = chat_bot
        if type == "input":
            self.raw = self.raw.lower()
        self.id_next = -1
        self.attribute = None

    def set_next(self, id_next):
        self.id_next = id_next

    def set_attribute(self, att=None):
        self.attribute = att

    def get_next(self):
        return self.id_next


class SpeakSentence(Node):
    """
    Node dạng Speak
    """
    def __init__(self, raw, chat_bot):
        super().__init__(raw=raw,  chat_bot=chat_bot, type="speak")
        tmp = raw.split("::")
        self.set_next(int(tmp[len(tmp) - 1]))

    def get_speak_sentence(self):
        ans = self.raw.split("::")[2]
        if self.attribute is not None:
            ans = ans.replace("<ATT>", self.attribute)
        return ans


class ChooseSentence(Node):
    """
    Node dạng Chọn yêu cầu
    """
    def __init__(self, raw, chat_bot, type="choose"):
        super().__init__(raw=raw, chat_bot=chat_bot,type=type)
        self.list_chooses = []
        tmp = raw.split("::")[2:len(raw)]
        # print(raw)
        for i in range(0, len(tmp), 3):
            self.list_chooses.append((tmp[i], tmp[i+1], int(tmp[i + 2])))

    def select_a_choose(self, input):
        for choose in self.list_chooses:
            if checker.check_choose(input, choose[1]):
                self.set_next(choose[2])
                return choose[0]
        return None


class InputSentence(Node):
    """
    Node dạng nhập input
    """
    def __init__(self, raw, chat_bot):
        super().__init__(raw=raw, chat_bot=chat_bot, type="input")
        self.input_type = "<NONE>"
        tmp = raw.split("::")
        self.set_next(int(tmp[len(tmp) - 1]))
        self.input_value(tmp[2])

    def input_value(self, value=""):
        self.input_type = value

    def check_input(self, input):
        return checker.check_input_type(input, self.input_type)


class MainQuestion(Node):
    """
    Node dạng câu hỏi từ Bot
    """
    def __init__(self, raw, chat_bot):
        super().__init__(raw=raw, chat_bot=chat_bot, type="start")
        tmp = raw.split("::")
        self.question = tmp[2]
        self.set_next(int(tmp[len(tmp) - 1]))

    def check_question(self, input):
        if self.question is None:
            return False
        return checker.check_start_question(input, self.question)


class SolveCase(Node):
    """
    Node solve: Bot xử lý thông tin, và tính toán
    """
    def __init__(self, raw, chat_bot):
        super().__init__(raw, chat_bot=chat_bot, type="solve")
        tmp = raw.split("::")
        self.func = tmp[2]
        tmp = raw.split("::")[3:len(raw)]
        self.list_answers = []
        for i in range(0, len(tmp), 2):
            self.list_answers.append((tmp[i], int(tmp[i + 1])))

    def save_number_phone(self):
        number_phone = self.attribute
        ans, value = services.save_number_phone(number_phone)
        for x in self.list_answers:
            if x[0] == ans:
                self.set_next(x[1])
                self.chat_bot.user.set_phone(number_phone)
                return value

    def save_address(self):
        ans, value = services.save_address(self.chat_bot.user_phone, self.attribute)
        self.set_next(self.list_answers[0][1])
        self.chat_bot.user.set_address()
        return value

    def save_date(self):
        self.chat_bot.user.date_meet = self.attribute
        self.set_next(self.list_answers[0][1])
        return "OK"

    def save_time(self):
        self.chat_bot.user.time_meet = self.attribute
        self.set_next(self.list_answers[0][1])
        return "OK"

    def check_info(self):
        value = services.get_address(self.chat_bot.user.phone)
        self.set_next(self.list_answers[0][1])
        return value

    def show_meet_time(self):
        ans = self.chat_bot.user.time_meet + " ngày " + self.chat_bot.user.date_meet
        self.set_next(self.list_answers[0][1])
        return ans

    def show_request(self):
        ans = ">> Thông tin về " + self.chat_bot.user.request + ""
        if self.attribute is None:
            ans = ans + " tổng quát"
        else:
            ans = ans + " tại " + self.attribute
        self.set_next(self.list_answers[0][1])
        return ans

    def solve(self):
        if self.func == "<SAVE_NUMBER_PHONE>":
            return self.save_number_phone()
        elif self.func == "<SAVE_ADDRESS>":
            return self.save_address()
        elif self.func == "<CHECK_INFO>":
            return self.check_info()
        elif self.func == "<SHOW_REQUEST>":
            return self.show_request()
        elif self.func == "<SAVE_DATE>":
            return self.save_date()
        elif self.func == "<SAVE_TIME>":
            return self.save_time()
        elif self.func == "<SHOW_MEET_TIME>":
            return self.show_meet_time()
        else:
            pass
