import re

# x = "(.*?<!không)(có|được|đồng ý|nhất trí).*?"
# y = "tôi có được"
# print(re.match(x, y))


a = "hello<ATT>ass"
print(a.replace("<ATT>","dmm"))