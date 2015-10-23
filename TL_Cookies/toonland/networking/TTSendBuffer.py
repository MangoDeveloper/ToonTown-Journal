########################## THE TOON LAND DLC ##########################
# Filename: TTSendBuffer.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the sending of messages to all clients interested in the
# local avatar's location zone.
####

from random import randrange
from toontown.toon import LocalToon
from toontown.toon.LocalToon import globalClockDelta
from direct.distributed import DistributedNode
from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, SoundInterval
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from types import StringType

class TTSendBuffer:

    __ClientHeader = 'xTL'
    __FormatMessage = 'timestamp=%d|message=%s'

    def __init__(self):
        self._d_setParent = LocalToon.LocalToon.d_setParent
        LocalToon.LocalToon.d_setParent = lambda *x:self.d_setParent(*x)

    def d_setParent(self, newSelf, parentToken):
        if type(parentToken) == StringType:
            Parallel(Func(self._d_setParent, newSelf, parentToken),
             Func(self._d_setParent, newSelf, 2)).start()
        else:
            return self._d_setParent(newSelf, parentToken)

    def getClientHeader(self):
        clientHeader = self.__ClientHeader
        for iteration in range(4):
            clientHeader += chr(randrange(256))
        return clientHeader

    def getFormattedDatagram(self, datagram):
        message = datagram.getMessage()
        datagram = PyDatagram()
        datagram.addUint32(base.localAvatar.doId)
        datagram.appendData(message)
        return datagram.getMessage()

    def sendDatagram(self, datagram):
        data = self.getFormattedDatagram(datagram)
        message = self.getClientHeader()
        timestamp = globalClockDelta.getRealNetworkTime()
        message += HackerCrypt.encrypt(self.__FormatMessage % (timestamp, repr(data)))
        base.localAvatar.d_setParent(message)