import wx
import sys
import os
import json
import subprocess


class ChappyPuttyMainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.allSession = None
        self.puttyPath = None
        wx.Frame.__init__(self, parent, title=title, size=(325, 600))
        self.SetMaxSize((325, 600))
        self.panel = wx.Panel(self, -1, style=wx.BORDER_THEME)
        self.listbox = wx.ListBox(self.panel, -1, pos=(1, 1), size=(300, 600))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.onOpenSession, self.listbox)
        self.readSessionFrmFile()
        self.readCfgFrmFile()
        self.Show(True)

    def onOpenSession(self, event):
        selpos = self.listbox.GetSelection()
        hostname = self.listbox.GetString(selpos)
        hostinfo = self.allSession[hostname]
        hostip = hostinfo["ip"]
        hostuser = hostinfo["username"]
        hostpass = hostinfo["password"]
        cmdstr = "%s -ssh %s@%s -pw %s" % (self.puttyPath, hostuser, hostip, hostpass)
        #wx.MessageBox(cmdstr)
        subprocess.Popen(cmdstr)

    def readSessionFrmFile(self):
        fp = open("session.json")
        self.allSession = json.load(fp)
        hostlist = [str(x) for x in self.allSession.keys()]
        self.listbox.InsertItems(hostlist, 0)
        fp.close()

    def readCfgFrmFile(self):
        fp = open("cfg.json")
        cfgjson = json.load(fp)
        self.puttyPath = cfgjson["putty"]
        fp.close()


happyApp = wx.App()
myWindow = ChappyPuttyMainWindow(None, "happyPutty")
happyApp.MainLoop()


