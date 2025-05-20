<div align="center">

<img src="./assets/polsu/Polsu.png" alt="Polsu" width="100" height="100" style="border-radius:20px"/>

# Polsu's Overlay
A Hypixel Bedwars Overlay in Python, 100% free and open source!

<a href="https://github.com/Polsu-Development/PolsuOverlay/releases"><img src="https://img.shields.io/github/downloads/Polsu-Development/PolsuOverlay/total" alt="Downloads"></a>
<a href="https://discord.polsu.xyz"><img src="https://img.shields.io/discord/761623845119328257?color=7289DA&label=Discord" alt="Discord"></a>
<a><img src="https://wakatime.com/badge/user/ae13d286-a127-41f2-b631-4c4b2e09d04c/project/bdf90bf4-bb4f-4adb-8305-c4523e188b2c.svg" alt="Wakatime"></a>

</div>
  
> [!WARNING]
> Hypixel pushed an update which hides player usernames in pre-game lobbies. This means the overlays can't get the player usernames before the game starts!  
> However, Polsu Overlay still works in-game (run /who).
  
# 📖 Table of Contents

- [📝 About](#-about)
- [📥 Installation](#-installation)
- [📄 Usage](#-usage)
    - [🔍 Features](#-features)
    - [🆕 Next Features](#-next-features)
    - [🐛 Known Bugs](#-known-bugs)
- [💻 Development](#-development)
    - [⚒️ Requirements](#-requirements)
    - [📥 Configuration](#-configuration)
    - [🏗️ Build](#-build)
- [📃 Credits](#-credits)
    - [💻 Developers](#-developers)
    - [📚 Libraries](#-libraries)
    - [🎨 Assets](#-assets)
- [📜 License](#-license)


# 📝 About

This is the second version of Polsu's Overlay, a powerful Hypixel Bedwars Overlay made in Python.  


# 📥 Installation

Download the latest version of Polsu's Overlay as an executable file (`.exe`) [here](https://github.com/Polsu-Development/PolsuOverlay/releases).  

You can also download the source code and run it with Python (see [Development](#-development)).

Or even download the source code and compile it yourself with [`PyInstaller`](https://www.pyinstaller.org/) (see [Development](#-development)).


# 📄 Usage

![](https://assets.polsu.xyz/overlay/beautiful.png)

Launch the Overlay and it will automatically ask you to enter your Polsu API Key (you can find it [here](https://polsu.xyz/api/apikey)).  

Then you just need to head over to the settings (click the Polsu logo) and choose your Minecraft client (or custom path).


## 🔍 Features
- Automatically shows stats of players who joined your lobby after you
- Shows party stats
- Shows if players are nicked
- Automatically claim your daily reward
- View your opponent’s quickbuy
- Highly customisable, change the look of the interface. Craft custom themes, you can change:
    - fonts
    - colors
    - icons
    - images
- You can easily know if a player is good or not since the player gets highlighted
- Shows player heads, stars, name, winstreak, fkdr, finals, wlr, wins, bblr, beds and index stats
- You can manually add a player to the overlay by doing `/msg +<PLAYER>` or `/w +<PLAYER>` in game
- You can manually clear the stats list
- Displays game duration at the top of the window
- Displays player table count
- Tags:
    - Party
    - Nicked
- Ranks (emojis):
    - Overlay User 🎮
    - Premium ✨
    - VIP 🔗
    - Staff 🔨
    - Developer 💻
    - Owner 👑
- Requested players stats are temporarily saved
- Automatic `/who`
- Discord Rich Presence
- Customizable window opacity, size & opacity
- Custom logs path
- Blacklist System
    - Local blacklists (unlimited)
    - Polsu blacklist

## 🆕 Next Features
- Shows stats of the player who mentioned you in the lobby  
- Keybinds  

## 🐛 Known Bugs
*None for the moment.*


# 💻 Development

### ⚒️ Requirements

- [`Python`](https://www.python.org/downloads/): To unlock all the power of Python (`v3.11`)

### 📥 Configuration

Create a virtual environment
```shell
python3.11 -m venv venv
```

Activate the virtual environment
```shell
# Windows
venv\Scripts\activate.bat

# Linux
source venv/bin/activate
```

Install the dependencies
```shell
pip install -r requirements.txt
```

Run the program
```shell
python main.py
```

### 🏗️ Build

Install [`PyInstaller`](https://www.pyinstaller.org/)
```shell
pip install pyinstaller
```

Build the executable file
```shell
pyinstaller --noconfirm build.spec
```

The executable file will be in the `dist` folder.  
You can now run it!  


# 💎 Support us

Hosting our services is not free, so if you like our work, please consider supporting us by buying a premium subscription on our website [here](https://premium.polsu.xyz).  
By becoming a premium user, you not only gain our gratitude, but you also get access to exclusive features, limited only to donators on our Discord bot, Polsu!  

**We hope we can continue to provide you with the best free services possible, and we thank you for your support!**


# 📃 Credits

## 💻 Developers

This overlay was entirely made & designed by [Polsulpicien](https://github.com/Polsulpicien).

Special thanks to:
- [Zickles](https://github.com/Zickles)  
- [phiwijo](https://github.com/phiwijo)  
for adding a linux support to the overlay.  
- [Dueel](https://github.com/Dueel)  
for adding support for custom fonts.  


## 📚 Libraries

- [`PyQt5`](https://pypi.org/project/PyQt5/): Python bindings for the Qt cross-platform application and UI framework (`v5.15.2`)
- [`requests`](https://pypi.org/project/requests/): Python HTTP for Humans (`v2.26.0`)
- [`asyncio`](https://docs.python.org/3/library/asyncio.html): Asynchronous I/O, event loop, coroutines and tasks (`v3.11.0`)
- [`aiohttp`](https://docs.aiohttp.org/en/stable/): HTTP client/server for asyncio (`v3.7.4.post0`)
- [`pypresence`](https://pypi.org/project/pypresence/): Discord RPC client library for Python (`v4.2.0`)
- [`keyboard`](https://pypi.org/project/keyboard/): Hook and simulate keyboard events on Windows and Linux (`v0.13.5`)
- [`DateTime`](https://pypi.org/project/DateTime/): A Python DateTime library (`v4.3`)
- [`pystray`](https://pypi.org/project/pystray/): A cross-platform API for writing system tray applications in Python (`v0.17.0`)
- [`Pillow`](https://pypi.org/project/Pillow/): Python Imaging Library (`v8.4.0`)
- [`notify-py`](https://pypi.org/project/notify-py/): A cross-platform Python package to display desktop notifications (`v0.4.2`)
- [`pyqt_frameless_window`](https://pypi.org/project/pyqt-frameless-window/): A PyQt5 widget that can be used to create frameless windows (`v1.0.0`)
- [`packaging`](https://pypi.org/project/packaging/): Core utilities for Python packages (`v21.3`)
- [`pywinctl`](https://pypi.org/project/pywinctl/): A Python library for controlling Windows (`v0.1.0`)
- [`PyInstaller`](https://www.pyinstaller.org/): A program that freezes (packages) Python programs into stand-alone executables (`v4.5.1`)

## 🎨 Assets

- `Copyright 2023 Fonticons, Inc.` • Overlay Icons (https://fontawesome.com/)
- `Copyright 2017 Jacob Debono` • Minecraft Font
- `Copyright 2023 Polsu Development` • Polsu's Overlay Logo (https://polsu.xyz)


# 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

```py
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                                                        ┃
# ┃                         Polsu                          ┃
# ┃                                                        ┃
# ┃          A Hypixel Bedwars Overlay in Python,          ┃
# ┃               100% free and open source!               ┃
# ┃                                                        ┃
# ┃ • https://polsu.xyz                                    ┃
# ┃ • https://invite.polsu.xyz                             ┃
# ┃ • https://api.polsu.xyz                                ┃
# ┃ • https://discord.polsu.xyz                            ┃
# ┃ • https://premium.polsu.xyz                            ┃
# ┃ • https://overlay.polsu.xyz                            ┃
# ┃                                                        ┃
# ┃                                                        ┃
# ┃ © 2023 - 2024, Polsu Development - All rights reserved ┃
# ┃                                                        ┃
# ┃ Redistribution and use in source and binary forms,     ┃
# ┃ with or without modification, are permitted provided   ┃ 
# ┃ that thfollowing conditions are met:                   ┃
# ┃                                                        ┃
# ┃ 1. Redistributions of source code must retain the      ┃
# ┃    above copyright notice, this list of                ┃
# ┃    conditions and the following disclaimer.            ┃
# ┃                                                        ┃
# ┃ 2. Redistributions in binary form must reproduce the   ┃
# ┃    above copyright notice, this list                   ┃
# ┃    of conditions and the following disclaimer in the   ┃
# ┃    documentation and/or other materials provided       ┃
# ┃    with the distribution.                              ┃
# ┃                                                        ┃
# ┃ 3. Neither the name of Polsu Overlay nor the           ┃
# ┃    names of its contributors may be used to endorse    ┃
# ┃    or promote products derived from this software      ┃
# ┃    without specific prior written permission.          ┃
# ┃                                                        ┃
# ┃ THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS     ┃
# ┃ AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED    ┃
# ┃ WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED ┃
# ┃ WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A        ┃
# ┃ PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL   ┃
# ┃ THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR     ┃
# ┃ ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,  ┃
# ┃ OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   ┃
# ┃ TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS  ┃
# ┃ OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)    ┃
# ┃ HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER ┃
# ┃ IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      ┃
# ┃ NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE ┃
# ┃ USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           ┃
# ┃ POSSIBILITY OF SUCH DAMAGE.                            ┃
# ┃                                                        ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  
``` 
