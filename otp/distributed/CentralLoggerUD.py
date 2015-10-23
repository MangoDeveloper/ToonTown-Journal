from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

class CentralLoggerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("CentralLoggerUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)   
             
    def sendMessage(self, category, description, sender, receiver):
        try:
            self.air.csm.accountDB.persistMessage(category, description, sender, receiver)
            self.air.writeServerEvent(category, sender, receiver, description)
        except:
            self.notify.warning('exception in CentralLoggerUD')
            
    def logAIGarbage(self):
        pass

