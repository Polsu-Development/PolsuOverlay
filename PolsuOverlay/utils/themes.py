from getpass import getuser

import os


def loadThemes(win):
    win.dirThemes = os.path.join(f"C:\\Users\\{getuser()}", 'Polsu', 'themes')
    if not os.path.exists(win.dirThemes):
        os.makedirs(win.dirThemes)

        
    win.themes = []
    for theme in os.listdir(win.pathThemes):
        if os.path.isfile(f"{win.pathThemes}/{theme}/icon.png"):
            win.themes.append((theme, f"{win.pathThemes}/{theme}/icon.png", f"{win.pathThemes}/{theme}/data.json"))
        else:
            win.themes.append((theme, ""))

    for theme in os.listdir(win.dirThemes):
        if os.path.isfile(f"{win.dirThemes}/{theme}/icon.png"):
            win.themes.append((theme, f"{win.dirThemes}/{theme}/icon.png", f"{win.dirThemes}/{theme}/data.json"))
        else:
            win.themes.append((theme, ""))
