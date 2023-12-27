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
from ..PolsuAPI import Polsu


from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer


import asyncio
import traceback


class APIKeyWorker(QThread):
    """
    APIKeyWorker is a QThread that will check if the API Key is valid or not
    """
    data = pyqtSignal(object, object)

    def __init__(self, parent, key: str) -> None:
        """
        Initialise the APIKeyWorker
        
        :param parent: The parent of the APIKeyWorker
        :param key: The API Key to check
        """
        super(QThread, self).__init__()
        self._parent = parent

        self.client = Polsu(key)
 

    def run(self) -> None:
        """
        Run the APIKeyWorker
        """
        try:
            data = asyncio.run(self.client.key.get())
            self.data.emit(self._parent, data)
        except:
            self.data.emit(self._parent, None)



def loadUpdate(parent) -> None:
    """
    Check if the API Key is valid or not
    
    :param parent: The parent of the APIKeyWorker
    """
    key = parent.apikeyBox.text()
    
    if len(key) == 36:
        parent.apikeyBox.setEnabled(False)

        try:
            parent.threads[key] = APIKeyWorker(parent, key)
            parent.threads[key].data.connect(apikeyUpdate)
            parent.threads[key].start()
        except:
            parent.win.logger.error(f"An error occurred while checking the API Key!\n\nTraceback: {traceback.format_exc()}")


def apikeyUpdate(parent, data) -> None:
    """
    Function called when the API Key is checked
    
    :param parent: The parent of the APIKeyWorker
    :param data: The data returned by the APIKeyWorker
    """
    if data:
        newString = f"{data.key[0:4]}XXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        parent.win.logger.info(f"API Key {newString} is valid!")

        parent.apikeyBox.setStyleSheet(parent.win.themeStyle.settingsAPIKeyStyleValid)

        parent.win.configAPIKey = data.key
        parent.win.player.client.updateKey(data.key)
        parent.win.settings.update("APIKey", data.key)

        parent.apikeyBox.setText("")
        parent.apikeyBox.setPlaceholderText(newString)
        parent.win.notif.send(title="Valid API Key", message="Your Polsu API Key is valid you can now launch a Bedwars game!")

        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec_()

        parent.apikeyBox.setStyleSheet(parent.win.themeStyle.settingsAPIKeyStyle)

        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec_()

        parent.win.logger.info("Closing API Key menu...")

        parent.win.close_apikey_menu()
    else:
        parent.win.logger.info(f"API Key {parent.apikeyBox.text()} is invalid!")

        parent.apikeyBox.setStyleSheet(parent.win.themeStyle.settingsAPIKeyStyleInvalid)

        parent.apikeyBox.setPlaceholderText("Enter your Polsu API Key")
        parent.win.notif.send(title="Invalid API Key!", message="The Polsu API Key you provided is invalid!")

        loop = QEventLoop()
        QTimer.singleShot(3000, loop.quit)
        loop.exec_()
        
        parent.apikeyBox.setStyleSheet(parent.win.themeStyle.settingsAPIKeyStyle)

        parent.apikeyBox.setEnabled(True)
        parent.apikeyBox.setText("")
