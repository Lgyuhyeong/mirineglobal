#크롤링 에러 관리하는 클래스

class StockException(Exception):
    def __init__(self, msg_type, msg):
        self.msg_type = msg_type
        self.msg = msg

    def __str__(self):
        #에러메세지 가공
        return self.msg_type + self.msg