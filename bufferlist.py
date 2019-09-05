class Buffer_List():

    def __init__(self):
        # format of buffer is {channel ID: [(message ID, message content)]}
        self._buff = {}
        self._num_elements = 9

    def checker(f):
        def wrapper(*args):
            self = args[0]
            cid = args[1]
            if cid not in self._buff:
                self._buff[cid] = []
            return f(self, cid, *args[2:])
        return wrapper

    @checker
    def insert(self, cid, element):
        self._buff[cid].append(element)
        self._buff[cid] = self._buff[cid][:self._num_elements - 1]

    @checker
    def get(self, cid, i):
        # i=0 is same as i=1, so set i=1 if i=0
        i = 1 if not i else i
        try:
            # ignore message ID in the tuple
            # element at index 0 is the oldest
            return self._buff[cid][-i][1]
        except IndexError:
            # if there are not enough elements in the buffer
            return ''

    @checker
    def is_non_zero(self, cid):
        return self._buff[cid]

    @checker
    def remove(self, cid, message_id):
        for i in range(len(self._buff[cid])):
            if message_id in self._buff[i]:
                del self._buff[i]
                return

    def __str__(self):
        return str(self._buff)
