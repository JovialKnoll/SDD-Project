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
        self.masterPanel = wx.Panel(self)
        self.mainPanel = wx.Panel(self.masterPanel) #used for holding all creator tools
        self.savePanel = wx.Panel(self.masterPanel) #used for holding the save prompt
        
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.sizer.Add(self.savePanel, 1, wx.EXPAND)
        self.masterPanel.SetSizer(self.sizer)
        self.init_save_panel()
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #row 2 is the save button
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonSave = wx.Button(self.mainPanel, 5, label="Save Study Guide")
        self.hbox2.Add(self.buttonSave, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 70)
        
        #row 1 is the add term button
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonAdd = wx.Button(self.mainPanel, 2, label="Add Term")
        self.hbox1.Add(self.buttonAdd, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 70)
        
        #row 3 is the labels for term and definition textboxes
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.labelTerm = wx.StaticText(self.mainPanel, label="Term/Question:")
        self.labelDefinition = wx.StaticText(self.mainPanel, label="Definition/Answer:")
        self.hbox3.Add(self.labelTerm, 2, wx.RIGHT, 50)
        self.hbox3.Add(self.labelDefinition, 3, wx.RIGHT, 50)
        
        #row 4 is the textboxes for term and definition
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.textTerm = wx.TextCtrl(self.mainPanel)
        #self.textTerm.setDefaultStyle(wxTE_PROCESS_ENTER)
        self.textDefinition = wx.TextCtrl(self.mainPanel)
        self.hbox4.Add(self.textTerm, 2, wx.RIGHT, 50)
        self.hbox4.Add(self.textDefinition, 3, wx.RIGHT, 50)
        
        #row 5 is the textbox for decoy answers
        self.vbox5 = wx.BoxSizer(wx.VERTICAL)
        self.hbox5a = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox5b = wx.BoxSizer(wx.HORIZONTAL)
        self.labelDecoy = wx.StaticText(self.mainPanel, label="Decoy Answers:")
        self.textDecoy = wx.TextCtrl(self.mainPanel)
        self.buttonAddDecoy = wx.Button(self.mainPanel, 8, label="Add Decoy")
        wx.EVT_BUTTON(self, 8, self._add_decoy)
        self.buttonRemDecoy = wx.Button(self.mainPanel, 9, label="Remove Decoy")
        wx.EVT_BUTTON(self, 9, self._rem_decoy)
        self.decoyListBox = wx.ListBox(self.mainPanel, id=10)
        self.hbox5a.Add(self.labelDecoy, 2, wx.RIGHT, 50)
        self.hbox5a.Add(self.textDecoy, 3, wx.RIGHT, 50)
        self.vbox5.Add(self.buttonAddDecoy, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox5.Add(self.buttonRemDecoy, 1, wx.ALL | wx.EXPAND, 5)
        self.hbox5b.Add(self.vbox5, 2, wx.ALL | wx.EXPAND, 10)
        self.hbox5b.Add(self.decoyListBox, 3, wx.ALL | wx.EXPAND, 10)
        
        #row 6
        self.vbox6 = wx.BoxSizer(wx.VERTICAL)
        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.labelList = wx.StaticText(self.mainPanel, label="Current\nItems:")
        self.labelList.SetFont(wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.button_delete = wx.Button(self.mainPanel, 3, label="Delete")
        wx.EVT_BUTTON(self, 3, self._delete_element)
        self.buttonChange = wx.Button(self.mainPanel, 4, label="Change")
        wx.EVT_BUTTON(self, 4, self._change_element)
        self.termListBox = wx.ListBox(self.mainPanel, id=7)
        wx.EVT_LISTBOX(self, 7, self._term_selected)
        self.vbox6.Add(self.labelList, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox6.Add(self.button_delete, 1, wx.ALL | wx.EXPAND, 5)
        self.vbox6.Add(self.buttonChange, 1, wx.ALL | wx.EXPAND, 5)
        self.hbox6.Add(self.vbox6, 2, wx.TOP | wx.LEFT | wx.EXPAND, 0)
        self.hbox6.Add(self.termListBox, 3, wx.TOP | wx.RIGHT | wx.EXPAND, 10)
        
        
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
        self.mainPanel.SetSizer(self.vbox)
    
    def init_save_panel(self):
        """ create the save prompt """
        
        self.saveVbox = wx.BoxSizer(wx.VERTICAL)
        
        #create items
        self.saveFileLabel = wx.StaticText(self.savePanel, label="Save file as:")
        self.saveFileText = wx.TextCtrl(self.savePanel)
        self.saveFileSaveButton = wx.Button(self.savePanel, 11, label="FileSave ")
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
        
        self.savePanel.SetSizer(self.saveVbox)
        self.savePanel.Hide()
    
    def _add_term(self, event):
        """ adds a term to the list """
        #print "Added term: " + self.textTerm.GetValue() + " with definition: " + self.textDefinition.GetValue()
        self.termList.append(self.textTerm.GetValue())
        self.defList.append(self._combine_definitions())
        self.update_list()
        self.update_decoy_list()
    
    def _delete_element(self, event):
        """ deletes a term from the list """
        self.termList.pop(self.termListBox.GetSelection())
        self.defList.pop(self.termListBox.GetSelection())
        self.update_list()
    
    def _change_element(self, event):
        """ alters the selected term to match the current state """
        self.termList[self.termListBox.GetSelection()] = self.textTerm.GetValue()
        self.defList[self.termListBox.GetSelection()] = self._combine_definitions()
        self.update_list()
        self.update_decoy_list()
    
    def _term_selected(self, event):
        """ change which term you have selected, and update all items to reflet that """
        self.textTerm.SetValue(self.termList[self.termListBox.GetSelection()])
        self.textDefinition.SetValue(self.defList[self.termListBox.GetSelection()][0])
        self.decoys = [self.defList[self.termListBox.GetSelection()][i] for i in range(1,len(self.defList[self.termListBox.GetSelection()]))]
        self.update_decoy_list()
    
    def _add_decoy(self, event):
        """ add a decoy definition to the list of decoy definitions for that term """
        self.decoys.append(self.textDecoy.GetValue())
        self.update_decoy_list()
    
    def _rem_decoy(self, event):
        """ remove a decoy definition from the list of decoy definitions for that term """
        self.decoys.pop(self.decoyListBox.GetSelection())
        self.update_decoy_list()
    
    def _combine_definitions(self):
        """ combine the correct definition and all decoys into one list """
        result = [self.textDefinition.GetValue()]
        for i in self.decoys:
            result.append(i)
        return result
    
    def update_decoy_list(self):
        """ update the listBox of decoys to reflect the current state """
        self.decoyListBox.Set(self.decoys)
    
    def update_list(self):
        """ update the listBox of terms to reflect the current state """
        self.termListBox.Set([self.termList[i] + " = " + self.defList[i][0] for i in range(0, len(self.termList))])
        
    def save(self, event):
        """ open the save tab """
        self.mainPanel.Hide()
        self.savePanel.Show()
        self.sizer.Layout()
    
    def save_as(self, event):
        """ write the data to a save file """
        data = [(self.termList[i], self.defList[i]) for i in range(0, len(self.termList))]
        gbxml.save_xml(data, self.saveFileText.GetValue())
        self.savePanel.Hide()
        self.mainPanel.Show()
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