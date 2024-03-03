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
┃                               © 2023 - 2024, Polsu Development - All rights reserved                                 ┃
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
from src import __version__, __module__, EXECUTABLE, LINUX
from .utils.path import resource_path
from .components.logger import Logger


from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QProgressBar, QLabel, QMainWindow
from PyQt5.QtGui import QIcon
# from pyqt_frameless_window import FramelessDialog


import threading
import requests
import subprocess
import os
import traceback
import sys

from packaging import version
from time import sleep


class Updater(QMainWindow):
    """
    Updater class
    """
    ended = pyqtSignal(object, object)

    def __init__(self, logger: Logger) -> None:
        """
        Initialise the Updater class

        :param logger: The logger
        """
        super().__init__()
        self.logger = logger
        self.value = False

        self.setWindowTitle("Polsu Overlay - Update")

        self.setWindowIcon(QIcon(f"{resource_path('assets')}/polsu/Polsu_.png"))

        self.setFixedSize(400, 100)

        self.gridLayout = self.layout()

        self.label = QLabel(self)
        self.label.setText("Looking for updates...")
        self.label.setFixedSize(380, 20)
        self.label.setContentsMargins(20, 0, 0, 0)

        self.gridLayout.addWidget(self.label)

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(-1)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFixedSize(360, 20)

        self.gridLayout.addWidget(self.progressBar)
        self.gridLayout.setAlignment(self.progressBar, Qt.AlignCenter)

        self.setLayout(self.gridLayout)


        def update() -> None:
            """
            Update the overlay
            """
            self.logger.info(f"Checking for updates...")
            # try:
            #     subprocess.call(f"python -m main", shell=True)
            # except:
            #     pass

            try:
                latest_version = requests.get('https://api.polsu.xyz/internal/overlay/version')
                latest_version = latest_version.json().get("data", {}).get("version", None)

                if not latest_version:
                    self.logger.error(f"An error occurred while checking for updates! The server didn't respond.")
                    self.label.setText(f"Can't check for updates. Please try again later.")

                    self.value = False

                    self.progressBar.setMaximum(100)
                    self.progressBar.setValue(1)
                else:
                    latest_version = latest_version.replace("v", "")

                    self.logger.info(f"Latest version available: {latest_version}")
                    if version.parse(__version__) < version.parse(latest_version):
                        if EXECUTABLE:
                            self.logger.info(f"Found a new version! Downloading...")
                            self.label.setText(f"v{latest_version} - Found a new version! Updating...")

                            os.rename(sys.argv[0], os.path.join(os.getcwd(), f"[{__version__} - Outdated] PolsuOverlay.exe"))

                            sleep(2)

                            download_url = f"https://github.com/Polsu-Development/PolsuOverlay/releases/download/v{latest_version}/Polsu-Overlay.exe"

                            directory = os.path.join(os.getcwd(), "Polsu Overlay.exe")

                            self.label.setText(f"v{latest_version} - Downloading the latest version...")

                            # Download the file and save it
                            with requests.get(download_url, stream=True) as response:
                                if response.status_code == 404:
                                    self.logger.error(f"An error occurred while downloading the latest version!\n\nTraceback: {traceback.format_exc()}")
                                    self.label.setText(f"[404] Found a new version, but an error occurred while downloading it!")

                                    self.value = False
                                    self.ended.emit(self, self.logger)

                                    return
                                else:
                                    response.raise_for_status()

                                total_size = int(response.headers.get('Content-Length', 0))

                                bytes_downloaded = 0
                                with open(directory, 'wb') as f:
                                    for chunk in response.iter_content(chunk_size=8192):
                                        if chunk:
                                            f.write(chunk)
                                            f.flush()
                                            bytes_downloaded += len(chunk)
                                            
                                            # Calculate and update the progress
                                            progress = int((bytes_downloaded / total_size) * 100)
                                            self.label.setText(f"v{latest_version} - Download in progress... ({progress}%)")

                            self.logger.info(f"Download complete! Launching the new version...")
                            self.label.setText(f"v{latest_version} - Download complete!")

                            sleep(2)

                            self.label.setText(f"v{latest_version} - Launching the new version...")

                            sleep(2)

                            self.value = "Clean"
                            self.ended.emit(self, self.logger)

                            path = lambda *p: __module__+'\\'.join(p)
                            subprocess.call([directory, '-p', path().replace("\\", "/"), '-v', latest_version])
                        else:
                            self.logger.info(f"Found a new version! Download it from GitHub.")
                            self.label.setText(f"v{latest_version} - A new version is available! Download it from GitHub.")

                            self.value = False
                    else:
                        self.logger.info(f"No updates found. Launching the overlay (v{__version__})")
                        self.label.setText(f"No updates found.")

                        self.value = True
                        self.ended.emit(self, self.logger)
            except requests.exceptions.ConnectionError:
                self.logger.warning(f"An error occurred while updating the overlay! No internet connection!")
                self.label.setText(f"Can't check for updates. Please try again later.")

                self.progressBar.setMaximum(100)
                self.progressBar.setValue(1)

                self.value = False
            except:
                self.logger.error(f"An error occurred while updating the overlay!\n\nTraceback: {traceback.format_exc()}")
                self.label.setText(f"Something went wrong... Please try again later.")

                self.progressBar.setMaximum(100)
                self.progressBar.setValue(1)

                self.value = False

        self.logger.debug(f"Running on Linux: {'yes' if LINUX else 'no'}")
        self.logger.debug(f"Running as executable: {'yes' if EXECUTABLE else 'no'}")

        if LINUX:
            self.logger.info(f"Updater Initialised.")
            self.logger.info(f"Running version: v{__version__}")

            thread = threading.Thread(target=update, daemon=True)
            thread.start()
        else:
            self.label.setText("Uh Oh! Looks like you downloaded the wrong verison.\nLearn more at https://discord.polsu.xyz")
            self.label.setFixedSize(380, 60)
            self.label.setContentsMargins(20, 0, 0, 0)

            self.progressBar.setMaximum(1)
            self.progressBar.setValue(1)
            self.progressBar.hide()
