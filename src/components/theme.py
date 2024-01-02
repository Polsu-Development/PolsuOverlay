"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                      ┃
┃                                                  Polsu's Overlay                                                     ┃
┃                                                                                                                      ┃
┃                                                                                                                      ┃
┃  • A Hypixel Bedwars Overlay in Python, 100% free and open source!                                                   ┃
┃  > https://github.com/Polsu-Development/PolsuOverlay                                                                 ┃
┃  • Made by Polsu's Development Team                                                                                  ┃
┃                                                                                                                      ┃
┃                                                                                                                      ┃
┃                                                                                                                      ┃
┃                                   © 2023, Polsu Development - All rights reserved                                    ┃
┃                                                                                                                      ┃
┃  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the    ┃
┃  following conditions are met:                                                                                       ┃
┃                                                                                                                      ┃
┃  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the           ┃
┃     following disclaimer.                                                                                            ┃
┃                                                                                                                      ┃
┃  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the        ┃
┃     following disclaimer in the documentation and/or other materials provided with the distribution.                 ┃
┃                                                                                                                      ┃
┃  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,  ┃
┃  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE   ┃
┃  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  ┃
┃  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR     ┃
┃  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,   ┃
┃  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE    ┃
┃  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                                            ┃
┃                                                                                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
import json


