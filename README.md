# 🌌 AstroCategorizer

A sleek, modern Python desktop application designed for amateur astronomers and astrophotographers to organize, categorize, and archive their celestial captures.

![AstroCategorizer Logo](logo.png)

## ✨ Features

- **Sequential Intro**: Professional splash screen with smooth fade-in and cross-fade to the main application.
- **Dynamic Image Grid**: Automated layout adapting to window size, displaying large thumbnails of your captures.
- **Instant Sidebar**: View high-resolution previews and edit metadata without leaving the main view.
- **Automatic Focal Length Categorization**: Enter focal length in mm and the app automatically labels it as Wide Field, Deep Sky, or Ultra Deep Sky.
- **Mass Tagging**: Select multiple images at once to apply common categories, focal lengths, or descriptions in one click.
- **Show in Explorer**: Quickly jump to the original file location on your disk.
- **Local Database**: All metadata is stored in a lightweight SQLite database in your local AppData, ensuring your organization persists across sessions.
- **Dark Mode UI**: A fully themed, immersive dark interface with custom-styled scrollbars and dark title bars.

## 📦 Installation

### Windows (Installer)
1. Download the latest `AstroCategorizer_Setup.exe` from the Releases section.
2. Run the installer and follow the instructions.
3. Launch from the Desktop or Start Menu.

### From Source (Python)
If you want to run the code directly:
1. Clone the repository: `git clone https://github.com/USERNAME/AstroCategorizer.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python main.py`

## 🛠️ Built With

- **Python 3.14+**
- **PyQt5**: For the hardware-accelerated GUI.
- **SQLite**: For robust local data management.
- **PyInstaller**: For bundling into a standalone executable.
- **Inno Setup**: For the professional Windows installer.

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

