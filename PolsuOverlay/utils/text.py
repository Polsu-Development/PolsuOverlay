from re import findall, split


COLORS = {
    "0": (0, 0, 0),
    "1": (0, 0, 170),
    "2": (0, 170, 0),
    "3": (0, 170, 170),
    "4": (170, 0, 0),
    "5": (170, 0, 170),
    "6": (255, 170, 0),
    "7": (170, 170, 170),
    "8": (85, 85, 85),
    "9": (85, 85, 255),
    "a": (85, 255, 85),
    "b": (85, 255, 255),
    "c": (255, 85, 85),
    "d": (255, 85, 255),
    "e": (255, 255, 85),
    "f": (255, 255, 255),
}

def text2html(text: str, size: int = 11, colour: str = None, bold: bool = False):
    if colour:
        return f"<span style=\"color: #{colour}; font-size: {size}pt; {'font-weight: bold;' if bold else ''}\">{text}</span>"
    else:
        text = text.replace("§fYOUTUBE§c", "§fYT§c")

        colors = findall('§.', text)
        
        if len(colors) == 0:
            return text
        else:
            res = split('§.', text)

            for index, section in enumerate(res.copy()[:-1]):
                res[index] += f"<span style=\"color: rgb{COLORS[colors[index][1:]]}; font-size: {size}pt; {'font-weight: bold;' if bold else ''}\">"
                res[index+1] = res[index+1] + "</span>"

            return ''.join(res)