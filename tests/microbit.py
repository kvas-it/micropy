# Microbitm module mock.


def sleep(millis):
    pass


class Image:
    def __init__(self, data):
        self.data = data


Image.HAPPY = Image('happy')
Image.ARROW_W = Image('arrow_w')
