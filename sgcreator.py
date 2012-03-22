import wx

class StudyGuideCreator(wx.Frame):
    
    def __init__(self, parent, title):
        super(StudyGuideCreator, self).__init__(parent, title=title, size=(700,560))
        self.init_ui()
        self.Show()
        self.Centre()
    
    def init_ui(self):
        self.main_panel = wx.Panel(self)

app = wx.App()
s = StudyGuideCreator(None, title="The Title")
app.MainLoop()