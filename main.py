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
from src import DEV_MODE
from src.updater import Updater
from src.overlay import Overlay
from src.components.logger import Logger
from src.utils.path import resource_path


from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


import sys
import os
import traceback
import datetime


if getattr(sys, 'frozen', False):
    import pyi_splash


def run(window: Updater, logger: Logger) -> None:
    """
    Run the overlay, depending on the value of the Updater window
    
    :param window: The Updater window
    :param logger: The logger
    """
    if window.value:
        window.close()
        try:
            Overlay(logger).show()
        except:
            logger.critical(f"An error occurred while running the overlay!\n\nTraceback: {traceback.format_exc()}")

            errorWindow = QMessageBox()
            errorWindow.setWindowTitle("An error occurred!")
            errorWindow.setWindowIcon(QIcon(f"{resource_path('assets')}/polsu/Polsu_.png"))
            errorWindow.setIcon(QMessageBox.Critical)
            errorWindow.setText("Something went wrong while running the overlay!\nPlease report this issue on GitHub or our Discord server.\nhttps://discord.polsu.xyz")
            errorWindow.setInformativeText(traceback.format_exception_only(type(sys.exc_info()[1]), sys.exc_info()[1])[0])
            errorWindow.setDetailedText(traceback.format_exc())
            errorWindow.setFocus()
            errorWindow.exec_()
    elif window.value == "Clean":
        window.progressBar.setMaximum(100)
        window.progressBar.setValue(100)

        window.close()

        # Cleanup, delete the old version
        def cleanup():
            with open("cleanup.bat", "w+") as file:
                file.write(f"DEL /F \"{sys.argv[0]}\" \nDEL /F \"{os.getcwd()}\\cleanup.bat\"")
            os.startfile(os.getcwd()+"\\cleanup.bat")

        cleanup()
    else:
        window.close()


if __name__ == '__main__':
    # DO NOT REMOVE THE FOLLOWING LINES!
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    #
    # This is a fix for the DPI scaling on Windows
    # Removing this might break the overlay window.

    logger = Logger()
    logger.info("-----------------------------------------------------------------------------------------------------")
    logger.info(f"Polsu Overlay - {datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"OS: {sys.platform}")
    logger.info(f"Running in: {'Development' if DEV_MODE else 'Production'} mode")
    logger.info("-----------------------------------------------------------------------------------------------------")
    logger.info("Starting Polsu Overlay...")

    app = QApplication(sys.argv)

    try:
        if getattr(sys, 'frozen', False):
            pyi_splash.close()

        window = Updater(logger)
        window.ended.connect(run)
        window.show()
    except:
        logger.critical(f"An error occurred while updating the overlay!\n\nTraceback: {traceback.format_exc()}")

    sys.exit(app.exec_())
