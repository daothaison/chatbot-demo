from __future__ import print_function
from static import *
import csv

# chứa các hàm solve, xử lý, có thể thay bởi các service khác để lưu trữ xử lý thông tin khách hàng, ở đây đang xử lý thông thường
def save_number_phone(phone):
    if phone is None:
        return "NEW", ""
    f = open(USER_INFO)
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if row[0] == phone:
            f.close()
            ans = ""
            for col in row:
                ans = ans + str(col) + "\t"
            return "<EXIST>", ans

    fw = open(USER_INFO, mode="a")
    csv_writer = csv.writer(fw)
    csv_writer.writerow([phone, "None"])
    return "<NEW>", ""


def get_address(phone):
    print(phone)
    if phone is None:
        return None
    f = open(USER_INFO)
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if row[0] == phone:
            print(row[1])
            f.close()
            return str(row[1])
    return None


def save_address(phone, address):
    f = open(USER_INFO, "r")
    csv_reader = csv.reader(f, delimiter=',')
    list_rows = []
    for row in csv_reader:
        if row[0] == phone:
            row[1] = address
        list_rows.append(row)
    f.close()
    f = open(USER_INFO, "w")
    csv_writer = csv.writer(f, delimiter=',')
    for row in list_rows:
        csv_writer.writerow(row)
    f.close()
    return "OK"
