from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals

# Import the Catalog
from toontown.catalog import CatalogItem
from toontown.catalog.CatalogItemList import CatalogItemList
from toontown.catalog.CatalogPoleItem import CatalogPoleItem
from toontown.catalog.CatalogBeanItem import CatalogBeanItem
from toontown.catalog.CatalogChatItem import CatalogChatItem
from toontown.catalog.CatalogClothingItem import CatalogClothingItem, getAllClothes
from toontown.catalog.CatalogAccessoryItem import CatalogAccessoryItem
from toontown.catalog.CatalogRentalItem import CatalogRentalItem
from toontown.catalog.CatalogInvalidItem import CatalogInvalidItem

import time

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTCodeRedemptionMgrAI")

    # Contexts
    Success = 0
    InvalidCode = 1
    ExpiredCode = 2
    Ineligible = 3
    AwardError = 4
    TooManyFails = 5
    ServiceUnavailable = 6

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def delete(self):
        DistributedObjectAI.delete(self)



    def redeemCode(self, context, code):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Tried to redeem a code from an invalid avId')
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Invalid avatar tried to redeem a code')
            return

        # Some constants
        valid = True
        eligible = True
        expired = False
        delivered = False

        # Get our redeemed codes
        codes = av.getRedeemedCodes()
        print codes
        if not codes:
            codes = [code]
            av.setRedeemedCodes(codes)
        else:
            if not code in codes:
                codes.append(code)
                av.setRedeemedCodes(codes)
                valid = True
            else:
                valid = False

        # Is the code valid?
        if not valid:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Invalid code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
            return

        # Did our code expire?
        if expired:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Expired code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.ExpiredCode, 0])
            return

        # Are we able to redeem this code?
        if not eligible:
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Ineligible for code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.Ineligible, 0])
            return

        # Iterate over these items and deliver item to player
        items = self.getItemsForCode(code)
        for item in items:
            if isinstance(item, CatalogInvalidItem): # Umm, u wot m8?
                self.air.writeServerEvent('suspicious', avId=avId, issue='Invalid CatalogItem\'s for code: %s' % code)
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
                break

            if len(av.mailboxContents) + len(av.onGiftOrder) >= ToontownGlobals.MaxMailboxContents:
                # Mailbox is full
                delivered = False
                break

            item.deliveryDate = int(time.time() / 60) + 1 # Let's just deliver the item right away.
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            delivered = True

        if not delivered:
            # 0 is Success
            # 1, 2, 15, & 16 is an UnknownError
            # 3 & 4 is MailboxFull
            # 5 & 10 is AlreadyInMailbox
            # 6, 7, & 11 is AlreadyInQueue
            # 8 is AlreadyInCloset
            # 9 is AlreadyBeingWorn
            # 12, 13, & 14 is AlreadyReceived
            self.air.writeServerEvent('code-redeemed', avId=avId, issue='Could not deliver items for code: %s' % code)
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.InvalidCode, 0])
            return

        # Send the item and tell the user its A-Okay
        self.air.writeServerEvent('code-redeemed', avId=avId, issue='Successfuly redeemed code: %s' % code)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, self.Success, 0])

    def getItemsForCode(self, code):
        avId = self.air.getAvatarIdFromSender()
        if not avId:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Could not parse the gender of an invalid avId')
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId=avId, issue='Could not parse the gender of an invalid avatar')
            return

        '''
        # Here is an example of giving clothing to specific genders.
        if code == "GenderExample":
            # The following code will check to see if the gender is a male.
            # If it is, then they will be given shirt 2002.
            if av.getStyle().getGender() == 'm':
                shirt = CatalogClothingItem(2002, 0)
            # If it sees the gender isn't male, it will give shirt 2003.
            else:
                shirt = CatalogClothingItem(2003, 0)
            return [shirt]
        '''

        code = code.lower() # Anti-frustration features, activate!

        # Now onto the actual codes
        if code == "gadzooks":
            shirt = CatalogClothingItem(1807, 0)
            return [shirt]

        if code == "sillymeter" or code == "silly meter" or code == "silly-meter":
            shirt = CatalogClothingItem(1753, 0)
            return [shirt]

        if code == "gc-sbfo" or code == "gc sbfo" or code == "gcsbfo":
            shirt = CatalogClothingItem(1788, 0)
            return [shirt]

        if code == "getconnected" or code == "get connected" or code == "get_connected":
            shirt = CatalogClothingItem(1752, 0)
            return [shirt]

        if code == "summer":
            shirt = CatalogClothingItem(1709, 0)
            return [shirt]

        if code == "brrrgh":
            shirt = CatalogClothingItem(1800, 0)
            return [shirt]

        if code == "toontastic":
            shirt = CatalogClothingItem(1820, 0)
            return [shirt]

        if code == "sunburst":
            shirt = CatalogClothingItem(1809, 0)
            return [shirt]

        #Cog Nation Free Part (Propeller Piece)
        #if code == "lawbots-lose" or code == "lbfo":
            #suitpart = SuitPart(0, 0)
            #return [suit]

        if code == "sweet":
            beans = CatalogBeanItem(12000, tagCode = 2)
            return [beans]

        if code == "winter" or code == "cannons":
            rent = CatalogRentalItem(ToontownGlobals.RentalCannon, 48*60, 0)
            return [rent]

        return []

    def redeemCode(self, code):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        code = code.lower()

        if code in self.codes:
            if av.isCodeRedeemed(code):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [4])
                self.air.writeServerEvent('suspicious', avId, 'Toon tried to redeem already redeemed code %s' % code)
                return

            codeInfo = self.codes[code]
            date = datetime.now()

            if ('year' in codeInfo and date.year is not codeInfo['year']) and date.year > codeInfo['year'] or ('expirationDate' in codeInfo and codeInfo['expirationDate'] - date < timedelta(hours = 1)):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [2])
                self.air.writeServerEvent('suspicious', avId, 'Toon attempted to redeem code %s but it was expired!' % code)
                return
            elif ('year' in codeInfo and date.year is not codeInfo['year']) and date.year < codeInfo['year'] or ('month' in codeInfo and date.month is not codeInfo['month']) or ('day' in codeInfo and date.day is not codeInfo['day']):
                self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [5])
                self.air.writeServerEvent('suspicious', avId, "Toon attempted to redeem code %s but it wasn't usable yet!" % code)
                return

            av.redeemCode(code)
            self.requestCodeRedeem(avId, av, codeInfo['items'])
            self.air.writeServerEvent('code-redeemed', avId, 'Toon successfully redeemed %s' % code)
        else:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [1])
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to redeem non-existent code %s' % code)

    def requestCodeRedeem(self, avId, av, items):
        if len(av.mailboxContents) + len(av.onOrder) + len(av.onGiftOrder) + len(items) >= ToontownGlobals.MaxMailboxContents:
            self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [3])
            return

        for item in items:
            if item in av.onOrder:
                continue

            item.deliveryDate = int(time.time() / 60) + 0.01
            av.onOrder.append(item)

        av.b_setDeliverySchedule(av.onOrder)
        self.sendUpdateToAvatarId(avId, 'redeemCodeResult', [0])
        self.air.writeServerEvent('code-redeemed', avId, 'Toon is being sent %s from redeemed code' % items)
