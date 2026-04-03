# YPT

```
██    ██ ██████  ████████ 
 ██  ██  ██   ██    ██    
  ████   ██████     ██    
   ██    ██         ██    
   ██    ██         ██    
```

**Your Packet Tracer** - Install Cisco Packet Tracer on any Linux distro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/PyPI-ypt-blue)](https://pypi.org/project/ypt/)

---

**YPT** is a cross-distribution installer for Cisco Packet Tracer that extracts and configures the AppImage from the official `.deb` package. It solves the infamous login button browser opening issue on Wayland (especially KDE Plasma) and works on Fedora, openSUSE, Arch, Debian, Ubuntu, and other Linux distributions.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🐧 Cross-Distro** | Works on Fedora, openSUSE, Arch, Debian, Ubuntu, and more |
| **🔓 Login Fix** | Fixes broken login button on Wayland with URL handler shim |
| **🔒 No Root** | Installs to `~/.local/` - no sudo required |
| **🔍 Auto Discover** | Automatically finds `.deb` file in current directory |
| **🐛 Debug Mode** | Comprehensive logging to diagnose installation issues |

## 🚀 Quick Start

### Installation

```bash
pip install ypt
```

### Usage

```bash
# Download Packet Tracer .deb from Cisco NetAcad first, then:

# Auto-discover .deb in current directory and install
ypt

# Or specify the .deb file explicitly
ypt ~/Downloads/CiscoPacketTracer_900_Ubuntu_64bit.deb

# Test browser detection before installing
ypt --test-browser

# Enable debug mode for troubleshooting
ypt --debug

# Run diagnostics on existing installation
ypt --diagnose

# Uninstall Packet Tracer
ypt --uninstall
```

## 📥 Getting Cisco Packet Tracer

**IMPORTANT**: YPT does NOT redistribute Cisco software. You must:

1. **Register** for a free account at [Cisco Networking Academy](https://www.netacad.com)
2. **Download** the Packet Tracer `.deb` package for Ubuntu from your NetAcad account
3. **Run** `ypt` in the same directory as the downloaded `.deb` file

YPT only extracts and configures the software YOU downloaded from Cisco. We respect Cisco's End User License Agreement.

## 🔧 How It Works

### The Login Button Problem

Packet Tracer's AppImage on Wayland cannot open URLs because:
- Qt WebEngine can't access the system DBus session
- `xdg-open` isn't available inside the AppImage sandbox
- Standard browser detection fails on non-Debian distros

### YPT's Solution

YPT creates an intelligent wrapper system:

1. **Custom URL Handler**: Injects a `xdg-open` shim into the PATH
2. **Browser Detection**: Auto-detects your default browser (Firefox, Chrome, Chromium, Brave, etc.)
3. **Environment Setup**: Configures Qt WebEngine with proper browser executable
4. **Debug Logging**: Logs every URL opening attempt to `~/.local/share/PacketTracer/debug.log`

### Installation Structure

```
~/.local/
├── bin/
│   └── packettracer              # Launcher wrapper script
└── share/
    ├── PacketTracer/
    │   ├── packettracer.AppImage # Extracted from .deb
    │   └── shims/
    │       └── xdg-open          # URL handler shim
    ├── applications/
    │   └── cisco-packet-tracer.desktop
    └── icons/
        └── hicolor/256x256/apps/
            └── cisco-packet-tracer.png
```

## 📋 Requirements

- **Python**: 3.8 or higher
- **Linux Tools**: `ar` and `tar` (pre-installed on most distros)
- **Web Browser**: Firefox, Chrome, Chromium, Brave, or similar
- **Packet Tracer .deb**: Download from [netacad.com](https://www.netacad.com)

## 🐛 Troubleshooting

### Login Button Not Working

```bash
# Run diagnostics
ypt --diagnose

# Check debug log
cat ~/.local/share/PacketTracer/debug.log
```

### Browser Not Detected

```bash
# Test browser detection
ypt --test-browser

# Manually specify browser
ypt --browser firefox ~/path/to/PacketTracer.deb
```

### Installation Failed

```bash
# Run with debug mode
ypt --debug ~/path/to/PacketTracer.deb

# Verify .deb file integrity
file ~/path/to/PacketTracer.deb
```

## 📜 Legal Notice

**YPT is an installation utility only.** This software:

- ✅ Extracts the AppImage from the `.deb` package YOU downloaded
- ✅ Configures desktop integration and URL handlers
- ✅ Does NOT contain any Cisco software
- ✅ Does NOT redistribute Cisco Packet Tracer
- ✅ Does NOT modify Cisco's software

**You must**:
1. Download Packet Tracer yourself from [Cisco Networking Academy](https://www.netacad.com)
2. Accept Cisco's End User License Agreement
3. Comply with Cisco's terms of use

Cisco, Cisco Packet Tracer, and the Cisco logo are trademarks or registered trademarks of Cisco Systems, Inc. This project is not affiliated with, endorsed by, or sponsored by Cisco Systems, Inc.

## 📄 License

YPT is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The MIT License applies to YPT (the installer tool) only, not to Cisco Packet Tracer software.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🆘 Support

- **Issues**: [github.com/itxmjr/ypt/issues](https://github.com/itxmjr/ypt/issues)
- **Source Code**: [github.com/itxmjr/ypt](https://github.com/itxmjr/ypt)

## 🌟 Star History

If YPT helped you, consider giving it a star ⭐ on GitHub!

---

**Made with ❤️ for the Linux networking community**
