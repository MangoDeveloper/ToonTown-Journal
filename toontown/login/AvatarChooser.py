from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
import AvatarChoice
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.launcher import DownloadForceAcknowledge
from direct.gui.DirectGui import *
from toontown.hood import SkyUtil
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import DisplayOptions
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from toontown.toontowngui import TTDialog
import random
MAX_AVATARS = 6
POSITIONS = (Vec3(-0.9, 0, 0.8),
 Vec3(-0.9, 0, 0.5),
 Vec3(-0.9, 0, 0.2),
 Vec3(-0.9, 0, -0.1),
 Vec3(-0.9, 0, -0.4),
 Vec3(-0.9, 0, -0.7))
COLORS = (Vec4(0.917, 0.164, 0.164, 1),
 Vec4(0.152, 0.75, 0.258, 1),
 Vec4(0.598, 0.402, 0.875, 1),
 Vec4(0.133, 0.59, 0.977, 1),
 Vec4(0.895, 0.348, 0.602, 1),
 Vec4(0.977, 0.816, 0.133, 1))
chooser_notify = DirectNotifyGlobal.directNotify.newCategory('AvatarChooser')

class AvatarChooser(StateData.StateData):

    def __init__(self, avatarList, parentFSM, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.choice = None
        self.avatarList = avatarList
        self.displayOptions = None
        self.fsm = ClassicFSM.ClassicFSM('AvatarChooser', [State.State('Choose', self.enterChoose, self.exitChoose, ['CheckDownload']), State.State('CheckDownload', self.enterCheckDownload, self.exitCheckDownload, ['Choose'])], 'Choose', 'Choose')
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getCurrentState().addChild(self.fsm)
        return

    def enter(self):
        self.notify.info('AvatarChooser.enter')
        if not self.displayOptions:
            self.displayOptions = DisplayOptions.DisplayOptions()
        self.notify.info('calling self.displayOptions.restrictToEmbedded(False)')
        if base.appRunner:
            self.displayOptions.loadFromSettings()
            self.displayOptions.restrictToEmbedded(False)
        if self.isLoaded == 0:
            self.load()
        base.disableMouse()
        self.title.reparentTo(aspect2d)
        self.quitButton.show()
        if base.cr.loginInterface.supportsRelogin():
            self.logoutButton.show()
        self.pickAToonBG.setBin('background', 1)
        self.pickAToonBG.reparentTo(aspect2d)

        base.setBackgroundColor(Vec4(0.145, 0.368, 0.78, 1))
        choice = config.GetInt('auto-avatar-choice', -1)
        for panel in self.panelList:
            panel.show()
            self.accept(panel.doneEvent, self.__handlePanelDone)
            if panel.position == choice and panel.mode == AvatarChoice.AvatarChoice.MODE_CHOOSE:
                self.__handlePanelDone('chose', panelChoice=choice)

    def exit(self):
        if self.isLoaded == 0:
            return None
        for panel in self.panelList:
            panel.hide()

        self.ignoreAll()
        self.title.reparentTo(hidden)
        self.quitButton.hide()
        self.logoutButton.hide()
        self.pickAToonBG.reparentTo(hidden)
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        self.releaseNotesBox.hide()
        self.gamelogo.hide()
        return None

    def load(self, isPaid):
        if self.isLoaded == 1:
            return None
        self.isPaid = isPaid
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        gui2 = loader.loadModel('phase_3/models/gui/quit_button')
        newGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui')
        self.pickAToonBG = newGui.find('**/tt_t_gui_pat_background')
        self.pickAToonBG.reparentTo(hidden)
        self.pickAToonBG.setPos(0.0, 2.73, 0.0)
        self.pickAToonBG.setScale(1, 1, 1)
        self.title = OnscreenText(TTLocalizer.AvatarChooserPickAToon, scale=TTLocalizer.ACtitle, parent=hidden, font=ToontownGlobals.getSignFont(), fg=(1, 0.9, 0.1, 1), pos=(0.0, 0.82))

        # Quit Button
        quitHover = gui.find('**/QuitBtn_RLVR')
        self.quitButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None, text=TTLocalizer.AvatarChooserQuit, text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_pos=TTLocalizer.ACquitButtonPos, text_scale=TTLocalizer.ACquitButton, image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, pos=(1.08, 0, -0.907), command=self.__handleQuit)
        self.quitButton.reparentTo(base.a2dTopRight)
        self.quitButton.setPos(-0.5, 0, -0.07)
        
        # Options Button
        self.logoutButton = DirectButton(relief=None, image=(quitHover, quitHover, quitHover), text="Options", text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_scale=TTLocalizer.AClogoutButton, text_pos=(0, -0.035), image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, command=self.showOptionsWarning)
        self.logoutButton.reparentTo(base.a2dTopLeft)
        self.logoutButton.setPos(0.5, 0, -0.07) 
        self.logoutButton.hide()

        # Release Notes Box
        self.releaseNotesBox = OnscreenImage(image = 'phase_3/maps/gui-panel-transparent.png')
        self.releaseNotesBox.setTransparency(TransparencyAttrib.MAlpha)
        self.releaseNotesBox.setPos(0.6, 0, 0)
        self.releaseNotesBox.setScale(0.6)

        # Release Notes Text
        self.releaseNotesText = OnscreenText(text = 'Release Notes:\n' + TTLocalizer.releaseNotes)
        self.releaseNotesText.reparentTo(self.releaseNotesBox)
        
        # Game Logo
        self.gamelogo = OnscreenImage(image = "phase_3/maps/toontown-logo.png")
        self.gamelogo.setTransparency(TransparencyAttrib.MAlpha)
        self.gamelogo.setScale(0.9, 0.4, 0.4)
        self.gamelogo.setPos(0, 0, 1.1)
        self.gamelogo.reparentTo(self.releaseNotesBox)
        self.gamelogo.hide()

        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()
        self.panelList = []
        used_position_indexs = []
        for av in self.avatarList:
            if base.cr.isPaid():
                okToLockout = 0
            else:
                okToLockout = 1
                if av.position in AvatarChoice.AvatarChoice.OLD_TRIALER_OPEN_POS:
                    okToLockout = 0
            panel = AvatarChoice.AvatarChoice(av, position=av.position, paid=isPaid, okToLockout=okToLockout)
            panel.setPos(POSITIONS[av.position])
            used_position_indexs.append(av.position)
            self.panelList.append(panel)

        for panelNum in range(0, MAX_AVATARS):
            if panelNum not in used_position_indexs:
                panel = AvatarChoice.AvatarChoice(position=panelNum, paid=isPaid)
                panel.setPos(POSITIONS[panelNum])
                self.panelList.append(panel)

        if len(self.avatarList) > 0:
            self.initLookAtInfo()
        self.isLoaded = 1

    def getLookAtPosition(self, toonHead, toonidx):
        lookAtChoice = random.random()
        if len(self.used_panel_indexs) == 1:
            lookFwdPercent = 0.33
            lookAtOthersPercent = 0
        else:
            lookFwdPercent = 0.2
            if len(self.used_panel_indexs) == 2:
                lookAtOthersPercent = 0.4
            else:
                lookAtOthersPercent = 0.65
        lookRandomPercent = 1.0 - lookFwdPercent - lookAtOthersPercent
        if lookAtChoice < lookFwdPercent:
            self.IsLookingAt[toonidx] = 'f'
            return Vec3(0, 1.5, 0)
        elif lookAtChoice < lookRandomPercent + lookFwdPercent or len(self.used_panel_indexs) == 1:
            self.IsLookingAt[toonidx] = 'r'
            return toonHead.getRandomForwardLookAtPoint()
        else:
            other_toon_idxs = []
            for i in range(len(self.IsLookingAt)):
                if self.IsLookingAt[i] == toonidx:
                    other_toon_idxs.append(i)

            if len(other_toon_idxs) == 1:
                IgnoreStarersPercent = 0.4
            else:
                IgnoreStarersPercent = 0.2
            NoticeStarersPercent = 0.5
            bStareTargetTurnsToMe = 0
            if len(other_toon_idxs) == 0 or random.random() < IgnoreStarersPercent:
                other_toon_idxs = []
                for i in self.used_panel_indexs:
                    if i != toonidx:
                        other_toon_idxs.append(i)

                if random.random() < NoticeStarersPercent:
                    bStareTargetTurnsToMe = 1
            if len(other_toon_idxs) == 0:
                return toonHead.getRandomForwardLookAtPoint()
            else:
                lookingAtIdx = random.choice(other_toon_idxs)
            if bStareTargetTurnsToMe:
                self.IsLookingAt[lookingAtIdx] = toonidx
                otherToonHead = None
                for panel in self.panelList:
                    if panel.position == lookingAtIdx:
                        otherToonHead = panel.headModel

                otherToonHead.doLookAroundToStareAt(otherToonHead, self.getLookAtToPosVec(lookingAtIdx, toonidx))
            self.IsLookingAt[toonidx] = lookingAtIdx
            return self.getLookAtToPosVec(toonidx, lookingAtIdx)
        return

    def getLookAtToPosVec(self, fromIdx, toIdx):
        x = -(POSITIONS[toIdx][0] - POSITIONS[fromIdx][0])
        y = POSITIONS[toIdx][1] - POSITIONS[fromIdx][1]
        z = POSITIONS[toIdx][2] - POSITIONS[fromIdx][2]
        return Vec3(x, y, z)

    def initLookAtInfo(self):
        self.used_panel_indexs = []
        for panel in self.panelList:
            if panel.dna != None:
                self.used_panel_indexs.append(panel.position)

        if len(self.used_panel_indexs) == 0:
            return
        self.IsLookingAt = []
        for i in range(MAX_AVATARS):
            self.IsLookingAt.append('f')

        for panel in self.panelList:
            if panel.dna != None:
                panel.headModel.setLookAtPositionCallbackArgs((self, panel.headModel, panel.position))

        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        cleanupDialog('globalDialog')
        for panel in self.panelList:
            panel.destroy()

        del self.panelList
        self.title.removeNode()
        del self.title
        self.quitButton.destroy()
        del self.quitButton
        self.logoutButton.destroy()
        del self.logoutButton
        self.releaseNotesBox.destroy()
        del self.releaseNotesBox
        self.gamelogo.removeNode()
        del self.gamelogo
        self.pickAToonBG.removeNode()
        del self.pickAToonBG
        del self.avatarList
        self.parentFSM.getCurrentState().removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.ignoreAll()
        self.isLoaded = 0
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        return None

    def __handlePanelDone(self, panelDoneStatus, panelChoice = 0):
        self.doneStatus = {}
        self.doneStatus['mode'] = panelDoneStatus
        self.choice = panelChoice
        if panelDoneStatus == 'chose':
            self.__handleChoice()
        elif panelDoneStatus == 'nameIt':
            self.__handleCreate()
        elif panelDoneStatus == 'delete':
            self.__handleDelete()
        elif panelDoneStatus == 'create':
            self.__handleCreate()

    def getChoice(self):
        return self.choice

    def __handleChoice(self):
        self.fsm.request('CheckDownload')

    def __handleCreate(self):
        base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent, [self.doneStatus]))

    def __handleDelete(self):
        messenger.send(self.doneEvent, [self.doneStatus])

    def __handleQuit(self):
        cleanupDialog('globalDialog')
        self.doneStatus = {'mode': 'exit'}
        messenger.send(self.doneEvent, [self.doneStatus])

    def enterChoose(self):
        pass

    def exitChoose(self):
        pass

    def enterCheckDownload(self):
        self.accept('downloadAck-response', self.__handleDownloadAck)
        self.downloadAck = DownloadForceAcknowledge.DownloadForceAcknowledge('downloadAck-response')
        self.downloadAck.enter(4)

    def exitCheckDownload(self):
        self.downloadAck.exit()
        self.downloadAck = None
        self.ignore('downloadAck-response')
        return

    def __handleDownloadAck(self, doneStatus):
        if doneStatus['mode'] == 'complete':
            base.transitions.fadeOut(finishIval=EventInterval(self.doneEvent, [self.doneStatus]))
        else:
            self.fsm.request('Choose')

    def __handleLogoutWithoutConfirm(self):
        base.cr.loginFSM.request('login')

    def showOptionsWarning(self):
        # Close Options Button
        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        quitHover = gui.find('**/QuitBtn_RLVR')
        self.closeOptionsButton = DirectButton(relief=None, image=(quitHover, quitHover, quitHover), text="< Back", text_font=ToontownGlobals.getSignFont(), text_fg=(0.977, 0.816, 0.133, 1), text_scale=TTLocalizer.AClogoutButton, text_pos=(0, -0.035), image_scale=1, image1_scale=1.05, image2_scale=1.05, scale=1.05, command=self.exitWarning)
        self.closeOptionsButton.reparentTo(base.a2dTopLeft)
        self.closeOptionsButton.setPos(0.5, 0, -0.07) 
        self.logoutButton.hide()
        self.optionsBox = OnscreenImage(image = 'phase_3/maps/gui-panel-transparent.png')
        self.optionsBox.setTransparency(TransparencyAttrib.MAlpha)
        self.optionsBox.setPos(0, 0, 0)
        self.optionsBox.setScale(0.7)

        # Music Label
        self.Music_Label = DirectLabel(parent=aspect2d, relief=None, text='Music Volume', text_align=TextNode.ACenter, text_scale=0.052, pos=(0, 0, 0.5))
        # Music Slider
        self.Music_toggleSlider = DirectSlider(parent=aspect2d, pos=(0, 0, 0.4),
                                               value=settings['musicVol']*100, pageSize=5, range=(0, 100), command=self.__doMusicLevel,)
        self.Music_toggleSlider.setScale(0.4, 0.4, 0.4)
        self.Music_toggleSlider.show()
        
        # SFX Slider
        self.SoundFX_toggleSlider = DirectSlider(parent=aspect2d, pos=(0, 0.0, 0.1),
                                               value=settings['sfxVol']*100, pageSize=5, range=(0, 100), command=self.__doSfxLevel)
        self.SoundFX_toggleSlider.setScale(0.4, 0.4, 0.4)
        # SFX Label
        self.SoundFX_Label = DirectLabel(parent=aspect2d, relief=None, text='SFX Volume', text_align=TextNode.ACenter, text_scale=0.052, pos=(0, 0, 0.2))

        # Toon Chat Sound Effects
        self.ToonChatSounds_toggleButton = DirectButton(parent=aspect2d, relief=None, image=(guiButton.find('**/QuitBtn_UP'),
         guiButton.find('**/QuitBtn_DN'),
         guiButton.find('**/QuitBtn_RLVR'),
         guiButton.find('**/QuitBtn_UP')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=(0.7, 1, 1), text='', text3_fg=(0.5, 0.5, 0.5, 0.75), text_scale=0.052, text_pos=(0, -.02), pos=(0, 0, -0.2), command=self.__doToggleToonChatSounds)
        self.ToonChatSounds_toggleButton.setScale(0.8)
        self.ToonChatSounds_Label = DirectLabel(parent=aspect2d, relief=None, text='Toon Chat Sounds', text_align=TextNode.ACenter, text_scale=0.052, pos=(0, 0, -0.1))
        
    def exitWarning(self):
        self.optionsBox.hide()
        self.Music_Label.hide()
        self.Music_toggleSlider.hide()
        self.SoundFX_Label.hide()
        self.SoundFX_toggleSlider.hide()
        self.ToonChatSounds_Label.hide()
        self.ToonChatSounds_toggleButton.hide()
        self.logoutButton.show()
        self.closeOptionsButton.hide()

        # EZ copy from optionspage.py
    def __doMusicLevel(self):
        vol = self.Music_toggleSlider['value']
        vol = float(vol) / 100
        settings['musicVol'] = vol
        base.musicManager.setVolume(vol)
        base.musicActive = vol > 0.0
        
    def __doSfxLevel(self):
        vol = self.SoundFX_toggleSlider['value']
        vol = float(vol) / 100
        settings['sfxVol'] = vol
        for sfm in base.sfxManagerList:
            sfm.setVolume(vol)
        base.sfxActive = vol > 0.0
        
    def __doToggleToonChatSounds(self):
        messenger.send('wakeup')
        if base.toonChatSounds:
            base.toonChatSounds = 0
            settings['toonChatSounds'] = False
        else:
            base.toonChatSounds = 1
            settings['toonChatSounds'] = True
        self.settingsChanged = 1
        self.__setToonChatSoundsButton()

    def __setToonChatSoundsButton(self):
        if base.toonChatSounds:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOnLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOffLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn
        if base.sfxActive:
            self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
        else:
            self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
            self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED