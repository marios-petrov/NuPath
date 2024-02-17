class notes:
    def __init__(self):
        self.noteText = "" 
        
    def updateNote(self, newNoteText):
        self.noteText = newNoteText
        
    def getNoteText(self):
        return self.noteText
    
    def clearNoteText(self):
        self.noteText = ""

        