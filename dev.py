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
from src import DEV_MODE
from src.overlay import Overlay
from src.components.logger import Logger


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


import sys
import os
import traceback
import datetime


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


    # DEVELOPMENT MODE
    # 
    # This isn't designed to be used by anyone other than developers.
    # If you are not a developer, please download the latest release from https://overlay.polsu.xyz/download
    #
    # > The development bypasses the updater, and runs the overlay directly.
    # > The development version won't send login and logout attempts to the API.

    if DEV_MODE:
        logger.warning("You are running the overlay in development mode! This is not recommended, as it may cause issues.")
        logger.warning("If you are not a developer, please download the latest release from https://overlay.polsu.xyz/download")

        app = QApplication(sys.argv)

        try:
            Overlay(logger).show()
        except:
            logger.critical(f"An error occurred while updating the overlay!\n\nTraceback: {traceback.format_exc()}")

        sys.exit(app.exec_())
    else:
        logger.critical("You are running the development version of the overlay! However, you are not in development mode.")

        print("\n")
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃                                                                                                   ┃")
        print("┃                                             WARNING !                                             ┃")
        print("┃                                                                                                   ┃")
        print("┃ You are running the development version of the overlay! However, you are not in development mode. ┃")
        print("┃ Please set the DEV_MODE variable to True in the environment file! Or run the main.py file.        ┃")
        print("┃                                                                                                   ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("\n")

        sys.exit(1)
