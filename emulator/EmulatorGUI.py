import os
import platform


class EmulatorGUI:
    '''
    private static class
    '''
    TOP_BAR = ['┌', '─', '┐']
    MID_BAR = ['├', '─', '┤']
    BTM_BAR = ['└', '─', '┘']
    CONTENT = ['│', ' ', '│']
    DOTS = '...'

    @staticmethod
    def clearTerminal():
        if platform.system() == "Windows":
            os.system("cls")
        else:  # assuming Unix-based systems
            os.system("clear")

    @staticmethod
    def singleFrame(content: list, width: int, lineLimit: int = None, title: str = None) -> str:
        result = []
        header = EmulatorGUI.__frameHeader(width, title)
        result.append(header)
        if lineLimit is not None and len(content) > lineLimit:
            # remove excess content and replace with dots
            content = content[:lineLimit - 1]
            content.append(EmulatorGUI.DOTS)
        for contentString in content:
            contentLine = EmulatorGUI.__frameContent(width, contentString)
            result.append(contentLine)
        footer = EmulatorGUI.__frameFooter(width)
        result.append(footer)
        return '\n'.join(result)

    def __insertString(originalString: str, insertedString: str, index: int) -> str:
        n = len(insertedString)
        if index + n > len(originalString)-1:
            return originalString
        return originalString[:index]+insertedString+originalString[(index+n):]

    def __renderLine(width: int, start: str, middle: str, end: str, content: str = None, index: int = None) -> str:
        line = start + middle * (width - 2) + end
        if content is not None:
            line = EmulatorGUI.__insertString(line, content, index)
        return line

    def __frameHeader(width: int, title: str = None) -> str:
        start, middle, end = EmulatorGUI.TOP_BAR
        header = EmulatorGUI.__renderLine(width, start, middle, end, title, 2)
        return header

    def __frameContent(width: int, content: str = None) -> str:
        start, middle, end = EmulatorGUI.CONTENT
        dots = EmulatorGUI.DOTS
        index = 2
        n = len(content)
        m = len(dots)
        if n > m and index+n > width-1:
            content = content[:width-index-1-m]+dots
        contentLine = EmulatorGUI.__renderLine(
            width, start, middle, end, content, index)
        return contentLine

    def __frameFooter(width: int) -> str:
        start, middle, end = EmulatorGUI.BTM_BAR
        footer = EmulatorGUI.__renderLine(width, start, middle, end)
        return footer
