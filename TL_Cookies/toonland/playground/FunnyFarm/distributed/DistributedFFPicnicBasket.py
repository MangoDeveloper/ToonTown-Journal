########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedFFPicnicBasket.py
# Created by: Cody/Fd Green Cat Fd (August 2nd, 2013)
####
# Description:
#
# This is the server-side code for the picnic tables in Funny Farm.
####

from toontown.safezone import DistributedPicnicBasket
from toontown.toon.LocalToon import globalClockDelta

class DistributedFFPicnicBasket(DistributedPicnicBasket.DistributedPicnicBasket):

    # This distributed object is a little weird, because we're inheriting a Disney distributed object.
    # In order to make this compatible, we'll need to use both base.cr, and ToonLandRepository.ToonLandRepository...
    # Which is why we are re-writing the sendUpdate method.

    def __init__(self, tlr):
        DistributedPicnicBasket.DistributedPicnicBasket.__init__(self, tlr)
        self.tlr = tlr
        self.cr = base.cr
        self.fullSeat2doId = ([0] * 4)

    def sendUpdate(self, fieldName, args=[], sendToId=None):
        self.tlr.send(self.dclass.clientFormatUpdate(fieldName, sendToId or self.doId, args))

    def handleEnterPicnicTable(self, i):
        if not self.fullSeat2doId[i]:
            self.b_setAvatarState(i, 1)

    def handleExitButton(self):
        if base.localAvatar.doId in self.fullSeat2doId:
            self.b_setAvatarState(self.fullSeat2doId.index(base.localAvatar.doId), 0)
            self.clockNode.hide()

    def doneExit(self, avId):
        self.handleExitButton()

    def d_setClockTime(self, receiverId, clockTime):
        self.sendUpdate('setClockTime', [base.localAvatar.doId, receiverId, clockTime])

    def setClockTime(self, senderId, receiverId, clockTime):
        if (senderId in self.fullSeat2doId) and (receiverId == base.localAvatar.doId):
            self.clockNode.countdown(clockTime, self.handleExitButton)

    def b_setAvatarState(self, slotIndex, isBoarded):
        self.setAvatarState(base.localAvatar.doId, slotIndex, isBoarded)
        self.d_setAvatarState(slotIndex, isBoarded)

    def d_setAvatarState(self, slotIndex, isBoarded):
        self.sendUpdate('setAvatarState', [base.localAvatar.doId, slotIndex, isBoarded])

    def setAvatarState(self, avId, slotIndex, isBoarded):
        if isBoarded:
            if self.fullSeat2doId[slotIndex]:
                return None
            if not self.clockNode.currentTime:
                self.fsm.request('waitCountdown', [globalClockDelta.getFrameNetworkTime()])
            if avId != base.localAvatar.doId:
                base.cr.doId2do.get(avId).setPos(self.tablecloth.getPos())
            self.fullSeat2doId[slotIndex] = avId
            self.fillSlot(slotIndex, avId)
        else:
            if self.fullSeat2doId[slotIndex] != avId:
                return None
            if avId == base.localAvatar.doId:
                base.cr.playGame.getPlace().trolley.disableExitButton()
            self.fullSeat2doId[slotIndex] = 0
            ts = globalClockDelta.getFrameNetworkTime()
            if self.fullSeat2doId == ([0] * 4):
                self.clockNode.stop()
                self.clockNode.reset()
                self.setState('waitEmpty', self.seed, ts)
            self.emptySlot(slotIndex, avId, ts)