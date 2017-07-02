from app.models import *


# 用于存放包装类

class Homework:
    workmeta = None
    attachments = None

    def __init__(self, workmeta, attachments):
        self.workmeta = workmeta
        self.attachments = attachments


class ScoreWrapper:
    workmeta=None
    works=None

    def __init__(self,workmeta,works):
        self.workmeta=workmeta
        self.works=works
