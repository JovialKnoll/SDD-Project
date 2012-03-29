#must install wxpython to the version of python running this code.

import wx
import xmlWriter

class StudyGuideCreator(wx.Frame):
    
    def __init__(self, parent, title):
        super(StudyGuideCreator, self).__init__(parent, title=title, size=(700,560))
        self.termList = []
        self.defList = []
        
        self.init_ui()
        self.Show()
        self.Centre()
    
    def init_ui(self):
        self.main_panel = wx.Panel(self)
        
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #row 2
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_save = wx.Button(self.main_panel, 5, label="Save Study Guide")
        self.hbox2.Add(self.button_save, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 70)
        
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
        #self.text_term.setDefaultStyle(wxTE_PROCESS_ENTER)
        self.text_definition = wx.TextCtrl(self.main_panel)
        self.hbox4.Add(self.text_term, 2, wx.RIGHT, 50)
        self.hbox4.Add(self.text_definition, 3, wx.RIGHT, 50)
        
        #row 6
        self.vbox6 = wx.BoxSizer(wx.VERTICAL)
        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_list = wx.StaticText(self.main_panel, label="Current\nItems:")
        self.label_list.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.button_delete = wx.Button(self.main_panel, 3, label="Delete")
        wx.EVT_BUTTON(self, 3, self._delete_element)
        self.button_change = wx.Button(self.main_panel, 4, label="Change")
        wx.EVT_BUTTON(self, 4, self._change_element)
        self.term_listBox = wx.ListBox(self.main_panel, id=7)
        wx.EVT_LISTBOX(self, 7, self._term_selected)
        self.vbox6.Add(self.label_list, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox6.Add(self.button_delete, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox6.Add(self.button_change, 1, wx.ALL | wx.EXPAND, 5)
        self.hbox6.Add(self.vbox6, 2, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.hbox6.Add(self.term_listBox, 3, wx.TOP | wx.RIGHT | wx.EXPAND, 10)
        
        
        #rack em up
        self.vbox.Add(self.hbox2, 1, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox1, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox4, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox6, 7, wx.ALL | wx.EXPAND, 10)
        
        #Interactivtize me baby
        wx.EVT_BUTTON(self, 2, self._add_term)
        wx.EVT_BUTTON(self, 5, self.save)
        #wx.EVT_TEXT_ENTER(self, 3, self._add_term)
        #self.main_panel.Bind(wx.EVT_KEY_DOWN, self._on_key_down)
        #self.text_definition.Bind(wx.EVT_KEY_DOWN, self._on_key_down)
        #wx.EVT_KEY_DOWN(self, 2, self._on_key_down)
        self.main_panel.SetSizer(self.vbox)
    
    def _add_term(self, event):
        #print "Added term: " + self.text_term.GetValue() + " with definition: " + self.text_definition.GetValue()
        self.termList.append(self.text_term.GetValue())
        self.defList.append(self.text_definition.GetValue())
        self.update_list()
    
    def _delete_element(self, event):
        self.termList.pop(self.term_listBox.GetSelection())
        self.defList.pop(self.term_listBox.GetSelection())
        self.update_list()
    
    def _change_element(self, event):
        self.termList[self.term_listBox.GetSelection()] = self.text_term.GetValue()
        self.defList[self.term_listBox.GetSelection()] = self.text_definition.GetValue()
        self.update_list()
    
    def _term_selected(self, event):
        self.text_term.SetValue(self.termList[self.term_listBox.GetSelection()])
        self.text_definition.SetValue(self.defList[self.term_listBox.GetSelection()])
    
    def update_list(self):
        self.term_listBox.Set([self.termList[i] + " = " + self.defList[i] for i in range(0, len(self.termList))])
        
    def save(self, event):
        data = [(self.termList[i], [self.defList[i]]) for i in range(0, len(self.termList))]
        xmlWriter.saveXML(data)
    
    """
    def _on_key_down(self, event):
        print "Keydown = " + event.GetKeyCode()
        if (event.GetKeyCode() == wx.WXK_RETURN):
            self._add_term(event)
    """

app = wx.App()
s = StudyGuideCreator(None, title="The Title")
app.MainLoop()