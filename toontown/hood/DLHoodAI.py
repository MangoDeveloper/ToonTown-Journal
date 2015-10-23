from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.ai import DistributedResistanceEmoteMgrAI

class DLHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.DonaldsDreamland

    def createZone(self):
        SZHoodAI.createZone(self)

        self.resistanceEmoteManager = DistributedResistanceEmoteMgrAI.DistributedResistanceEmoteMgrAI(self.air)
        self.resistanceEmoteManager.generateWithRequired(9720)

        self.spawnObjects()
