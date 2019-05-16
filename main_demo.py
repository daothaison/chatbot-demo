from static import *
from bot import Bot


def start_conversation():
    chat_bot = Bot()
    print(chat_bot.speak(START_CONVERSATION_SENTENCE))
    while True:
        ans = chat_bot.next_sentence()
        print(ans)
        if ans is None:
            break


def main():
    while True:
        print("=========================================================")
        start_conversation()


if __name__ == "__main__":
    main()
