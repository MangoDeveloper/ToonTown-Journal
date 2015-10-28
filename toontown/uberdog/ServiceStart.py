import __builtin__


__builtin__.process = 'uberdog'


# Temporary hack patch:
__builtin__.__dict__.update(__import__('pandac.PandaModules', fromlist=['*']).__dict__)
from direct.extensions_native import HTTPChannel_extensions


from direct.showbase import PythonUtil

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--base-channel', help='The base channel that the server may use.')
parser.add_argument('--max-channels', help='The number of channels the server may use.')
parser.add_argument('--stateserver', help="The control channel of this UD's designated State Server.")
parser.add_argument('--astron-ip', help="The IP address of the Astron Message Director to connect to.")
parser.add_argument('--eventlogger-ip', help="The IP address of the Astron Event Logger to log to.")
parser.add_argument('config', nargs='*', default=['config/general.prc', 'config/release/dev.prc'], help="PRC file(s) to load.")
args = parser.parse_args()

for prc in args.config:
    loadPrcFile(prc)

localconfig = ''
if args.base_channel: localconfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels: localconfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver: localconfig += 'air-stateserver %s\n' % args.stateserver
if args.astron_ip: localconfig += 'air-connect %s\n' % args.astron_ip
if args.eventlogger_ip: localconfig += 'eventlog-host %s\n' % args.eventlogger_ip
loadPrcFileData('Command-line', localconfig)

def __inject_wx(_):
    code = textbox.GetValue()
    exec (code, globals())

def openInjector_wx():
    import wx
    
    app = wx.App(redirect = False)
        
    frame = wx.Frame(None, title = "Toontown Journey UberDOG Server Debug Injector", size=(640, 400), style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
    panel = wx.Panel(frame)
    button = wx.Button(parent = panel, id = -1, label = "Inject!", size = (50, 20), pos = (295, 0))
    global textbox
    textbox = wx.TextCtrl(parent = panel, id = -1, pos = (20, 22), size = (600, 340), style = wx.TE_MULTILINE)
    frame.Bind(wx.EVT_BUTTON, __inject_wx, button)

    frame.Show()
    app.SetTopWindow(frame)
    
    textbox.AppendText('')
    
    threading.Thread(target = app.MainLoop).start()

openInjector_wx()

from otp.ai.AIBaseGlobal import *

from toontown.uberdog.ToontownUberRepository import ToontownUberRepository
simbase.air = ToontownUberRepository(config.GetInt('air-base-channel', 400000000),
                                     config.GetInt('air-stateserver', 4002))
host = config.GetString('air-connect', '127.0.0.1')
port = 7100
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)
simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception:
    info = PythonUtil.describeException()
    simbase.air.writeServerEvent('uberdog-exception', simbase.air.getAvatarIdFromSender(), simbase.air.getAccountIdFromSender(), info)
    raise
