

class User:
    def __init__(self):
        self.phone = None
        self.address = ""
        self.date_meet = ""
        self.time_meet = ""
        self.request = ""

    def set_request(self, request):
        self.request = request

    def set_phone(self, phone):
        self.phone = phone

    def set_address(self, address):
        self.address = address

    def set_date_meet(self, date):
        self.date_meet = date

    def set_time_meet(self, t):
        self.time_meet = t
