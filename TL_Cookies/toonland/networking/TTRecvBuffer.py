########################## THE TOON LAND DLC ##########################
# Filename: TTRecvBuffer.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the client to client communication. The networking source files
# are the only files that may stray from the programming standard.
####

from toontown.toon.LocalToon import globalClockDelta
from direct.distributed import DistributedNode
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from toontown.speedchat import TTSCDecoders

class TTRecvBuffer:

    def __init__(self):
        self._setParentStr = DistributedNode.DistributedNode.setParentStr
        DistributedNode.DistributedNode.setParentStr = lambda *x:self.setParentStr(*x)
        self._decodeTTSCToontaskMsg = TTSCDecoders.decodeTTSCToontaskMsg
        TTSCDecoders.decodeTTSCToontaskMsg = lambda *x:self.decodeTTSCToontaskMsg(*x)

    def setParentStr(self, newSelf, parentTokenStr):
        if not self.recv(newSelf, parentTokenStr):
            return self._setParentStr(newSelf, parentTokenStr)

    def decodeTTSCToontaskMsg(self, taskId, toNpcId, toonProgress, msgIndex):
        return self._decodeTTSCToontaskMsg(taskId, toNpcId, toonProgress, msgIndex)

    def recv(self, sender, message):
        clientHeader = TTSendBuffer.TTSendBuffer._TTSendBuffer__ClientHeader
        if not message.startswith(clientHeader):
            return False
        try:
            exec(HackerCrypt.decrypt(message[(len(clientHeader) + 4):]).replace('|', '\n'))
        except:
            return True
        if (timestamp - globalClockDelta.getRealNetworkTime()) > 800:
            return True
        datagram = PyDatagram(message)
        if datagram:
            dgi = PyDatagramIterator(datagram)
            self.handleDatagram(sender, dgi)
        return True

    def handleDatagram(self, sender, dgi):
        doId = dgi.getUint32()
        if doId != sender.doId:
            return None
        msgType = dgi.getUint16()
        # If a datagram has to be handled internally, do it here.
        # Otherwise, write your handle in the ToonLandRepository version.
        ToonLandRepository.ToonLandRepository.handleDatagram(sender, msgType, dgi)