class ThemeStyle:
    """
    A class representing a theme style
    """
    def __init__(self, window, theme: str = "Default Dark") -> None:
        """
        Initialise the theme style
        
        :param window: The main window
        :param theme: The theme
        """
        self.win = window

        themeConfig = False
        for t in self.win.themes:
            if t[0] == theme:
                with open(t[2], "r") as f:
                    self.config = json.load(f)
                themeConfig = True
                self.path = t[2].replace('/data.json', '')


        if not themeConfig:
            with open(f"{window.pathThemes}/Default Dark/data.json", "r") as f:
                self.config = json.load(f)
            self.win.configTheme = "Default Dark"
            self.win.settings.update("theme", "Default Dark")
            self.path = f"{window.pathThemes}/Default Dark"


        self.uparrow = str(self.win.getIconPath('uparrow', self.path)).replace('\\', '/')
        self.downarrow = str(self.win.getIconPath('downarrow', self.path)).replace('\\', '/')

        self.switchOn = str(self.win.getIconPath('switch-on', self.path)).replace('\\', '/')
        self.switchOff = str(self.win.getIconPath('switch-off', self.path)).replace('\\', '/')

        self.loadAllStyles()


    def loadAllStyles(self) -> None:
        """
        Load all styles
        """
        self.icon = self.config.get('overlay', {}).get('icon', 'Polsu_.png')
        self.name = self.config.get('overlay', {}).get('name', 'Polsu Overlay')

        if len(self.name) > len("Polsu Overlay") + 1:
            self.name = "Polsu Overlay"
        else:
            self.name += "         "

        self.color = self.config.get('color', '#000000')
        self.border = self.config.get('border', '#000000')
        self.table_highlight = self.config.get('table', {}).get('highlight', 'white')
        self.titleStyle = self.getTitleStyle()
        self.sideBarTextStyle = self.getSideBarTextStyle()
        self.deliveryTextTitleStyle = self.getDeliveryTextTitleStyle()
        self.deliveryTextSmallStyle = self.getDeliveryTextSmallStyle()
        self.sideBarButtonsStyle = self.getSideBarButtonsStyle()
        self.deliveryButtonsStyle = self.getDeliveryButtonsStyle()
        self.sideBarSmallButtonsStyle = self.getSideBarSmallButtonsStyle()
        self.buttonsStyle = self.getButtonStyle()
        self.closeButtonStyle = self.getCloseButtonStyle()
        self.searchBarStyle = self.getSearchBarStyle()
        self.timerBarStyle = self.getTimerBarStyle()
        self.tableStyle = self.getTableStyle()
        self.VscrollBarStyle = self.getVScrollBarStyle()
        self.HscrollBarStyle = self.getHScrollBarStyle()
        self.settingsMenuStyle = self.getSettingsMenuStyle()
        self.settingsAPIKeyStyle = self.getSettingsAPIKeyStyle()
        self.settingsAPIKeyStyleValid = self.getSettingsAPIKeyStyleValid()
        self.settingsAPIKeyStyleInvalid = self.getSettingsAPIKeyStyleInvalid()
        self.settingsAPIKeyFocus = self.getSettingsAPIKeyFocus()
        self.settingsLogPathStyle = self.getSettingsLogPathStyle()
        self.switchButtonStyle = self.getSwitchButtonStyle()
        self.sliderStyle = self.getSliderStyle()


    def getTitleStyle(self) -> str:
        """
        Get the title style
        
        :return: The title style
        """
        return f"""
            QLabel {{
                font-size: 27px;
                color: qlineargradient(x1:200, x2:1, stop:0 {self.config.get('overlay', {}).get('gradient', {}).get('end', '#59DDE0')}, stop:1 {self.config.get('overlay', {}).get('gradient', {}).get('start', '#2CA9EF')});
                font-weight: bold;
            }}
        """

    def getSideBarTextStyle(self) -> str:
        """
        Get the sidebar text style
        
        :return: The sidebar text style
        """
        return f"""
            QLabel {{
                color: {self.config.get('menu', {}).get('text', {}).get('color', 'white')}; 
                padding-left: 35px;
                font-size: 22px;
                font-weight: bold;
            }}
        """

    def getDeliveryTextTitleStyle(self) -> str:
        """
        Get the delivery text title style
        
        :return: The delivery text title style
        """
        return f"""
            QLabel {{
                color: {self.config.get('menu', {}).get('text', {}).get('color', 'white')}; 
                padding-left: 35px;
                font-size: 16px;
                font-weight: bold;
            }}
        """

    def getDeliveryTextSmallStyle(self) -> str:
        """
        Get the delivery text small style
        
        :return: The delivery text small style
        """
        return f"""
            QLabel {{
                color: {self.config.get('menu', {}).get('text', {}).get('color', 'white')}; 
                padding-left: 35px;
                font-size: 14px;
            }}
        """

    def getSideBarButtonsStyle(self) -> str:
        """
        Get the sidebar buttons style
        
        :return: The sidebar buttons style
        """
        return f"""
            QPushButton {{
                padding-right: 150px;
            }}
            QPushButton::hover {{
                background-color: {self.config.get('menu', {}).get('buttons-hover', {}).get('background-color', '#73737391')};
                border-radius: {self.config.get('menu', {}).get('buttons-hover', {}).get('border-radius', '8px')};
                padding-right: 150px;
            }}
            QPushButton:disabled {{
                background-color: {self.config.get('menu', {}).get('buttons-hover', {}).get('disabled-color', 'lightgray')};
                border-radius: {self.config.get('menu', {}).get('buttons-hover', {}).get('border-radius', '8px')};
            }}
        """
    
    def getDeliveryButtonsStyle(self) -> str:
        """
        Get the delivery buttons style
        
        :return: The delivery buttons style
        """
        return f"""
            QPushButton {{
                padding-right: 180px;
            }}
            QPushButton::hover {{
                background-color: {self.config.get('menu', {}).get('buttons-hover', {}).get('background-color', '#73737391')};
                border-radius: {self.config.get('menu', {}).get('buttons-hover', {}).get('border-radius', '8px')};
                padding-right: 180px;
            }}
            QPushButton:disabled {{
                background-color: {self.config.get('menu', {}).get('buttons-hover', {}).get('disabled-color', 'lightgray')};
                border-radius: {self.config.get('menu', {}).get('buttons-hover', {}).get('border-radius', '8px')};
            }}
        """

    def getSideBarSmallButtonsStyle(self) -> str:
        """
        Get the sidebar small buttons style
        
        :return: The sidebar small buttons style
        """
        return f"""
            QPushButton::hover {{
                background-color: {self.config.get('menu', {}).get('smallButtons-hover', {}).get('background-color', '#73737391')};
                border-radius: {self.config.get('menu', {}).get('smallButtons-hover', {}).get('border-radius', '8px')};
            }}
            QPushButton:disabled {{
                background-color: {self.config.get('menu', {}).get('smallButtons-hover', {}).get('disabled-color', 'lightgray')};
                border-radius: {self.config.get('menu', {}).get('smallButtons-hover', {}).get('border-radius', '8px')};
            }}
        """
    
    def getButtonStyle(self) -> str:
        """
        Get the button style
        
        :return: The button style
        """
        return f"""
            QPushButton::hover {{
                background-color: {self.config.get('buttons-hover', {}).get('background-color', '#73737391')}; 
                border-radius: {self.config.get('buttons-hover', {}).get('border-radius', '8px')};
            }}
            QPushButton:disabled {{
                background-color: {self.config.get('menu', {}).get('buttons-hover', {}).get('disabled-color', 'gray')};
                border-radius: {self.config.get('menu', {}).get('buttons-hover', {}).get('border-radius', '8px')};
            }}
        """

    def getCloseButtonStyle(self) -> str:
        """
        Get the close button style
        
        :return: The close button style
        """
        return f"""
            QPushButton::hover {{
                background-color: {self.config.get('close-button', {}).get('background-color', 'red')}; 
                border-radius: {self.config.get('close-button', {}).get('border-radius', '8px')};
            }}
        """

    def getSearchBarStyle(self) -> str:
        """
        Get the search bar style
        
        :return: The search bar style
        """
        return f"""
            QLineEdit {{ 
                color: {self.config.get('searchBar', {}).get('color', 'lightgrey')};
                border-width: {self.config.get('searchBar', {}).get('border-width', '2px')}; 
                border-radius: {self.config.get('searchBar', {}).get('border-radius', '10px')};
                border-style: {self.config.get('searchBar', {}).get('border-style', 'solid')}; 
                border-color: {self.config.get('searchBar', {}).get('border-color', 'white')}; 
                padding-left: 20px;
                padding-top: -2px;
                padding-right: 6px;
            }}
            QLineEdit[text=\"\"]{{
                color: {self.config.get('searchBar', {}).get('default', 'lightgrey')};
                font-weight: bold;
            }}
            QLineEdit::hover {{
                background-color: {self.config.get('searchBar', {}).get('hover-color', '#73737391')};
            }}
            QLineEdit:disabled {{
                background-color: {self.config.get('searchBar', {}).get('disabled-color', 'gray')};
            }}
        """

    def getTimerBarStyle(self) -> str:
        """
        Get the timer bar style
        
        :return: The timer bar style
        """
        return f"""
            QLineEdit {{ 
                color: {self.config.get('searchBar', {}).get('color', 'lightgrey')};
                border-width: {self.config.get('searchBar', {}).get('border-width', '2px')}; 
                border-radius: {self.config.get('searchBar', {}).get('border-radius', '10px')};
                border-style: {self.config.get('searchBar', {}).get('border-style', 'solid')}; 
                border-color: {self.config.get('searchBar', {}).get('border-color', 'white')}; 
                padding-left: 20px;
                padding-top: -2px;
                font-weight: bold;
            }}
        """

    def getTableStyle(self) -> str:
        """
        Get the table style
        
        :return: The table style
        """
        return f"""
            QTableView {{
                color: {self.config.get('table', {}).get('color', 'white')};
                border: 0px;
            }}
            QHeaderView::section {{
                background-color: transparent;
                color: {self.config.get('table', {}).get('color', 'white')};
            }}
            QHeaderView::section:horizontal {{
                border: 1px solid {self.config.get('table', {}).get('border', 'white')};
                border-top: 0px;
                border-left: 0px;
                border-right: 0px;
            }}
            QHeaderView::down-arrow {{
                image: url({self.downarrow});
                height: 12px;
                width: 12px;
            }}
            QHeaderView::up-arrow {{
                image: url({self.uparrow});
                height: 12px;
                width: 12px;
            }}
            QToolTip {{ 
                background-color: {self.config.get('table', {}).get('tooltip', {}).get('background', '#404040')}; 
                color: {self.config.get('table', {}).get('tooltip', {}).get('color', 'white')}; 
                border: 1px solid {self.config.get('table', {}).get('tooltip', {}).get('border', 'white')};
                border-radius: {self.config.get('table', {}).get('tooltip', {}).get('border-radius', '8px')};
            }}
        """

    def getVScrollBarStyle(self) -> str:
        """
        Get the vertical scrollbar style
        
        :return: The vertical scrollbar style
        """
        return f"""
            QScrollBar {{
                background: {self.config.get('scrollBar', {}).get('background', 'white')};
                margin: 0px 0px 0px 0px;
                margin-left: 5px;
                width: 10px;
            }}
            QScrollBar::handle {{
                background: {self.config.get('scrollBar', {}).get('color', self.color)};
            }}
            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal, 
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                border: none;
                background: none;
                color: none;
            }}
            QScrollBar::add-line, QScrollBar::sub-line {{
                border:none;
                background-color:none;
            }}
        """

    def getHScrollBarStyle(self) -> str:
        """
        Get the horizontal scrollbar style
        
        :return: The horizontal scrollbar style
        """
        return f"""
            QScrollBar {{
                background: {self.config.get('scrollBar', {}).get('background', 'white')};
                margin: 0px 0px 0px 0px;
                margin-top: 5px;
                height: 10px;
            }}
            QScrollBar::handle {{
                background: {self.config.get('scrollBar', {}).get('color', self.color)};
            }}
            QScrollBar::left-arrow:vertical, QScrollBar::right-arrow:vertical, 
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                border: none;
                background: none;
                color: none;
            }}
            QScrollBar::add-line, QScrollBar::sub-line {{
                border:none;
                background-color:none;
            }}
        """

    def getSettingsMenuStyle(self) -> str:
        """
        Get the settings menu style
        
        :return: The settings menu style
        """
        return f"""
            QComboBox {{
                background-color: transparent; 
                border-radius: {self.config.get('settings', {}).get('menu', {}).get('border-radius', '8px')};
                border-width: 2px; 
                border-style: {self.config.get('settings', {}).get('menu', {}).get('border-style', 'solid')}; 
                border-color: {self.config.get('settings', {}).get('menu', {}).get('border-color', 'gray')};
                color: {self.config.get('settings', {}).get('menu', {}).get('color', 'white')};
            }}
            QComboBox:editable {{
                background: white;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; 
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }}
            QComboBox::down-arrow {{
                image: url({self.downarrow});
                height: 20px;
                width: 20px;
                padding-right: 20px;
            }}
            QComboBox::down-arrow:on {{
                image: url({self.uparrow});
            }}
            QComboBox::hover {{
                background-color : {self.config.get('settings', {}).get('menu', {}).get('hover', {}).get('background-color', '#73737391')};
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.config.get('settings', {}).get('menu', {}).get('hover', {}).get('background-color', '#73737391')};
                selection-background-color: gray;
                selection-color: black;
                outline: none;
            }}
            QScrollBar:vertical {{
                background: rgb(231, 233, 234);
                margin: 0px 0px 0px 0px;
                width: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgb(138, 147, 155), stop: 0.5 rgb(138, 147, 155), stop:1 rgb(138, 147, 155));
                min-height: 0px
            }}
            QScrollBar::add-line:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 rgb(138, 147, 155), stop: 0.5 rgb(138, 147, 155), stop:1 rgb(138, 147, 155));
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}
            QScrollBar::sub-line:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0  rgb(138, 147, 155), stop: 0.5 rgb(138, 147, 155), stop:1 rgb(138, 147, 155));
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QComboBox:disabled {{
                background-color: {self.config.get('settings', {}).get('menu', {}).get('disabled-color', 'gray')};
            }}
        """

    def getSettingsAPIKeyStyle(self) -> str:
        """
        Get the settings api key style
        
        :return: The settings api key style
        """
        return f"""
            QLineEdit {{ 
                color: white;
                border-width: {self.config.get('settings', {}).get('searchBar', {}).get('border-width', '2px')}; 
                border-radius: {self.config.get('settings', {}).get('searchBar', {}).get('border-radius', '10px')};
                border-style: {self.config.get('settings', {}).get('searchBar', {}).get('border-style', 'solid')}; 
                border-color: {self.config.get('settings', {}).get('searchBar', {}).get('border-color', 'white')}; 
                padding-left: 22px;
                padding-top: -2px;
                padding-right: 6px;
            }}
            QLineEdit[text=\"\"]{{
                color: white;
                font-weight: bold;
            }}
            QLineEdit::hover {{
                background-color: {self.config.get('settings', {}).get('searchBar', {}).get('hover-color', '#73737391')};
            }}
        """

    def getSettingsAPIKeyStyleValid(self) -> str:
        """
        Get the settings api key style valid
        
        :return: The settings api key style valid
        """
        return f"""
            QLineEdit {{ 
                color: white;
                border-width: {self.config.get('settings', {}).get('searchBar', {}).get('border-width', '2px')}; 
                border-radius: {self.config.get('settings', {}).get('searchBar', {}).get('border-radius', '10px')};
                border-style: {self.config.get('settings', {}).get('searchBar', {}).get('border-style', 'solid')}; 
                border-color: lightgreen; 
                padding-left: 22px;
                padding-top: -2px;
                padding-right: 6px;
            }}
            QLineEdit[text=\"\"]{{
                color: white;
                font-weight: bold;
            }}
            QLineEdit::hover {{
                background-color: {self.config.get('settings', {}).get('searchBar', {}).get('hover-color', '#73737391')};
            }}
        """
    
    def getSettingsAPIKeyStyleInvalid(self) -> str:
        """
        Get the settings api key style invalid
        
        :return: The settings api key style invalid
        """
        return f"""
            QLineEdit {{ 
                color: white;
                border-width: {self.config.get('settings', {}).get('searchBar', {}).get('border-width', '2px')}; 
                border-radius: {self.config.get('settings', {}).get('searchBar', {}).get('border-radius', '10px')};
                border-style: {self.config.get('settings', {}).get('searchBar', {}).get('border-style', 'solid')}; 
                border-color: red; 
                padding-left: 22px;
                padding-top: -2px;
                padding-right: 6px;
            }}
            QLineEdit[text=\"\"]{{
                color: white;
                font-weight: bold;
            }}
            QLineEdit::hover {{
                background-color: {self.config.get('settings', {}).get('searchBar', {}).get('hover-color', '#73737391')};
            }}
        """

    def getSettingsAPIKeyFocus(self) -> str:
        """
        Get the settings api key focus
        
        :return: The settings api key focus
        """
        return f"""
            QLineEdit {{ 
                color: white;
                border-width: 3px; 
                border-radius: {self.config.get('settings', {}).get('searchBar', {}).get('border-radius', '10px')};
                border-style: solid;
                border-color: {self.config.get('settings', {}).get('searchBar', {}).get('border-color', 'white')}; 
                padding-left: 22px;
                padding-top: -2px;
                padding-right: 6px;
            }}
            QLineEdit[text=\"\"]{{
                color: white;
                font-weight: bold;
            }}
            QLineEdit::hover {{
                background-color: {self.config.get('settings', {}).get('searchBar', {}).get('hover-color', '#73737391')};
            }}
        """

    def getSettingsLogPathStyle(self) -> str:
        """
        Get the settings log path style
        
        :return: The settings log path style
        """
        return f"""
            QLineEdit {{ 
                color: white;
                border-width: {self.config.get('settings', {}).get('searchBar', {}).get('border-width', '2px')}; 
                border-radius: {self.config.get('settings', {}).get('searchBar', {}).get('border-radius', '10px')};
                border-style: {self.config.get('settings', {}).get('searchBar', {}).get('border-style', 'solid')}; 
                border-color: {self.config.get('settings', {}).get('searchBar', {}).get('border-color', 'white')}; 
                padding-left: 3px;
                padding-top: -2px;
                padding-right: 3px;
            }}
            QLineEdit[text=\"\"]{{
                color: white;
                font-weight: bold;
            }}
            QLineEdit::hover {{
                background-color: {self.config.get('settings', {}).get('searchBar', {}).get('hover-color', '#73737391')};
            }}
        """

    def getSwitchButtonStyle(self) -> str:
        """
        Get the switch button style
        
        :return: The switch button style
        """
        return f"""
            QCheckBox::indicator:unchecked {{
                image: url({self.switchOff});
                width: 36px;
                height: 36px;
            }}
            QCheckBox::indicator:checked {{
                image: url({self.switchOn});
                width: 36px;
                height: 36px;
            }}
            QCheckBox::indicator:disabled {{
                image: url({self.switchOff});
                width: 36px;
                height: 36px;
                background-color: {self.config.get('toggleButton', {}).get('disabled-color', 'black')};
                border-radius: 10px;
                padding-top: -8px;
                padding-bottom: -8px;
            }}
        """

    def getSliderStyle(self) -> str:
        """
        Get the slider style
        
        :return: The slider style
        """
        return """QSlider:horizontal {
            min-height: 40px;
        }
        QSlider::groove:horizontal {
            height: 4px;
            background: gray; 
        }
        QSlider::handle:horizontal {
            width: 30px;
            margin-top: -10px;
            margin-bottom: -10px;
            border-radius: 10px;
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.3, fx:0.5, fy:0.5, stop:0 rgba(39, 148, 245, 0.38));
        }
        QSlider::handle:horizontal:hover {
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.3, fx:0.5, fy:0.5, stop:0 rgba(39, 148, 255, 0.7));
        }
        """
