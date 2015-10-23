from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.ai import DistributedPolarPlaceEffectMgrAI

class BRHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.TheBrrrgh

    def createZone(self):
        SZHoodAI.createZone(self)

        self.polarPlaceEffectManager = DistributedPolarPlaceEffectMgrAI.DistributedPolarPlaceEffectMgrAI(self.air)
        self.polarPlaceEffectManager.generateWithRequired(3821)

        self.spawnObjects()
