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

def get_font_surf(font, text, width, antialias, color, backgroundColor):
    lines = wrap_text(font, text, width).split("\n")
    print len(lines)
    surfs = [font.render(i, antialias, color) for i in lines]
    for i in lines:
        print i
    maxwidth = 0
    maxheight = 0
    for i in surfs:
        if i.get_width() > maxwidth:
            maxwidth = i.get_width()
        if i.get_height() > maxheight:
            maxheight = i.get_height()
    print "(" + str(maxwidth) + ", " + str(maxheight) + ")"
    surface = pygame.Surface((maxwidth, maxheight*len(lines)))
    surface.fill(backgroundColor)
    for i in range(len(surfs)):
        surface.blit(surfs[i], (0, i*maxheight))
    return surface

#pygame.font.init()
#text = "This is a very long sentence and I want to test the wrapText function to make sure that it will correctly separate this sentence into lines of approximately equal length."
#font = pygame.font.Font(pygame.font.get_default_font(), 12)
#print wrap_text(font, text, 250)