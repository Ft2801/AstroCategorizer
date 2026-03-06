import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
from ui import MainWindow, SplashScreen
import database

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def set_dark_theme(app):
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

def main():
    # Inizializza o aggiorna il database
    database.init_db()
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('logo.png')))
    
    set_dark_theme(app)
    
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)
    
    main_window = None

    def start_app():
        nonlocal main_window
        main_window = MainWindow()
        main_window.showMaximized()

    # Avvio Splash Screen
    splash = SplashScreen()
    splash.start_animation(start_app)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()