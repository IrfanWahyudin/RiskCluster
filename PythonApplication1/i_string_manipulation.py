class stringmanipulation(object):
    """description of class"""
    def left(self, s, amount):
        return s[:amount]

    def right(self, s, amount):
        return s[-amount:]

    def mid(self, s, offset, amount):
        return s[offset:offset+amount]


