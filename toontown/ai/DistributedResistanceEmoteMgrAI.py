from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from otp.otpbase.OTPLocalizerEnglish import EmoteFuncDict
RESIST_INDEX = EmoteFuncDict['Resistance Salute']

class DistributedResistanceEmoteMgrAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedResistanceEmoteMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ResistanceFSM')
        self.air = air

    def enterOff(self):
        self.requestDelete()

    def addResistanceEmote(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av: return
        av.emoteAccess[RESIST_INDEX] = 1
        av.d_setEmoteAccess(av.emoteAccess)
