#must install wxpython to the version of python running this code.

import wx

class StudyGuideCreator(wx.Frame):
    
    def __init__(self, parent, title):
        super(StudyGuideCreator, self).__init__(parent, title=title, size=(700,560))
        self.init_ui()
        self.Show()
        self.Centre()
    
    def init_ui(self):
        self.main_panel = wx.Panel(self)
        
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #row 1
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        #self.image_title = wx.StaticBitmap(self.main_panel)
        #self.image_title.SetBitmap(wx.Image("images/menu.png", wx.BITMAP_TYPE_PNG).Rescale(550,160).ConvertToBitmap())
        #self.image_title = wx.Image("images/menu.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #self.join_panel.setBitmap(wx.Image("images/menu.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        #self.label_title = wx.StaticText(self.join_panel, label="Rezolution")
        #self.label_title.SetFont(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.button_add = wx.Button(self.main_panel, 2, label="Add Term")
        #self.join_hbox1.Add(self.image_title, 0, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.hbox1.Add(self.button_add, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 70)
        
        #row 4
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_term = wx.TextCtrl(self.main_panel)
        self.text_definition = wx.TextCtrl(self.main_panel)
        self.hbox4.Add(self.text_term, 2, wx.RIGHT, 50)
        self.hbox4.Add(self.text_definition, 3, wx.RIGHT, 50)
        
        
        #rack em up
        self.vbox.Add(self.hbox1, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox4, 0, wx.ALL | wx.EXPAND, 10)
        
        #Interactivtize me baby
        wx.EVT_BUTTON(self, 2, self._add_term)
        #wx.EVT_TEXT_ENTER(self, 2, self._on_key_down)
        #self.main_panel.Bind(wx.EVT_KEY_DOWN, self._on_key_down)
        #self.text_definition.Bind(wx.EVT_KEY_DOWN, self._on_key_down)
        #wx.EVT_KEY_DOWN(self, 2, self._on_key_down)
        self.main_panel.SetSizer(self.vbox)
    
    def _add_term(self, event):
        print "Added term: " + self.text_term.GetValue() + " with definition: " + self.text_definition.GetValue()
    
    """
    def _on_key_down(self, event):
        print "Keydown = " + event.GetKeyCode()
        if (event.GetKeyCode() == wx.WXK_RETURN):
            self._add_term(event)
    """

app = wx.App()
s = StudyGuideCreator(None, title="The Title")
app.MainLoop()