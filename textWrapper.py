import pygame

def wrap_text(font, text, width):
    wrapText = ""
    remainingText = text
    while len(remainingText) > 0:
        i = 0
        nextLine = ""
        while True:
            s = remainingText.partition(" ")
            if nextLine == "":
                nextLine = s[0]
                remainingText = s[2]
            elif font.size(nextLine + " " + s[0])[0] < width:
                nextLine = nextLine + " " + s[0]
                remainingText = s[2]
            else:
                break
        if len(wrapText) > 0:
            wrapText = wrapText + "\n"
        wrapText = wrapText + nextLine
    return wrapText

#pygame.font.init()
#text = "This is a very long sentence and I want to test the wrapText function to make sure that it will correctly separate this sentence into lines of approximately equal length."
#font = pygame.font.Font(pygame.font.get_default_font(), 12)
#print wrap_text(font, text, 250)