
from bncs.buffer import DataBuffer, DataReader, format_buffer


# Standard BNLS packet constants
BNLS_NULL = 0x00
BNLS_CDKEY = 0x01
BNLS_LOGONCHALLENGE = 0x02
BNLS_LOGONPROOF = 0x03
BNLS_CREATEACCOUNT = 0x04
BNLS_CHANGECHALLENGE = 0x05
BNLS_CHANGEPROOF = 0x06
BNLS_UPGRADECHALLENGE = 0x07
BNLS_UPGRADEPROOF = 0x08
BNLS_VERSIONCHECK = 0x09
BNLS_CONFIRMLOGON = 0x0A
BNLS_HASHDATA = 0x0B
BNLS_CDKEY_EX = 0x0C
BNLS_CHOOSENLSREVISION = 0x0D
BNLS_AUTHORIZE = 0x0E
BNLS_AUTHORIZEPROOF = 0x0F
BNLS_REQUESTVERSIONBYTE = 0x10
BNLS_VERIFYSERVER = 0x11

BNLS_RESERVESERVERSLOTS = 0x12
BNLS_SERVERLOGONCHALLENGE = 0x13
BNLS_SERVERLOGONPROOF = 0x14
BNLS_VERSIONCHECKEX = 0x18
BNLS_VERSIONCHECKEX2 = 0x1A

# Non-standard packets (may not be supported on all servers)
BNLS_WARDEN = 0x7D
BNLS_IPBAN = 0xFF


class BnlsPacket(DataBuffer):
    def __init__(self, packet_id):
        self.id = packet_id
        super().__init__()

    def __len__(self):
        return super().__len__() + 3

    def __str__(self):
        return format_buffer(self.get_data())

    def get_data(self):
        pak = DataBuffer()
        pak.insert_word(self.__len__())
        pak.insert_byte(self.id)
        pak.insert_raw(self.data)
        return pak.data


class BnlsReader(DataReader):
    def __init__(self, data):
        if len(data) < 3:
            raise ValueError("Packet data must contain at least 3 bytes.")

        super().__init__(data)
        self.length = self.get_word()
        self.id = self.get_byte()

    def __len__(self):
        return self.length

    @property
    def actual_length(self):
        return super().__len__()

    def append(self, data):
        if self.actual_length + len(data) > self.length:
            raise ValueError("Message length exceeded.")
        self.data += data

    def is_full_packet(self):
        return self.length == self.actual_length
