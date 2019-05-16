import re
import datetime

"""
    Chứa các  hàm kiểm tra thông tin truyền vào, 
    các regex câu hỏi, câu yêu cầu của client so với các câu trong script
"""


def check_start_question(input, question):
    return len(re.findall(question, input)) != 0


def check_choose(input, choose):
    return len(re.findall(choose, input)) != 0


def check_number_int(x):
    x = str(x)
    for c in x:
        if not c.isdecimal():
            return False
    return True


def check_string(input):
    return input is not None and len(input) != 0


def check_date(input):
    try:
        datetime.datetime.strptime(input, '%d-%m-%Y')
    except ValueError:
        try:
            datetime.datetime.strptime(input, '%d/%m/%Y')
        except ValueError:
            try:
                datetime.datetime.strptime(input, '%d,%m,%Y')
            except ValueError:
                return False
    return True


def check_time(input):
    re.match("..:..", input)
    return True


def check_input_type(input, input_type):
    if input_type == "<NUMBER>":
        return check_number_int(input)
    if input_type == "<ADDRESS>":
        return check_string(input)
    if input_type == "<DATE>":
        return check_date(input)
    if input_type == "<TIME>":
        return check_time(input)
    return True
