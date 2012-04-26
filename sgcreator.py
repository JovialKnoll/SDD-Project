#must install wxpython to the version of python running this code.
# sgcreator.py is a gui used for creating study guides
#
import wx

import gbxml

class StudyGuideCreator(wx.Frame):
    """ StudyGuideCreator is a window that has all the items for creating a study guide """
    def __init__(self, parent, title):
        """ initialize the window """
        super(StudyGuideCreator, self).__init__(parent, title=title, size=(700,560))
        self.termList = [] #the list of terms
        self.defList = [] #a list of lists of responses, the first in each being the correct response, and all others being decoys
        self.decoys = [] #the list of decoy responses for the current term
        
        self.init_ui() #create all the items in the window
        self.Show() #display the window
        self.Centre() #put the window in teh center of the screen
    
    def init_ui(self):
        """ creates all of the items in the window """
        self.master_panel = wx.Panel(self)
        self.main_panel = wx.Panel(self.master_panel) #used for holding all creator tools
        self.save_panel = wx.Panel(self.master_panel) #used for holding the save prompt
        
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.sizer.Add(self.save_panel, 1, wx.EXPAND)
        self.master_panel.SetSizer(self.sizer)
        self.init_save_panel()
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #row 2 is the save button
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_save = wx.Button(self.main_panel, 5, label="Save Study Guide")
        self.hbox2.Add(self.button_save, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 70)
        
        #row 1 is the add term button
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_add = wx.Button(self.main_panel, 2, label="Add Term")
        self.hbox1.Add(self.button_add, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 70)
        
        #row 3 is the labels for term and definition textboxes
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.label_term = wx.StaticText(self.main_panel, label="Term/Question:")
        self.label_definition = wx.StaticText(self.main_panel, label="Definition/Answer:")
        self.hbox3.Add(self.label_term, 2, wx.RIGHT, 50)
        self.hbox3.Add(self.label_definition, 3, wx.RIGHT, 50)
        
        #row 4 is the textboxes for term and definition
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_term = wx.TextCtrl(self.main_panel)
        #self.text_term.setDefaultStyle(wxTE_PROCESS_ENTER)
        self.text_definition = wx.TextCtrl(self.main_panel)
        self.hbox4.Add(self.text_term, 2, wx.RIGHT, 50)
        self.hbox4.Add(self.text_definition, 3, wx.RIGHT, 50)
        
        #row 5 is the textbox for decoy answers
        self.vbox5 = wx.BoxSizer(wx.VERTICAL)
        self.hbox5a = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox5b = wx.BoxSizer(wx.HORIZONTAL)
        self.label_decoy = wx.StaticText(self.main_panel, label="Decoy Answers:")
        self.text_decoy = wx.TextCtrl(self.main_panel)
        self.button_add_decoy = wx.Button(self.main_panel, 8, label="Add Decoy")
        wx.EVT_BUTTON(self, 8, self._add_decoy)
        self.button_rem_decoy = wx.Button(self.main_panel, 9, label="Remove Decoy")
        wx.EVT_BUTTON(self, 9, self._rem_decoy)
        self.decoy_listBox = wx.ListBox(self.main_panel, id=10)
        self.hbox5a.Add(self.label_decoy, 2, wx.RIGHT, 50)
        self.hbox5a.Add(self.text_decoy, 3, wx.RIGHT, 50)
        self.vbox5.Add(self.button_add_decoy, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox5.Add(self.button_rem_decoy, 1, wx.ALL | wx.EXPAND, 5)
        self.hbox5b.Add(self.vbox5, 2, wx.ALL | wx.EXPAND, 10)
        self.hbox5b.Add(self.decoy_listBox, 3, wx.ALL | wx.EXPAND, 10)
        
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
        
        
        #assemble the rows
        self.vbox.Add(self.hbox2, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox1, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox3, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        self.vbox.Add(self.hbox4, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox5a, 0, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox5b, 3, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(self.hbox6, 7, wx.ALL | wx.EXPAND, 10)
        
        #button events
        wx.EVT_BUTTON(self, 2, self._add_term)
        wx.EVT_BUTTON(self, 5, self.save)
        self.main_panel.SetSizer(self.vbox)
    
    def init_save_panel(self):
        """ create the save prompt """
        
        self.saveVbox = wx.BoxSizer(wx.VERTICAL)
        
        #create items
        self.saveFileLabel = wx.StaticText(self.save_panel, label="Save file as:")
        self.saveFileText = wx.TextCtrl(self.save_panel)
        self.saveFileSaveButton = wx.Button(self.save_panel, 11, label="FileSave ")
        wx.EVT_BUTTON(self, 11, self.save_as)
        
        #put them in sizers
        self.saveHbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.saveHbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.saveHbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.saveHbox1.Add(self.saveFileLabel, 1, wx.ALL | wx.EXPAND, 10)
        self.saveHbox2.Add(self.saveFileText, 1, wx.ALL | wx.EXPAND, 10)
        self.saveHbox3.Add(self.saveFileSaveButton, 1, wx.ALL | wx.EXPAND, 10)
        
        #put the sizers together
        self.saveVbox.Add(self.saveHbox1, 1, wx.ALL | wx.EXPAND, 10)
        self.saveVbox.Add(self.saveHbox2, 1, wx.ALL | wx.EXPAND, 10)
        self.saveVbox.Add(self.saveHbox3, 1, wx.ALL | wx.EXPAND, 10)
        
        self.save_panel.SetSizer(self.saveVbox)
        self.save_panel.Hide()
    
    def _add_term(self, event):
        """ adds a term to the list """
        #print "Added term: " + self.text_term.GetValue() + " with definition: " + self.text_definition.GetValue()
        self.termList.append(self.text_term.GetValue())
        self.defList.append(self._combine_definitions())
        self.update_list()
        self.update_decoy_list()
    
    def _delete_element(self, event):
        """ deletes a term from the list """
        self.termList.pop(self.term_listBox.GetSelection())
        self.defList.pop(self.term_listBox.GetSelection())
        self.update_list()
    
    def _change_element(self, event):
        """ alters the selected term to match the current state """
        self.termList[self.term_listBox.GetSelection()] = self.text_term.GetValue()
        self.defList[self.term_listBox.GetSelection()] = self._combine_definitions()
        self.update_list()
        self.update_decoy_list()
    
    def _term_selected(self, event):
        """ change which term you have selected, and update all items to reflet that """
        self.text_term.SetValue(self.termList[self.term_listBox.GetSelection()])
        self.text_definition.SetValue(self.defList[self.term_listBox.GetSelection()][0])
        self.decoys = [self.defList[self.term_listBox.GetSelection()][i] for i in range(1,len(self.defList[self.term_listBox.GetSelection()]))]
        self.update_decoy_list()
    
    def _add_decoy(self, event):
        """ add a decoy definition to the list of decoy definitions for that term """
        self.decoys.append(self.text_decoy.GetValue())
        self.update_decoy_list()
    
    def _rem_decoy(self, event):
        """ remove a decoy definition from the list of decoy definitions for that term """
        self.decoys.pop(self.decoy_listBox.GetSelection())
        self.update_decoy_list()
    
    def _combine_definitions(self):
        """ combine the correct definition and all decoys into one list """
        result = [self.text_definition.GetValue()]
        for i in self.decoys:
            result.append(i)
        return result
    
    def update_decoy_list(self):
        """ update the listBox of decoys to reflect the current state """
        self.decoy_listBox.Set(self.decoys)
    
    def update_list(self):
        """ update the listBox of terms to reflect the current state """
        self.term_listBox.Set([self.termList[i] + " = " + self.defList[i][0] for i in range(0, len(self.termList))])
        
    def save(self, event):
        """ open the save tab """
        self.main_panel.Hide()
        self.save_panel.Show()
        self.sizer.Layout()
    
    def save_as(self, event):
        """ write the data to a save file """
        data = [(self.termList[i], self.defList[i]) for i in range(0, len(self.termList))]
        gbxml.saveXML(data, self.saveFileText.GetValue())
        self.save_panel.Hide()
        self.main_panel.Show()
        self.sizer.Layout()
    
    """
    def _on_key_down(self, event):
        print "Keydown = " + event.GetKeyCode()
        if (event.GetKeyCode() == wx.WXK_RETURN):
            self._add_term(event)
    """

# run the application
app = wx.App()
s = StudyGuideCreator(None, title="The Title")
app.MainLoop()