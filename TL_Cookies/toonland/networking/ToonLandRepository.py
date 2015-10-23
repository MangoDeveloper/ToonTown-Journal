########################## THE TOON LAND DLC ##########################
# Filename: ToonLandRepository.py
# Created by: Cody/Fd Green Cat Fd (August 1st, 2013)
####
# Description:
#
# Handles the send and receive buffers. This should be where most of the
# datagram handles are, as well.
####

from pandac.PandaModules import *
from types import *
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DoCollectionManager import DoCollectionManager
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from toontown.distributed import ToontownClientRepository

class ToonLandRepository(DoCollectionManager):

    notify = DirectNotifyGlobal.directNotify.newCategory('ToonLandRepository')

    def __doUpdate(self, doId, di, ovUpdated):
        do = self.doId2do.get(doId)
        if do is not None:
            do.dclass.receiveUpdate(do, di)

    def _getMsgName(self, msgId):
        return MsgId2Names.get(msgId, 'UNKNOWN MESSAGE: %s' % msgId)[0]

    def _logFailedDisable(self, doId):
        self.notify.warning('Disable failed. DistObj ' + `doId` + ' is not in dictionary')

    def _addDelayDeletedDO(self, do):
        key = id(do)
        assert key not in self._delayDeletedDOs
        self._delayDeletedDOs[key] = do

    def _removeDelayDeletedDO(self, do):
        key = id(do)
        del self._delayDeletedDOs[key]

    def __init__(self, sendBuffer, recvBuffer, dcFileNames=[]):
        DoCollectionManager.__init__(self)
        globals().update(ToonLandMsgTypes.__dict__) # HACK
        self.sendBuffer = sendBuffer
        self.recvBuffer = recvBuffer
        self.dcFile = DCFile()
        self.readDCFile(dcFileNames)
        self.doIdBase = self.doIdLast = 800000000 # The doId range for Toon Land clients.
        self.doIdAllocator = UniqueIdAllocator(self.doIdBase, self.doIdLast )#- 1)
        self.deferredGenerates = []
        self.deferredDoIds = {}
        self.setDeferInterval(base.config.GetDouble('deferred-generate-interval', 0.2))
        self.noDefer = False
        self.lastGenerate = 0
        self.bootedIndex = None
        self.bootedText = None
        self._delayDeletedDOs = {}
        self.specialNameNumber = 0
        self.playGame = base.cr.playGame
        self._sendSetZoneMsg = ToontownClientRepository.ToontownClientRepository.sendSetZoneMsg
        ToontownClientRepository.ToontownClientRepository.sendSetZoneMsg = lambda *x:self.sendSetZoneMsg(*x)

    def send(self, datagram):
        if not datagram.getLength() > 0:
            return None
        self.sendBuffer.sendDatagram(datagram)

    def handleDatagram(self, sender, msgType, dgi):
        if self.notify.getDebug():
            print 'ClientRepository received datagram:'
            dgi.getDatagram().dumpHex(ostream)
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            self.handleGenerate(dgi)
        elif msgType == CLIENT_OBJECT_UPDATE_FIELD:
            self.handleUpdateField(dgi)
        elif msgType == CLIENT_OBJECT_DISABLE:
            self.handleDisable(dgi)
        elif msgType == REQUEST_GENERATES_CMU:
            self.handleRequestGenerates(dgi)
        else:
            self.handleMessageType(msgType, dgi)
        base.cr.considerHeartbeat() # We need to be sure our ToonTown
        # client is still sending updates to the Disney server so we aren't booted.

    def handleMessageType(self, msgType, di):
        self.notify.error('unrecognized message type ' + `msgType`)

    def sendSetZoneMsg(self, newSelf, zoneId, visibleZoneList=None):
        for doId in self.doId2do.copy():
            self.deleteObject(doId)
        returnCode = self._sendSetZoneMsg(newSelf, zoneId, visibleZoneList)
        datagram = PyDatagram()
        datagram.addUint16(REQUEST_GENERATES_CMU)
        datagram.addUint32(base.localAvatar.getZoneId())
        self.send(datagram)
        return returnCode

    def readDCFile(self, dcFileNames):
        self.dcFile.clear()
        self.dclassesByName = {}
        self.dclassesByNumber = {}
        self.hashVal = 0
        if isinstance(dcFileNames, StringType):
            dcFileNames = [dcFileNames]
        for dcFileName in dcFileNames:
            pathName = (__modulebase__ + '/etc/' + dcFileName)
            readResult = self.dcFile.read(pathName)
            if not readResult:
                self.notify.error('Could not read DC file: ' + pathName)
        self.hashVal = self.dcFile.getHash()
        dcImports = {}
        for n in range(self.dcFile.getNumImportModules()):
            moduleName = self.dcFile.getImportModule(n)[:].split('/', 1)[0]
            importSymbols = []
            for i in range(self.dcFile.getNumImportSymbols(n)):
                symbolName = self.dcFile.getImportSymbol(n, i).split('/', 1)[0]
                importSymbols.append(symbolName)
            self.importModule(dcImports, moduleName, importSymbols)
        for i in range(self.dcFile.getNumClasses()):
            dclass = self.dcFile.getClass(i)
            number = dclass.getNumber()
            className = dclass.getName()
            classDef = dcImports.get(className)
            if not classDef:
                try:
                    classDef = eval('.'.join([className] * 2))
                except:
                    pass
            if not classDef:
                self.notify.debug('No class definition for %s.' % className)
            else:
                if type(classDef) == ModuleType:
                    if not hasattr(classDef, className):
                        self.notify.warning('Module %s does not define class %s.' % (className, className))
                        continue
                    classDef = getattr(classDef, className)
                if (type(classDef) != ClassType) and (type(classDef) != TypeType):
                    self.notify.error('Symbol %s is not a class name.' % className)
                else:
                    dclass.setClassDef(classDef)
            self.dclassesByName[className] = dclass
            if number >= 0:
                self.dclassesByNumber[number] = dclass

    def importModule(self, dcImports, moduleName, importSymbols):
        module = __import__(moduleName, globals(), locals(), importSymbols)
        if importSymbols:
            if importSymbols == ['*']:
                if hasattr(module, '__all__'):
                    importSymbols = module.__all__
                else:
                    importSymbols = module.__dict__.keys()
            for symbolName in importSymbols:
                if hasattr(module, symbolName):
                    dcImports[symbolName] = getattr(module, symbolName)
                else:
                    raise StandardError('Symbol %s not defined in module %s.' % (symbolName, moduleName))
        else:
            dcImports[components[0]] = module

    def hasOwnerView(self):
        return False

    def openAutoInterests(self, obj):
        # We don't use this, but it is called by generate() in each distributed object.
        return None

    def closeAutoInterests(self, obj):
        # We don't use this, but it is called by _deactivateDO() in each distributed object.
        return None

    def handleRequestGenerates(self, dgi):
        zoneId = dgi.getUint32()
        for distObj in self.doId2do.values():
            if distObj.zoneId == zoneId:
                self.resendGenerate(distObj)

    def resendGenerate(self, distObj):
        extraFields = []
        for i in range(distObj.dclass.getNumInheritedFields()):
            field = distObj.dclass.getInheritedField(i)
            if field.hasKeyword('broadcast') and field.hasKeyword('ram') and not field.hasKeyword('required'):
                if field.asMolecularField():
                    continue
                extraFields.append(field.getName())
        self.send(self.formatGenerate(distObj, extraFields))

    def formatGenerate(self, distObj, extraFields):
        return distObj.dclass.clientFormatGenerate(distObj, distObj.doId, distObj.zoneId, extraFields)

    def handleGenerate(self, dgi):
        parentId = dgi.getUint32()
        zoneId = dgi.getUint32()
        classId = dgi.getUint16()
        dclass = self.dclassesByNumber[classId]
        doId = dgi.getUint32()
        distObj = self.doId2do.get(doId)
        if distObj and (distObj.dclass == dclass):
            dclass.receiveUpdateBroadcastRequired(distObj, dgi)
            dclass.receiveUpdateOther(distObj, dgi)
            return None
        self.notify.debug('performing generate for %s %s' % (dclass.getName(), doId))
        dclass.startGenerate()
        distObj = self.generateWithRequiredOtherFields(dclass, doId, dgi, 0, zoneId)
        dclass.stopGenerate()

    def generateWithRequiredFields(self, dclass, doId, dgi, parentId, zoneId):
        if self.doId2do.has_key(doId):
            distObj = self.doId2do[doId]
            assert distObj.dclass == dclass
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredFields(dclass, dgi)
        else:
            classDef = dclass.getClassDef()
            if classDef == None:
                self.notify.error('Could not create an undefined %s object.' % dclass.getName())
            distObj = classDef(self)
            distObj.dclass = dclass
            distObj.doId = doId
            self.doId2do[doId] = distObj
            distObj.generateInit()
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredFields(dclass, dgi)
            print 'New DO:%s, dclass:%s' % (doId, dclass.getName())
        return distObj

    def generateWithRequiredOtherFields(self, dclass, doId, dgi, parentId, zoneId):
        if self.doId2do.has_key(doId):
            distObj = self.doId2do[doId]
            assert distObj.dclass == dclass
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredOtherFields(dclass, dgi)
        else:
            classDef = dclass.getClassDef()
            if classDef == None:
                self.notify.error('Could not create an undefined %s object.' % dclass.getName())
            distObj = classDef(self)
            distObj.dclass = dclass
            distObj.doId = doId
            self.doId2do[doId] = distObj
            distObj.generateInit()
            distObj.generate()
            distObj.setLocation(parentId, zoneId)
            distObj.updateRequiredOtherFields(dclass, dgi)
        return distObj

    def allocateDoId(self):
        return self.doIdAllocator.allocate()

    def reserveDoId(self, doId):
        self.doIdAllocator.initialReserveId(doId)
        return doId

    def freeDoId(self, doId):
        assert self.isLocalId(doId)
        self.doIdAllocator.free(doId)

    def storeObjectLocation(self, object, parentId, zoneId):
        object.parentId = parentId
        object.zoneId = zoneId

    def createDistributedObject(self, className=None, distObj=None,
                                parentId=0, zoneId=0, optionalFields=None, doId=None,
                                reserveDoId=False, sendFormatGenerate=True):
        if not className:
            if not distObj:
                self.notify.error('Must specify either a className or a distObj.')
            className = distObj.__class__.__name__
        if not doId:
            doId = self.allocateDoId()
        elif reserveDoId:
            self.reserveDoId(doId)
        dclass = self.dclassesByName.get(className)
        if not dclass:
            self.notify.error('Unknown distributed class: ' + distObj.__class__)
        classDef = dclass.getClassDef()
        if classDef == None:
            self.notify.error('Could not create an undefined %s object.' % dclass.getName())
        if not distObj:
            distObj = classDef(self)
        if not isinstance(distObj, classDef):
            self.notify.error('Object %s is not an instance of %s' % (distObj.__class__.__name__, classDef.__name__))
        distObj.dclass = dclass
        distObj.doId = doId
        self.doId2do[doId] = distObj
        distObj.generateInit()
        distObj.generate()
        distObj.setLocation(parentId, zoneId)
        distObj.announceGenerate()
        if sendFormatGenerate:
            self.send(self.formatGenerate(distObj, optionalFields))
        return distObj

    def sendDeleteMsg(self, doId):
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_OBJECT_DELETE)
        datagram.addUint32(doId)
        self.send(datagram)

    def setObjectZone(self, distObj, zoneId):
        distObj.b_setLocation(0, zoneId)
        assert distObj.zoneId == zoneId
        self.resendGenerate(distObj)

    def sendSetLocation(self, doId, parentId, zoneId):
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_OBJECT_LOCATION)
        datagram.addUint32(doId)
        datagram.addUint32(parentId)
        datagram.addUint32(zoneId)
        self.send(datagram)

    def isLocalId(self, doId):
        return ((doId >= self.doIdBase) and (doId < self.doIdLast))

    def haveCreateAuthority(self):
        return (self.doIdLast > self.doIdBase)

    def handleUpdateField(self, dgi):
        doId = dgi.getUint32()
        if doId in self.deferredDoIds:
            # The object hasn't been generated yet, wait for a bit to update them.
            args, deferrable, dg0, updates = self.deferredDoIds[doId]
            datagram = PyDatagram(dgi.getDatagram())
            dgi = PyDatagramIterator(datagram, dgi.getCurrentIndex())
            updates.append((datagram, dgi))
        else:
            self.__doUpdate(doId, dgi)

    def handleGoGetLost(self, di):
        if dgi.getRemainingSize() > 0:
            self.bootedIndex = di.getUint16()
            self.bootedText = di.getString()
            self.notify.warning('Server is booting us out (%d): %s' % (
             self.bootedIndex, self.bootedText))
        else:
            self.bootedIndex = None
            self.bootedText = None
            self.notify.warning('Server is booting us out with no explanation.')
        base.cr.lostConnection()

    def handleDisable(self, di):
        while dgi.getRemainingSize() > 0:
            doId = di.getUint32()
            assert not self.isLocalId(doId)
            self.disableDoId(doId)

    def handleDelete(self, di):
        doId = dgi.getUint32()
        self.deleteObject(doId)

    def deleteObject(self, doId):
        if self.doId2do.has_key(doId):
            distObj = self.doId2do[doId]
            del self.doId2do[doId]
            distObj.deleteOrDelay()
            if self.isLocalId(doId):
                self.freeDoId(doId)
        else:
            self.notify.warning('Asked to delete non-existent DistObj ' + `doId`)

    def sendUpdate(self, distObj, fieldName, args):
        self.send(distObj.dclass.clientFormatUpdate(fieldName, distObj.doId, args))

    def setDeferInterval(self, deferInterval):
        self.deferInterval = deferInterval
        if self.deferredGenerates:
            taskMgr.remove('deferredGenerate')
            taskMgr.doMethodLater(self.deferInterval, self.doDeferredGenerate, 'deferredGenerate')

    def specialName(self, label):
        name = 'SpecialName %s %s' % (self.specialNameNumber, label)
        self.specialNameNumber += 1
        return name

    def doGenerate(self, parentId, zoneId, classId, doId, dgi):
        dclass = self.dclassesByNumber[classId]
        assert(self.notify.debug('performing generate for %s %s' % (dclass.getName(), doId)))
        dclass.startGenerate()
        distObj = self.generateWithRequiredOtherFields(dclass, doId, dgi, parentId, zoneId)
        dclass.stopGenerate()

    def flushGenerates(self):
        while self.deferredGenerates:
            msgType, extra = self.deferredGenerates[0]
            del self.deferredGenerates[0]
            self.replayDeferredGenerate(msgType, extra)
        taskMgr.remove('deferredGenerate')

    def replayDeferredGenerate(self, msgType, extra):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            doId = extra
            if doId in self.deferredDoIds:
                args, deferrable, dg, updates = self.deferredDoIds[doId]
                del self.deferredDoIds[doId]
                self.doGenerate(*args)
                if deferrable:
                    self.lastGenerate = globalClock.getFrameTime()
                for datagram, dgi in updates:
                    if type(dgi) is TupleType:
                        msgType = datagram
                        datagram, dgi = dgi
                        self.replayDeferredGenerate(msgType, (datagram, dgi))
                    else:
                        self.__doUpdate(doId, dgi, True)
        else:
            self.notify.warning('Ignoring deferred message ' + `msgType`)

    def doDeferredGenerate(self, task):
        now = globalClock.getFrameTime()
        while self.deferredGenerates:
            if now - self.lastGenerate < self.deferInterval:
                return Task.again
            msgType, extra = self.deferredGenerates[0]
            del self.deferredGenerates[0]
            self.replayDeferredGenerate(msgType, extra)
        return Task.done

    def disableDoId(self, doId):
        if self.deferredDoIds.has_key(doId):
            del self.deferredDoIds[doId]
            i = self.deferredGenerates.index((CLIENT_CREATE_OBJECT_REQUIRED_OTHER, doId))
            del self.deferredGenerates[i]
            if len(self.deferredGenerates) == 0:
                taskMgr.remove('deferredGenerate')
        else:
            self._logFailedDisable(doId)

    def getObjectsOfClass(self, objClass):
        doDict = {}
        for doId, do in self.doId2do.items():
            if isinstance(do, objClass):
                doDict[doId] = do
        return doDict

    def getObjectsOfExactClass(self, objClass):
        doDict = {}
        for doId, do in self.doId2do.items():
            if do.__class__ == objClass:
                doDict[doId] = do
        return doDict

    def getWorld(self, doId):
        obj = self.doId2do[doId]
        worldNP = obj.getParent()
        while 1:
            nextNP = worldNP.getParent()
            if nextNP == render:
                break
            elif worldNP.isEmpty():
                return None
        return worldNP

    def printDelayDeletes(self):
        print 'DelayDeletes:'
        print '============='
        for obj in self._delayDeletedDOs.itervalues():
            print '%s\t%s (%s)\tdelayDeletes=%s' % (obj.doId, safeRepr(obj), itype(obj), obj.getDelayDeleteNames())