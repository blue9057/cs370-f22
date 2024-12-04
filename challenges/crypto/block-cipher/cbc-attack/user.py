# A user object
class User(object):
    def __init__(self):
        # it has 5 fields
        self.uid = 0
        self.username = 'unknown'
        self.password = 'idont know'
        self.message = 'None'
        self.is_admin = 0

    def __str__(self):
        # a serialization function
        # [uid (16b)][username (16b)][password (16b)][message (48b)][is_admin (8b)]

        # 16 digit integer
        uid = "%016d" % self.uid
        # 16 byte string username
        username = "%16s" % self.username
        # 16 byte string password
        password = "%16s" % self.password
        # 48 byte string message
        message = "%48s" % self.message
        # 16 byte integer
        is_admin = "%016d" % self.is_admin
        # concatenate all!
        result = uid + username + password + message + is_admin
        return result

    def load(self, string_data):
        # load as int
        self.uid = int(string_data[0:16])
        # strip, ignore something after newline
        self.username = string_data[16:32].strip()
        self.password = string_data[32:48].strip()
        self.message = string_data[48:96]
        self.is_admin = int(string_data[96:])

