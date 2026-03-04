import os
import sys
import ctypes
import subprocess
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QListWidgetItem, QLabel, 
                             QComboBox, QLineEdit, QTextEdit, QFileDialog, QSplitter, 
                             QMessageBox, QFrame, QSizePolicy, QScrollArea)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer
import database

# Modern Dark Theme Constants
BG_COLOR = "#1e1e1e"
PANEL_BG = "#252526"
TEXT_COLOR = "#d4d4d4"
ACCENT_COLOR = "#007acc"
BORDER_COLOR = "#333333"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)
        
        layout = QVBoxLayout(self)
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Load logo.png
        pixmap = QPixmap(resource_path("logo.png"))
        if not pixmap.isNull():
            self.logo_label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("AstroCategorizer")
            self.logo_label.setStyleSheet(f"color: {ACCENT_COLOR}; font-size: 32px; font-weight: bold;")
            
        layout.addWidget(self.logo_label)
        self.resize(600, 600)
        
    def center(self):
        # Center splash on screen
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

    def start_animation(self, on_fade_out_callback):
        self.on_fade_out_callback = on_fade_out_callback
        self.center()
        self.show()
        
        # Fade In (0.5s)
        self.anim_in = QPropertyAnimation(self, b"windowOpacity")
        self.anim_in.setDuration(500)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Fade Out (0.5s)
        self.anim_out = QPropertyAnimation(self, b"windowOpacity")
        self.anim_out.setDuration(500)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim_out.finished.connect(self.deleteLater)
        
        # Timer for the fixed wait (0.5s)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.trigger_fade_out)
        
        self.anim_in.finished.connect(lambda: self.timer.start(500))
        self.anim_in.start()

    def trigger_fade_out(self):
        # Trigger the main app window show/fade-in
        if hasattr(self, 'on_fade_out_callback'):
            self.on_fade_out_callback()
        # Start our own fade out
        self.anim_out.start()
        
    def on_finished(self):
        # (This method is currently unused in the new logic but kept for safety if needed, 
        # but deleteLater in anim_out.finished is better)
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroCategorizer")
        self.resize(1200, 800)
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QListWidget {{
                background-color: {BG_COLOR};
                border: none;
                outline: 0;
            }}
            QListWidget::item:selected {{
                background-color: {ACCENT_COLOR};
                border-radius: 5px;
            }}
            QFrame#Sidebar {{
                background-color: {PANEL_BG};
                border-left: 1px solid {BORDER_COLOR};
            }}
            QPushButton {{
                background-color: #333333;
                color: {TEXT_COLOR};
                border: 1px solid #555555;
                padding: 6px 12px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #444444;
            }}
            QPushButton#PrimaryBtn {{
                background-color: {ACCENT_COLOR};
                border: none;
                font-weight: bold;
            }}
            QPushButton#PrimaryBtn:hover {{
                background-color: #005f9e;
            }}
            QComboBox, QLineEdit, QTextEdit {{
                background-color: #333333;
                color: {TEXT_COLOR};
                border: 1px solid #555555;
                padding: 4px;
                border-radius: 3px;
            }}
            QLabel {{
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background: #1e1e1e;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #555555;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #007acc;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        
        self.current_image_id = None
        self.current_image_path = None
        self.all_images = []
        
        # Set Application Icon
        self.setWindowIcon(QIcon(resource_path('logo.png')))
        
        self.setWindowOpacity(0.0)
        self.apply_dark_titlebar()
        
        self.init_ui()
        self.load_images_from_db()
        
    def apply_dark_titlebar(self, widget=None):
        target = widget if widget else self
        if sys.platform == "win32":
            try:
                hwnd = int(target.winId())
                set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
                rendering_policy = ctypes.c_int(1)
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_USE_IMMERSIVE_DARK_MODE_OLD = 19
                
                res = set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(rendering_policy), ctypes.sizeof(rendering_policy))
                if res != 0:
                    set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_OLD, ctypes.byref(rendering_policy), ctypes.sizeof(rendering_policy))
            except Exception as e:
                print("Could not set dark title bar:", e)

    def show_message(self, title, text, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(buttons)
        msg.setWindowIcon(QIcon(resource_path('logo.png')))
        self.apply_dark_titlebar(msg)
        return msg.exec_()
        
    def showEvent(self, event):
        super().showEvent(event)
        self.fade_in()

    def fade_in(self):
        self.anim_in = QPropertyAnimation(self, b"windowOpacity")
        self.anim_in.setDuration(400)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.setEasingCurve(QEasingCurve.OutQuad)
        self.anim_in.start()

    def closeEvent(self, event):
        if self.windowOpacity() == 1.0:
            event.ignore()
            self.fade_out()
        else:
            event.accept()

    def fade_out(self):
        self.anim_out = QPropertyAnimation(self, b"windowOpacity")
        self.anim_out.setDuration(400)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.setEasingCurve(QEasingCurve.InQuad)
        self.anim_out.finished.connect(self.close)
        self.anim_out.start()

        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # --- Top Filter Bar ---
        filter_bar = QHBoxLayout()
        
        self.btn_add_image = QPushButton("Add Images")
        self.btn_add_image.setObjectName("PrimaryBtn")
        self.btn_add_image.clicked.connect(self.add_images_dialog)
        
        self.filter_type = QComboBox()
        self.filter_type.addItems(["All Types", "Galaxies", "Nebulae", "Planets", "Clusters", "Landscapes", "Other"])
        self.filter_type.currentTextChanged.connect(self.apply_filters)
        
        self.filter_focal = QComboBox()
        self.filter_focal.addItems(["All Focal Lengths", "Wide Field (< 200mm)", "Deep Sky (200-1000mm)", "Ultra Deep Sky (> 1000mm)"])
        self.filter_focal.currentTextChanged.connect(self.apply_filters)
        
        filter_bar.addWidget(self.btn_add_image)
        filter_bar.addStretch()
        filter_bar.addWidget(QLabel("Filter by Type:"))
        filter_bar.addWidget(self.filter_type)
        filter_bar.addWidget(QLabel("Filter by Focal Length:"))
        filter_bar.addWidget(self.filter_focal)
        
        main_layout.addLayout(filter_bar)
        
        # --- Main Content Splitter ---
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 1. Grid
        self.image_grid = QListWidget()
        self.image_grid.setViewMode(QListWidget.IconMode)
        self.image_grid.setIconSize(QSize(200, 200))
        self.image_grid.setResizeMode(QListWidget.Adjust)
        self.image_grid.setSelectionMode(QListWidget.ExtendedSelection) # Enable multi-selection
        self.image_grid.setSpacing(10)
        self.image_grid.itemSelectionChanged.connect(self.on_selection_changed)
        splitter.addWidget(self.image_grid)
        
        # 2. Sidebar (Hidden by default)
        self.sidebar_outerWidget = QFrame()
        self.sidebar_outerWidget.setObjectName("Sidebar")
        self.sidebar_outerWidget.setMinimumWidth(400)
        self.sidebar_outerWidget.setStyleSheet(f"QFrame#Sidebar {{ background-color: {PANEL_BG}; border-left: 1px solid {BORDER_COLOR}; }}")
        
        sidebar_outer_layout = QVBoxLayout(self.sidebar_outerWidget)
        sidebar_outer_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_outer_layout.setSpacing(0)
        
        self.sidebar_container = QScrollArea()
        self.sidebar_container.setWidgetResizable(True)
        self.sidebar_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sidebar_container.setFrameShape(QFrame.NoFrame)
        self.sidebar_container.setStyleSheet("background-color: transparent;")
        
        self.sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        self.sidebar_container.setWidget(self.sidebar_widget)
        
        # Preview Image (Free scaling, no inner scroll)
        self.lbl_preview = QLabel()
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setStyleSheet("background-color: #000; border-radius: 5px;")
        self.lbl_preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sidebar_layout.addWidget(self.lbl_preview)
        
        # Filename
        self.lbl_filename = QLabel("filename.jpg")
        self.lbl_filename.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.lbl_filename.setAlignment(Qt.AlignCenter)
        self.lbl_filename.setWordWrap(True)
        sidebar_layout.addWidget(self.lbl_filename)
        
        # Type
        sidebar_layout.addWidget(QLabel("Type:"))
        self.cb_type = QComboBox()
        self.cb_type.addItems(["Galaxies", "Nebulae", "Planets", "Clusters", "Landscapes", "Other"])
        sidebar_layout.addWidget(self.cb_type)
        
        # Focal Length Input
        sidebar_layout.addWidget(QLabel("Focal Length (mm):"))
        self.le_focal = QLineEdit()
        self.le_focal.setPlaceholderText("e.g. 500")
        self.le_focal.textChanged.connect(self.auto_categorize_focal)
        sidebar_layout.addWidget(self.le_focal)
        
        # Focal Category (Manual override via buttons/combo)
        sidebar_layout.addWidget(QLabel("Focal Category:"))
        self.cb_focal_cat = QComboBox()
        self.cb_focal_cat.addItems(["Wide Field", "Deep Sky", "Ultra Deep Sky", "Unknown"])
        sidebar_layout.addWidget(self.cb_focal_cat)
        
        # Description
        sidebar_layout.addWidget(QLabel("Description:"))
        self.te_desc = QTextEdit()
        self.te_desc.setMinimumHeight(120)
        sidebar_layout.addWidget(self.te_desc)
        sidebar_layout.addStretch(1)
        
        sidebar_outer_layout.addWidget(self.sidebar_container)
        
        # Fixed Bottom Buttons Container
        self.bottom_btn_widget = QWidget()
        self.bottom_btn_widget.setStyleSheet(f"background-color: {PANEL_BG}; border-top: 1px solid {BORDER_COLOR};")
        btn_layout = QHBoxLayout(self.bottom_btn_widget)
        btn_layout.setContentsMargins(15, 15, 15, 15)
        
        self.btn_save = QPushButton("Save / Apply")
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_COLOR};
                border: none;
                font-weight: bold;
                color: {TEXT_COLOR};
            }}
            QPushButton:hover {{
                background-color: #005f9e;
            }}
        """)
        self.btn_save.clicked.connect(self.save_image_details)
        self.btn_save.setMinimumHeight(35)
        
        self.btn_explorer = QPushButton("Show in Explorer")
        self.btn_explorer.setStyleSheet("background-color: #444444; border: 1px solid #555555; padding: 6px 12px; border-radius: 4px; font-weight: bold;")
        self.btn_explorer.clicked.connect(self.show_in_explorer)
        self.btn_explorer.setMinimumHeight(35)
        
        self.btn_delete = QPushButton("Remove")
        self.btn_delete.setStyleSheet("background-color: #a4000f; border: none; font-weight: bold; border-radius: 4px;")
        self.btn_delete.clicked.connect(self.delete_current_image)
        self.btn_delete.setMinimumHeight(35)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_explorer)
        btn_layout.addWidget(self.btn_delete)
        
        sidebar_outer_layout.addWidget(self.bottom_btn_widget)
        
        splitter.addWidget(self.sidebar_outerWidget)
        
        # Set splitter sizes
        splitter.setSizes([800, 600])
        self.sidebar_outerWidget.hide() # hide initially
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_image_id and self.sidebar_outerWidget.isVisible():
            self.update_sidebar_preview()
        
    def add_images_dialog(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Select Images")
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
        dialog.setWindowIcon(QIcon(resource_path('logo.png')))
        self.apply_dark_titlebar(dialog)
        
        if dialog.exec_():
            files = dialog.selectedFiles()
            if files:
                for file_path in files:
                    database.add_image(file_path)
                self.load_images_from_db()
            
    def load_images_from_db(self):
        self.all_images = database.get_all_images()
        self.apply_filters()
        
    def apply_filters(self):
        type_filter = self.filter_type.currentText()
        focal_filter = self.filter_focal.currentText()
        
        self.image_grid.clear()
        
        for img_data in self.all_images:
            # Check type filter
            if type_filter != "All Types" and img_data['type'] != type_filter:
                continue
                
            # Check focal filter
            if focal_filter != "All Focal Lengths":
                if "Wide Field" in focal_filter and img_data['focal_category'] != "Wide Field":
                    continue
                if "Deep Sky" in focal_filter and "Ultra" not in focal_filter and img_data['focal_category'] != "Deep Sky":
                    continue
                if "Ultra Deep Sky" in focal_filter and img_data['focal_category'] != "Ultra Deep Sky":
                    continue

            # Check if file exists to display it
            if not os.path.exists(img_data['path']):
                continue
                
            item = QListWidgetItem()
            # Generate thumbnail
            pixmap = QPixmap(img_data['path'])
            if not pixmap.isNull():
                pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                item.setIcon(QIcon(pixmap))
                
            item.setText(img_data['filename'])
            item.setTextAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            # Store data in item
            item.setData(Qt.UserRole, img_data)
            self.image_grid.addItem(item)
            
    def focusOutEvent(self, event):
        super().focusOutEvent(event)

    def on_selection_changed(self):
        selected_items = self.image_grid.selectedItems()
        
        if not selected_items:
            self.sidebar_outerWidget.hide()
            self.current_image_id = None
            self.current_image_path = None
            return

        # Single selection mode
        if len(selected_items) == 1:
            item = selected_items[0]
            img_data = item.data(Qt.UserRole)
            self.current_image_id = img_data['id']
            self.current_image_path = img_data['path']
            
            self.sidebar_outerWidget.show()
            
            from PyQt5.QtWidgets import QApplication
            QApplication.processEvents()
            
            self.lbl_filename.setText(img_data['filename'])
            self.update_sidebar_preview()
                
            self.cb_type.setCurrentText(img_data['type'] if img_data['type'] else "Other")
            self.le_focal.setText(str(img_data['focal_length']) if img_data['focal_length'] else "")
            self.cb_focal_cat.setCurrentText(img_data['focal_category'] if img_data['focal_category'] else "Unknown")
            self.te_desc.setText(img_data['description'] if img_data['description'] else "")
            self.le_focal.setEnabled(True)
            self.te_desc.setEnabled(True)
            
        # Multi-selection mass-edit mode
        else:
            self.current_image_id = None
            self.current_image_path = None
            self.sidebar_outerWidget.show()
            self.lbl_filename.setText(f"Multiple Images Selected ({len(selected_items)})")
            self.lbl_preview.clear()
            self.lbl_preview.setText(f"Mass Editing {len(selected_items)} Images")
            
            # Optionally disable fields that shouldn't be bulk-edited if needed, but we allow bulk editing type/focal cat
            self.le_focal.setText("")
            self.te_desc.setText("")
            self.cb_type.setCurrentIndex(0)
            self.cb_focal_cat.setCurrentIndex(0)
            
            # The description and exact focal length mm in mass edit mode might be left empty if changing them is risky,
            # or we let them assign the same description to all. We allow it here.

    def update_sidebar_preview(self):
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            return
            
        pixmap = QPixmap(self.current_image_path)
        if not pixmap.isNull():
            # Scale to full width of the sidebar viewport
            # Margins inside sidebar are 15 on each side + some padding
            target_width = self.sidebar_container.viewport().width() - 32 
            if target_width > 0:
                pixmap = pixmap.scaledToWidth(target_width, Qt.SmoothTransformation)
                self.lbl_preview.setPixmap(pixmap)
        
    def auto_categorize_focal(self, text):
        try:
            mm = float(text)
            if mm < 200:
                self.cb_focal_cat.setCurrentText("Wide Field")
            elif 200 <= mm <= 1000:
                self.cb_focal_cat.setCurrentText("Deep Sky")
            else:
                self.cb_focal_cat.setCurrentText("Ultra Deep Sky")
        except ValueError:
            pass # Invalid number
            
    def save_image_details(self):
        selected_items = self.image_grid.selectedItems()
        if not selected_items:
            return
            
        img_type = self.cb_type.currentText()
        focal_category = self.cb_focal_cat.currentText()
        description = self.te_desc.toPlainText()
        
        try:
            focal_length = float(self.le_focal.text()) if self.le_focal.text() else 0.0
        except ValueError:
            focal_length = 0.0
            
        for item in selected_items:
            img_data = item.data(Qt.UserRole)
            img_id = img_data['id']
            
            # In mass edit, if a field is left entirely empty, we could choose to preserve the old value, 
            # but for simplicity, we apply exactly what's currently in the UI fields to all selected items.
            database.update_image(img_id, img_type, focal_length, focal_category, description)
            
        msg_text = f"Saved details for {len(selected_items)} image(s)!"
        self.show_message("Success", msg_text)
        
        # Remember selected ids to re-select them after refresh
        selected_ids = [item.data(Qt.UserRole)['id'] for item in selected_items]
        
        self.load_images_from_db() # Refresh
        
        # Restore selection
        for i in range(self.image_grid.count()):
            item = self.image_grid.item(i)
            if item.data(Qt.UserRole)['id'] in selected_ids:
                item.setSelected(True)

    def delete_current_image(self):
        selected_items = self.image_grid.selectedItems()
        if not selected_items:
            return
            
        count = len(selected_items)
        reply = self.show_message('Confirm', f'Are you sure you want to remove {count} image(s) from the application?', 
                                  QMessageBox.Question, QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for item in selected_items:
                img_data = item.data(Qt.UserRole)
                database.delete_image(img_data['id'])
                
            self.sidebar_outerWidget.hide()
            self.image_grid.clearSelection()
            self.current_image_id = None
            self.load_images_from_db()

    def show_in_explorer(self):
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            self.show_message("Error", "File path doesn't exist anymore.", QMessageBox.Warning)
            return
            
        if sys.platform == "win32":
            subprocess.Popen(f'explorer /select,"{os.path.normpath(self.current_image_path)}"')
        else:
            # Fallback for other OS
            import webbrowser
            webbrowser.open('file://' + os.path.dirname(self.current_image_path))
