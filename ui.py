import os
import sys
import ctypes
import subprocess
import re
import math
import urllib.request
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit,
    QFileDialog, QSplitter, QMessageBox, QFrame,
    QSizePolicy, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QStatusBar,
    QDialog, QSpacerItem, QDateEdit, QApplication, QSizeGrip,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import (QPixmap, QIcon, QFont, QColor, QPainter,
                         QBrush, QCursor, QPolygon, QDoubleValidator)
from PyQt5.QtCore import (Qt, QSize, QPropertyAnimation, QEasingCurve,
                          QTimer, QThread, pyqtSignal, QDate, QRect, QPoint, QEvent)
import database

# ── Palette ────────────────────────────────────────────────────────────────────
BG_COLOR      = "#0f0f16"
PANEL_BG      = "#14141e"
TEXT_COLOR    = "#e0e0e0"
SUBTLE_TEXT   = "#7b8099"
ACCENT_COLOR  = "#4361ee"
ACCENT_HOVER  = "#3a56d4"
ACCENT2_COLOR = "#4cc9f0"
BORDER_COLOR  = "#1e1e30"
SUCCESS_COLOR = "#06d6a0"
DANGER_COLOR  = "#e63946"
STAR_COLOR    = "#ffd60a"
INPUT_BG      = "#1c1c28"

# ── Global stylesheet ──────────────────────────────────────────────────────────
GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {BG_COLOR};
    color: {TEXT_COLOR};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}}
QTableWidget {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    gridline-color: {BORDER_COLOR};
    outline: 0;
    alternate-background-color: #1c1c38;
}}
QTableWidget::item {{
    padding: 4px 6px;
}}
QTableWidget::item:selected {{
    background-color: rgba(67, 97, 238, 0.15);
    color: {TEXT_COLOR};
}}
QTableWidget::item:focus {{
    background-color: transparent;
    border: none;
    outline: none;
    padding: 4px 6px;
}}
QTableWidget:focus {{
    outline: none;
    border: 1px solid {BORDER_COLOR};
}}
QHeaderView::section {{
    background-color: {PANEL_BG};
    color: {ACCENT2_COLOR};
    padding: 6px 8px;
    border: none;
    border-bottom: 2px solid {ACCENT_COLOR};
    font-weight: bold;
    font-size: 9pt;
    letter-spacing: 0.5px;
}}
QFrame#Sidebar {{
    background-color: {PANEL_BG};
    border-left: 1px solid {BORDER_COLOR};
}}
/* ── Bottoni neutri ── */
QPushButton {{
    background-color: #2a2a50;
    color: {TEXT_COLOR};
    border: 1px solid #3a3a68;
    padding: 7px 14px;
    border-radius: 5px;
    font-size: 9.5pt;
}}
QPushButton:hover {{
    background-color: #36366a;
    border-color: {ACCENT_COLOR};
}}
QPushButton:pressed {{
    background-color: {ACCENT_COLOR};
    color: #ffffff;
}}
QPushButton:disabled {{
    background-color: #1e1e38;
    color: #555577;
    border-color: #2a2a48;
}}
/* ── Bottone primario ── */
QPushButton#PrimaryBtn {{
    background-color: {ACCENT_COLOR};
    color: #ffffff;
    border: none;
    font-weight: bold;
}}
QPushButton#PrimaryBtn:hover  {{ background-color: {ACCENT_HOVER}; }}
QPushButton#PrimaryBtn:pressed {{ background-color: #2e44b8; }}
/* ── Bottone successo ── */
QPushButton#SuccessBtn {{
    background-color: #0d7a5f;
    color: #ffffff;
    border: none;
    font-weight: bold;
}}
QPushButton#SuccessBtn:hover  {{ background-color: #0a9a78; }}
QPushButton#SuccessBtn:pressed {{ background-color: #076348; }}
/* ── Bottone pericolo ── */
QPushButton#DangerBtn {{
    background-color: {DANGER_COLOR};
    color: #ffffff;
    border: none;
    font-weight: bold;
}}
QPushButton#DangerBtn:hover  {{ background-color: #c92336; }}
QPushButton#DangerBtn:pressed {{ background-color: #a01c2b; }}
/* ── Input ── */
QComboBox, QLineEdit, QTextEdit, QDateEdit {{
    background-color: {INPUT_BG};
    color: {TEXT_COLOR};
    border: 1px solid #3a3a68;
    padding: 5px 8px;
    border-radius: 4px;
    selection-background-color: {ACCENT_COLOR};
}}
QComboBox:focus, QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {{
    border: 1px solid {ACCENT_COLOR};
}}
QComboBox::drop-down {{ border: none; background: transparent; }}
QComboBox::down-arrow {{
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {SUBTLE_TEXT};
    margin-right: 6px;
}}
QComboBox QAbstractItemView {{
    background-color: {INPUT_BG};
    border: 1px solid {ACCENT_COLOR};
    color: {TEXT_COLOR};
    selection-background-color: {ACCENT_COLOR};
}}
/* ── Scrollbar ── */
QScrollBar:vertical {{
    border: none; background: {BG_COLOR}; width: 8px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #3a3a68; min-height: 30px; border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{ background: {ACCENT_COLOR}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    border: none; background: {BG_COLOR}; height: 8px; margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: #3a3a68; min-width: 30px; border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{ background: {ACCENT_COLOR}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
/* ── Labels ── */
QLabel {{ background-color: transparent; }}
/* ── Status Bar ── */
QStatusBar {{
    background-color: {PANEL_BG};
    border-top: 1px solid {BORDER_COLOR};
    color: {SUBTLE_TEXT};
    font-size: 8.5pt;
    padding: 2px 8px;
}}
/* ── Tooltip ── */
QToolTip {{
    background-color: #252548;
    color: {TEXT_COLOR};
    border: 1px solid {ACCENT_COLOR};
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 9pt;
}}
/* ── Dialog ── */
QDialog {{
    background-color: {BG_COLOR};
    color: {TEXT_COLOR};
}}
"""


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Full constellation list
CONSTELLATIONS = [
    "", "Andromeda", "Antlia", "Apus", "Aquarius", "Aquila", "Ara",
    "Aries", "Auriga", "Boötes", "Caelum", "Camelopardalis", "Cancer",
    "Canes Venatici", "Canis Major", "Canis Minor", "Capricornus", "Carina",
    "Cassiopeia", "Centaurus", "Cepheus", "Cetus", "Chamaeleon", "Circinus",
    "Columba", "Coma Berenices", "Corona Australis", "Corona Borealis", "Corvus",
    "Crater", "Crux", "Cygnus", "Delphinus", "Dorado", "Draco", "Equuleus",
    "Eridanus", "Fornax", "Gemini", "Grus", "Hercules", "Horologium",
    "Hydra", "Hydrus", "Indus", "Lacerta", "Leo", "Leo Minor", "Lepus",
    "Libra", "Lupus", "Lynx", "Lyra", "Mensa", "Microscopium", "Monoceros",
    "Musca", "Norma", "Octans", "Ophiuchus", "Orion", "Pavo", "Pegasus",
    "Perseus", "Phoenix", "Pictor", "Pisces", "Piscis Austrinus", "Puppis",
    "Pyxis", "Reticulum", "Sagitta", "Sagittarius", "Scorpius", "Sculptor",
    "Scutum", "Serpens", "Sextans", "Taurus", "Telescopium", "Triangulum",
    "Triangulum Australe", "Tucana", "Ursa Major", "Ursa Minor", "Vela",
    "Virgo", "Volans", "Vulpecula",
]

OBJECT_TYPES = [
    "Galassie", "Nebulose", "Pianeti", "Ammassi",
    "Paesaggi", "Luna", "Sistema Solare", "Comete", "Altro"
]


# ─────────────────────────────────────────────────────────────────────────────
# Star Rating Widget
# ─────────────────────────────────────────────────────────────────────────────
class StarRatingWidget(QWidget):
    ratingChanged = pyqtSignal(int)

    def __init__(self, max_stars=5, parent=None):
        super().__init__(parent)
        self._max    = max_stars
        self._rating = 0
        self._hover  = 0
        self.setFixedSize(max_stars * 26, 26)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip("Clicca per valutare — clicca di nuovo sulla stessa stella per azzerare")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, val):
        self._rating = max(0, min(self._max, int(val or 0)))
        self.update()

    def _star_rect(self, i):
        size = 20
        x = i * (size + 4) + 2
        y = (self.height() - size) // 2
        return QRect(x, y, size, size)

    def _draw_star(self, painter, cx, cy, filled):
        r_o, r_i = 9, 3.8
        color = QColor(STAR_COLOR) if filled else QColor("#3a3a68")
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        pts = []
        for k in range(10):
            angle = math.radians(-90 + k * 36)
            r = r_o if k % 2 == 0 else r_i
            pts.append(QPoint(int(cx + r * math.cos(angle)), int(cy + r * math.sin(angle))))
        painter.drawPolygon(QPolygon(pts))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        filled_to = self._hover if self._hover > 0 else self._rating
        for i in range(self._max):
            r = self._star_rect(i)
            self._draw_star(p, r.center().x(), r.center().y(), i < filled_to)

    def mouseMoveEvent(self, event):
        self._hover = next((i + 1 for i in range(self._max)
                            if self._star_rect(i).contains(event.pos())), 0)
        self.update()

    def leaveEvent(self, event):
        self._hover = 0
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for i in range(self._max):
                if self._star_rect(i).contains(event.pos()):
                    nv = 0 if (i + 1) == self._rating else (i + 1)
                    self._rating = nv
                    self.update()
                    self.ratingChanged.emit(self._rating)
                    return


# ─────────────────────────────────────────────────────────────────────────────
# Sky Map Fetcher Thread
# ─────────────────────────────────────────────────────────────────────────────
class SkyMapFetcher(QThread):
    finished = pyqtSignal(QPixmap)
    error    = pyqtSignal(str)

    def __init__(self, constellation):
        super().__init__()
        self.constellation = constellation

    def run(self):
        try:
            if not self.constellation:
                self.error.emit("Inserisci una costellazione per caricare la mappa in stile Wikipedia.")
                return
            
            import json, urllib.parse, urllib.request
            
            c_name = self.constellation.strip()
            # Gestiamo le costellazioni IAU tramite i file SVG da Wikipedia/Wikimedia Commons
            filename = f"File:{c_name}_IAU.svg"
            url = (
                f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(filename)}"
                f"&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json"
            )
            
            req  = urllib.request.Request(url, headers={"User-Agent": "AstroCategorizer/2.0"})
            data = urllib.request.urlopen(req, timeout=12).read()
            js = json.loads(data)
            pages = js.get("query", {}).get("pages", {})
            page = list(pages.values())[0]
            
            if "imageinfo" not in page:
                # Se l'utente digita qualcosa di non standard o non in inglese
                self.error.emit(f"Mappa per la costellazione '{c_name}' non trovata su Wikimedia Commons.")
                return
                
            img_url = page["imageinfo"][0].get("thumburl", "")
            if not img_url:
                img_url = page["imageinfo"][0].get("url", "")
                
            if not img_url:
                self.error.emit("URL dell'immagine non trovato.")
                return

            req_img = urllib.request.Request(img_url, headers={"User-Agent": "AstroCategorizer/2.0"})
            img_data = urllib.request.urlopen(req_img, timeout=12).read()
            
            px = QPixmap()
            px.loadFromData(img_data)
            if px.isNull():
                self.error.emit("Dati SVG rasterizzati non validi.")
            else:
                self.finished.emit(px)
        except Exception as e:
            self.error.emit(str(e))

class SkyMapFetcherDSS2(QThread):
    finished = pyqtSignal(QPixmap)
    error    = pyqtSignal(str)

    def __init__(self, ra_deg, dec_deg, fov=3.0):
        super().__init__()
        self.ra  = ra_deg
        self.dec = dec_deg
        self.fov = fov

    def run(self):
        try:
            url = (
                "https://alasky.cds.unistra.fr/hips-image-services/hips2fits?"
                f"hips=CDS%2FP%2FDSS2%2Fcolor&width=420&height=280&fov={self.fov:.3f}&"
                f"projection=TAN&coordsys=icrs&ra={self.ra}&dec={self.dec}&format=jpg"
            )
            req  = urllib.request.Request(url, headers={"User-Agent": "AstroCategorizer/2.0"})
            data = urllib.request.urlopen(req, timeout=12).read()
            px   = QPixmap()
            px.loadFromData(data)
            if px.isNull():
                self.error.emit("Dati immagine non validi dal server.")
            else:
                self.finished.emit(px)
        except Exception as e:
            self.error.emit(str(e))

# ─────────────────────────────────────────────────────────────────────────────
# Stats Dialog
# ─────────────────────────────────────────────────────────────────────────────
class StatsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Statistiche Catalogo")
        self.setMinimumWidth(380)
        self.setStyleSheet(GLOBAL_STYLE)
        _apply_dark_titlebar(self)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        hdr = QLabel("📊  Statistiche del Catalogo")
        hdr.setStyleSheet(f"color: {ACCENT2_COLOR}; font-size: 13pt; font-weight: bold; padding-bottom: 4px;")
        layout.addWidget(hdr)
        layout.addWidget(_hsep())

        stats = database.get_stats()

        def stat_row(label, value, color=ACCENT2_COLOR):
            h = QHBoxLayout()
            lb = QLabel(label)
            lb.setStyleSheet(f"color: {SUBTLE_TEXT};")
            vl = QLabel(str(value))
            vl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 11pt;")
            h.addWidget(lb)
            h.addStretch()
            h.addWidget(vl)
            return h

        layout.addLayout(stat_row("Immagini nel catalogo", stats.get("total", 0)))
        layout.addLayout(stat_row("Con titolo personalizzato", stats.get("titled", 0), SUCCESS_COLOR))
        layout.addLayout(stat_row("Con coordinate AR/Dec", stats.get("with_coords", 0), ACCENT_COLOR))
        layout.addWidget(_hsep())

        type_hdr = QLabel("Distribuzione per tipo")
        type_hdr.setStyleSheet(f"color: {SUBTLE_TEXT}; font-size: 9pt; margin-top:2px;")
        layout.addWidget(type_hdr)

        for tname, cnt in stats.get("by_type", []):
            layout.addLayout(stat_row(f"  {tname or 'Non categorizzato'}", cnt, TEXT_COLOR))

        layout.addSpacerItem(QSpacerItem(0, 10))
        btn_close = QPushButton("Chiudi")
        btn_close.setObjectName("PrimaryBtn")
        btn_close.setMinimumHeight(32)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)


# ─────────────────────────────────────────────────────────────────────────────
# Full-Screen Image Viewer Dialog
# ─────────────────────────────────────────────────────────────────────────────
class ImageViewerDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(os.path.basename(image_path))
        self.setWindowFlags(Qt.Dialog | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setStyleSheet(GLOBAL_STYLE)
        self.setMinimumSize(800, 600)
        self.resize(1200, 850)
        _apply_dark_titlebar(self)

        self._path  = image_path
        self._base  = QPixmap(image_path)
        self._zoom  = 1.0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        tb_w = QWidget()
        tb_w.setStyleSheet(f"background-color: {PANEL_BG}; border-bottom: 1px solid {BORDER_COLOR};")
        tb = QHBoxLayout(tb_w)
        tb.setContentsMargins(8, 6, 8, 6)
        tb.setSpacing(6)

        for label, tip, fn in [
            ("🔍+",  "Zoom in  ( + )",         lambda: self._zoom_by(1.25)),
            ("🔍−",  "Zoom out  ( − )",         lambda: self._zoom_by(0.8)),
            ("⤢ Adatta",  "Adatta alla finestra ( F )",  self._fit),
            ("1:1",  "Dimensione originale",    lambda: self._set_zoom(1.0)),
        ]:
            b = QPushButton(label)
            b.setToolTip(tip)
            b.setMinimumHeight(28)
            b.clicked.connect(fn)
            tb.addWidget(b)

        tb.addStretch()
        fn_label = QLabel(os.path.basename(image_path))
        fn_label.setStyleSheet(f"color: {SUBTLE_TEXT};")
        tb.addWidget(fn_label)

        if not self._base.isNull():
            sz_label = QLabel(f"{self._base.width()} × {self._base.height()} px")
            sz_label.setStyleSheet(f"color: {SUBTLE_TEXT}; font-size: 8.5pt;")
            tb.addWidget(sz_label)

        layout.addWidget(tb_w)

        self._scroll = QScrollArea()
        self._scroll.setAlignment(Qt.AlignCenter)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._img_lbl = QLabel()
        self._img_lbl.setAlignment(Qt.AlignCenter)
        self._scroll.setWidget(self._img_lbl)
        self._scroll.setWidgetResizable(False)
        layout.addWidget(self._scroll)

        self._fit()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._fit()

    def _zoom_by(self, factor):
        self._set_zoom(self._zoom * factor)

    def _set_zoom(self, z):
        if self._base.isNull():
            return
        self._zoom = max(0.05, min(12.0, z))
        w = int(self._base.width()  * self._zoom)
        h = int(self._base.height() * self._zoom)
        scaled = self._base.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._img_lbl.setPixmap(scaled)
        self._img_lbl.resize(scaled.size())

    def _fit(self):
        if self._base.isNull():
            return
        vp = self._scroll.viewport().size()
        px = self._base.scaled(vp, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._zoom = min(px.width() / self._base.width(),
                         px.height() / self._base.height())
        self._img_lbl.setPixmap(px)
        self._img_lbl.resize(px.size())

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_Escape:             self.close()
        elif k in (Qt.Key_Plus, Qt.Key_Equal): self._zoom_by(1.25)
        elif k == Qt.Key_Minus:            self._zoom_by(0.8)
        elif k == Qt.Key_F:                self._fit()
        else:                              super().keyPressEvent(e)


# ─────────────────────────────────────────────────────────────────────────────
# Splash Screen
# ─────────────────────────────────────────────────────────────────────────────
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)

        layout = QVBoxLayout(self)
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)

        px = QPixmap(resource_path("logo.png"))
        if not px.isNull():
            self.logo_label.setPixmap(px.scaled(480, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("AstroCategorizer")
            self.logo_label.setStyleSheet(f"color:{ACCENT_COLOR};font-size:32px;font-weight:bold;")

        layout.addWidget(self.logo_label)
        self.resize(560, 560)

    def center(self):
        s = QApplication.primaryScreen().geometry()
        self.move((s.width() - self.width()) // 2, (s.height() - self.height()) // 2)

    def start_animation(self, callback):
        self._cb = callback
        self.center()
        self.show()

        self._in = QPropertyAnimation(self, b"windowOpacity")
        self._in.setDuration(450)
        self._in.setStartValue(0.0)
        self._in.setEndValue(1.0)
        self._in.setEasingCurve(QEasingCurve.InOutQuad)

        self._out = QPropertyAnimation(self, b"windowOpacity")
        self._out.setDuration(450)
        self._out.setStartValue(1.0)
        self._out.setEndValue(0.0)
        self._out.setEasingCurve(QEasingCurve.InOutQuad)
        self._out.finished.connect(self.deleteLater)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._fade_out)
        self._in.finished.connect(lambda: self._timer.start(600))
        self._in.start()

    def _fade_out(self):
        if hasattr(self, "_cb"):
            self._cb()
        self._out.start()


# ─────────────────────────────────────────────────────────────────────────────
# Helpers (module-level, reusable)
# ─────────────────────────────────────────────────────────────────────────────
def _apply_dark_titlebar(widget):
    if sys.platform == "win32":
        try:
            hwnd = int(widget.winId())
            val = ctypes.c_int(1)
            r = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ctypes.byref(val), ctypes.sizeof(val))
            if r != 0:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 19, ctypes.byref(val), ctypes.sizeof(val))
        except Exception:
            pass


def _hsep():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"color: {BORDER_COLOR};")
    return line


def _section_label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"color: {ACCENT2_COLOR}; font-weight: bold; font-size: 8pt;"
        f" letter-spacing: 1.5px; padding: 5px 0 2px 0;"
    )
    return lbl


def _parse_coordinates(ra_str, dec_str):
    """
    Accetta gradi decimali puri (es. '83.82' / '-5.39')
    oppure sessagesimale (es. '05h 35m 17s' / '-05° 23′ 28″').
    Ritorna (ra_deg, dec_deg) o (None, None).
    """
    ra_str  = ra_str.strip()
    dec_str = dec_str.strip()
    try:
        return float(ra_str), float(dec_str)
    except ValueError:
        pass
    try:
        rm = re.search(r'(\d+)\s*[hH°]\s*(\d+)\s*[mM\'′]\s*([\d.]+)', ra_str)
        dm = re.search(r'([+-]?\d+)\s*[°dD]\s*(\d+)\s*[\'mM′]\s*([\d.]+)', dec_str)
        if not rm or not dm:
            return None, None
        h, m, s = map(float, rm.groups())
        ra_deg  = (h + m / 60 + s / 3600) * 15.0
        ds, dmi, dse = dm.groups()
        d = float(ds)
        sign = -1 if d < 0 or ds.startswith('-') else 1
        dec_deg = sign * (abs(d) + float(dmi) / 60 + float(dse) / 3600)
        return ra_deg, dec_deg
    except Exception:
        return None, None


# ─────────────────────────────────────────────────────────────────────────────
# Main Window
# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroCategorizer")
        self.resize(1440, 900)
        self.setStyleSheet(GLOBAL_STYLE)
        self.setWindowIcon(QIcon(resource_path("logo.png")))
        self.setWindowOpacity(0.0)

        self.current_image_id   = None
        self.current_image_path = None
        self.all_images         = []
        self._map_fetcher       = None
        self._map_fetcher_dss2  = None # Aggiunto riferimento mancante
        self._is_loading        = False
        self._is_closing        = False # Flag di sicurezza chiusura

        _apply_dark_titlebar(self)
        self._build_ui()
        self._build_status_bar()
        self.load_images_from_db()

    # ── Fade ──────────────────────────────────────────────────────────────────
    def showEvent(self, e):
        super().showEvent(e)
        a = QPropertyAnimation(self, b"windowOpacity")
        a.setDuration(350); a.setStartValue(0.0); a.setEndValue(1.0)
        a.setEasingCurve(QEasingCurve.OutQuad); a.start()
        self._fade_in_anim = a

    def _safe_shutdown(self):
        """Spegne i thread e pulisce le risorse prima della chiusura."""
        def stop_thread(t):
            if t and t.isRunning():
                t.quit()
                if not t.wait(500):
                    t.terminate()
                    t.wait()
        
        stop_thread(getattr(self, "_map_fetcher", None))
        stop_thread(getattr(self, "_map_fetcher_dss2", None))

    def closeEvent(self, e):
        # Se siamo già in fase di chiusura animata, accetta e basta
        if hasattr(self, "_fade_out_active") and self._fade_out_active:
            e.accept()
            return

        # 1. CONTROLLO MODIFICHE (Bloccante)
        try:
            if self.sidebar_outerWidget.isVisible() and self.current_image_id:
                if self._check_unsaved_changes():
                    e.ignore()
                    return
        except Exception as ex:
            print(f"Errore durante check chiusura: {ex}")
            # In caso di errore nel check, meglio far chiudere l'app che bloccarla

        # 2. PROCEDURA DI CHIUSURA
        e.ignore()
        self._fade_out_active = True
        
        # Fermiamo i thread
        self._safe_shutdown()

        # Animazione di chiusura
        a = QPropertyAnimation(self, b"windowOpacity")
        a.setDuration(280); a.setStartValue(1.0); a.setEndValue(0.0)
        a.setEasingCurve(QEasingCurve.InQuad)
        
        def on_anim_finished():
            # Forza la chiusura bypassando closeEvent
            QApplication.quit()
            
        a.finished.connect(on_anim_finished)
        a.start()
        self._fade_out_anim = a

    # ── Status bar ────────────────────────────────────────────────────────────
    def _build_status_bar(self):
        sb = QStatusBar(self)
        self.setStatusBar(sb)
        self._status_lbl = QLabel("Pronto")
        sb.addPermanentWidget(self._status_lbl)

    def set_status(self, text, ms=0):
        self._status_lbl.setText(text)
        if ms:
            QTimer.singleShot(ms, lambda: self._status_lbl.setText("Pronto"))

    # ── Messagebox helper ─────────────────────────────────────────────────────
    def show_message(self, title, text,
                     icon=QMessageBox.Information,
                     buttons=QMessageBox.Ok):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(buttons)
        msg.setWindowIcon(QIcon(resource_path("logo.png")))
        msg.setStyleSheet(GLOBAL_STYLE)
        _apply_dark_titlebar(msg)
        return msg.exec_()

    # ─────────────────────────────────────────────────────────────────────────
    # BUILD UI
    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(8, 8, 8, 4)
        root.setSpacing(6)
        root.addLayout(self._build_toolbar())

        self.overlay_container = QWidget()
        overlay_layout = QVBoxLayout(self.overlay_container)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.addWidget(self._build_table_panel())
        
        root.addWidget(self.overlay_container)

        self._build_sidebar()
        self.sidebar_outerWidget.setParent(self.overlay_container)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(-6)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.sidebar_outerWidget.setGraphicsEffect(shadow)
        
        self.overlay_container.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == getattr(self, 'overlay_container', None) and event.type() == QEvent.Resize:
            rect = obj.rect()
            w = 460
            if hasattr(self, 'sidebar_outerWidget'):
                self.sidebar_outerWidget.setGeometry(
                    rect.width() - w,
                    0,
                    w,
                    rect.height()
                )
        return super().eventFilter(obj, event)

    def _show_sidebar(self):
        if hasattr(self, 'sidebar_outerWidget') and hasattr(self, 'overlay_container'):
            # Interrompe animazioni in corso per evitare casini
            if hasattr(self, '_sidebar_anim_out') and self._sidebar_anim_out.state() == QPropertyAnimation.Running:
                self._sidebar_anim_out.stop()

            self.sidebar_outerWidget.raise_()
            if not self.sidebar_outerWidget.isVisible():
                self.sidebar_outerWidget.show()
                rect = self.overlay_container.rect()
                w = 460
                
                start_geom = QRect(rect.width() + 20, 0, w, rect.height())
                end_geom = QRect(rect.width() - w, 0, w, rect.height())
                
                self.sidebar_outerWidget.setGeometry(start_geom)
                
                self._sidebar_anim_in = QPropertyAnimation(self.sidebar_outerWidget, b"geometry")
                self._sidebar_anim_in.setDuration(350)
                self._sidebar_anim_in.setStartValue(start_geom)
                self._sidebar_anim_in.setEndValue(end_geom)
                self._sidebar_anim_in.setEasingCurve(QEasingCurve.OutQuad)
                self._sidebar_anim_in.start()

    def _hide_sidebar(self, force=False):
        if hasattr(self, 'sidebar_outerWidget') and hasattr(self, 'overlay_container'):
            if hasattr(self, '_sidebar_anim_in') and self._sidebar_anim_in.state() == QPropertyAnimation.Running:
                self._sidebar_anim_in.stop()

            if self.sidebar_outerWidget.isVisible():
                rect = self.overlay_container.rect()
                w = 460
                
                start_geom = self.sidebar_outerWidget.geometry()
                end_geom = QRect(rect.width() + 20, 0, w, rect.height())
                
                self._sidebar_anim_out = QPropertyAnimation(self.sidebar_outerWidget, b"geometry")
                self._sidebar_anim_out.setDuration(280)
                self._sidebar_anim_out.setStartValue(start_geom)
                self._sidebar_anim_out.setEndValue(end_geom)
                self._sidebar_anim_out.setEasingCurve(QEasingCurve.InQuad)
                self._sidebar_anim_out.finished.connect(self.sidebar_outerWidget.hide)
                self._sidebar_anim_out.start()

    # ── Toolbar ───────────────────────────────────────────────────────────────
    def _build_toolbar(self):
        bar = QHBoxLayout()
        bar.setSpacing(6)

        self.btn_add = QPushButton("＋  Aggiungi Immagini")
        self.btn_add.setObjectName("PrimaryBtn")
        self.btn_add.setMinimumHeight(32)
        self.btn_add.setToolTip("Aggiungi uno o più file immagine al catalogo")
        self.btn_add.clicked.connect(self.add_images_dialog)
        bar.addWidget(self.btn_add)

        self.btn_add_folder = QPushButton("📁  Aggiungi Cartella")
        self.btn_add_folder.setMinimumHeight(32)
        self.btn_add_folder.setToolTip("Importa automaticamente tutti i file da una cartella")
        self.btn_add_folder.clicked.connect(self.add_folder_dialog)
        bar.addWidget(self.btn_add_folder)

        self.btn_stats = QPushButton("📊  Statistiche")
        self.btn_stats.setMinimumHeight(32)
        self.btn_stats.setToolTip("Visualizza statistiche del catalogo")
        self.btn_stats.clicked.connect(self._show_stats)
        bar.addWidget(self.btn_stats)

        self.btn_export = QPushButton("⬇  Esporta CSV")
        self.btn_export.setMinimumHeight(32)
        self.btn_export.setToolTip("Esporta l'intero catalogo in un file CSV")
        self.btn_export.clicked.connect(self.export_csv)
        bar.addWidget(self.btn_export)

        bar.addStretch()

        # Ricerca live
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet(f"color:{SUBTLE_TEXT}; font-size:11pt;")
        bar.addWidget(search_icon)
        self.le_search = QLineEdit()
        self.le_search.setPlaceholderText("Cerca Titolo, Costellazione, Tipo, Strumentazione, Tag…")
        self.le_search.setMinimumWidth(330)
        self.le_search.setMinimumHeight(32)
        self.le_search.setClearButtonEnabled(True)
        self.le_search.textChanged.connect(self._on_search_changed)
        bar.addWidget(self.le_search)

        # Filtri
        bar.addWidget(QLabel("Tipo:"))
        self.filter_type = QComboBox()
        self.filter_type.setMinimumWidth(140)
        # Il contenuto sarà popolato in load_data() per riflettere i tipi reali nel DB
        self.filter_type.setMinimumHeight(32)
        self.filter_type.currentTextChanged.connect(self.apply_filters)
        bar.addWidget(self.filter_type)

        bar.addWidget(QLabel("Focale:"))
        self.filter_focal = QComboBox()
        self.filter_focal.addItems([
            "Tutte le Focali",
            "Wide Field (< 200mm)",
            "Deep Sky (200–1000mm)",
            "Ultra Deep Sky (> 1000mm)"
        ])
        self.filter_focal.setMinimumHeight(32)
        self.filter_focal.currentTextChanged.connect(self.apply_filters)
        bar.addWidget(self.filter_focal)

        return bar

    # ── Table panel ───────────────────────────────────────────────────────────
    def _build_table_panel(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)

        self.lbl_count = QLabel("0 immagini")
        self.lbl_count.setStyleSheet(f"color:{SUBTLE_TEXT}; font-size:9pt; padding:2px 4px;")
        l.addWidget(self.lbl_count)

        self.image_table = QTableWidget()
        self.image_table.setColumnCount(10)
        self.image_table.setHorizontalHeaderLabels([
            "Anteprima", "Titolo", "Descrizione", "Tipo", "Costellazione",
            "AR", "Dec", "Tempo Int.", "Strumentazione", "Rating"
        ])
        self.image_table.verticalHeader().setVisible(False)
        self.image_table.setWordWrap(True)
        self.image_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.image_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.image_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.image_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.image_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.image_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.image_table.setIconSize(QSize(68, 68))
        self.image_table.verticalHeader().setDefaultSectionSize(78)
        self.image_table.setSortingEnabled(True)
        self.image_table.setAlternatingRowColors(True)
        self.image_table.setShowGrid(True)
        # Larghezze predefinite: restringiamo Titolo e allarghiamo flessibilmente il resto
        for col, w_ in [(0, 82), (1, 140), (3, 110), (4, 110), (5, 90),
                        (6, 90), (7, 100), (8, 140), (9, 80)]:
            self.image_table.setColumnWidth(col, w_)
        self.image_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.image_table.setFocusPolicy(Qt.NoFocus)
        l.addWidget(self.image_table)
        return w

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        outer = QFrame()
        outer.setObjectName("Sidebar")
        outer.setMinimumWidth(430)
        outer.setMaximumWidth(580)
        self.sidebar_outerWidget = outer

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(0, 0, 0, 0)
        ol.setSpacing(0)

        # Scroll area
        self.sidebar_scroll = QScrollArea()
        self.sidebar_scroll.setWidgetResizable(True)
        self.sidebar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sidebar_scroll.setFrameShape(QFrame.NoFrame)
        self.sidebar_scroll.setStyleSheet("background-color: transparent;")

        inner = QWidget()
        inner.setStyleSheet(f"background-color: {PANEL_BG};")
        il = QVBoxLayout(inner)
        il.setContentsMargins(14, 14, 14, 10)
        il.setSpacing(7)
        self._sidebar_layout = il

        # ── Anteprima ─────────────────────────────────────────────────────────
        self.lbl_preview = QLabel()
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setMinimumHeight(170)
        self.lbl_preview.setStyleSheet(
            f"background-color:#000015; border-radius:6px; border:1px solid {BORDER_COLOR};"
        )
        self.lbl_preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        il.addWidget(self.lbl_preview)

        # Pulsante apri immagine (solo viewer di sistema)
        self.btn_open_sys = QPushButton("🖼  Apri con programma di sistema")
        self.btn_open_sys.setMinimumHeight(30)
        self.btn_open_sys.setToolTip("Apri con il programma predefinito del sistema operativo")
        self.btn_open_sys.clicked.connect(self._open_image_os)
        il.addWidget(self.btn_open_sys)

        # ── Titolo ────────────────────────────────────────────────────────────
        self.le_title = QLineEdit()
        self.le_title.setPlaceholderText("Titolo (es. Nebulosa di Orione – M42)")
        self.le_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.le_title.setAlignment(Qt.AlignCenter)
        self.le_title.setMinimumHeight(36)
        self.le_title.setStyleSheet(
            "background-color: transparent; border: 1px dashed #404080;"
            "border-radius: 4px; padding: 4px; color: #fff; font-size: 12pt;"
        )
        il.addWidget(self.le_title)

        self.lbl_original_file = QLabel("")
        self.lbl_original_file.setStyleSheet(f"color:{SUBTLE_TEXT}; font-size:8.5pt;")
        self.lbl_original_file.setAlignment(Qt.AlignCenter)
        il.addWidget(self.lbl_original_file)

        # ── Rating ────────────────────────────────────────────────────────────
        rat_row = QHBoxLayout()
        rat_lbl = QLabel("Valutazione:")
        rat_lbl.setStyleSheet(f"color:{SUBTLE_TEXT};")
        self.star_rating = StarRatingWidget()
        rat_row.addWidget(rat_lbl)
        rat_row.addWidget(self.star_rating)
        rat_row.addStretch()
        il.addLayout(rat_row)

        il.addWidget(_hsep())

        # ── CLASSIFICAZIONE ───────────────────────────────────────────────────
        il.addWidget(_section_label("CLASSIFICAZIONE"))

        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Tipo:"))
        self.cb_type = QComboBox()
        self.cb_type.addItems(OBJECT_TYPES)
        r1.addWidget(self.cb_type, 1)
        r1.addSpacing(8)
        r1.addWidget(QLabel("Focale (mm):"))
        self.le_focal = QLineEdit()
        self.le_focal.setPlaceholderText("es. 750")
        self.le_focal.setFixedWidth(72)
        self.le_focal.setValidator(QDoubleValidator(0, 99999, 1, self))
        self.le_focal.setToolTip("Lunghezza focale in millimetri")
        self.le_focal.textChanged.connect(self._auto_focal_cat)
        r1.addWidget(self.le_focal)
        il.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Categoria focale:"))
        self.cb_focal_cat = QComboBox()
        self.cb_focal_cat.addItems(["Wide Field", "Deep Sky", "Ultra Deep Sky", "Unknown"])
        r2.addWidget(self.cb_focal_cat, 1)
        il.addLayout(r2)

        tags_row = QHBoxLayout()
        tags_row.addWidget(QLabel("Tag:"))
        self.le_tags = QLineEdit()
        self.le_tags.setPlaceholderText("es. narrowband, Ha, LRGB, HOO, mosaic")
        self.le_tags.setToolTip("Separa i tag con virgole")
        tags_row.addWidget(self.le_tags, 1)
        il.addLayout(tags_row)

        il.addWidget(_hsep())

        # ── DATI ASTRONOMICI ──────────────────────────────────────────────────
        il.addWidget(_section_label("DATI ASTRONOMICI"))

        ra_row = QHBoxLayout()
        ra_row.addWidget(QLabel("AR:"))
        self.le_ra = QLineEdit()
        self.le_ra.setPlaceholderText("05h 35m 17s  oppure  83.81")
        self.le_ra.setToolTip("Ascensione Retta — sessagesimale o gradi decimali")
        ra_row.addWidget(self.le_ra, 1)
        il.addLayout(ra_row)
        
        dec_row = QHBoxLayout()
        dec_row.addWidget(QLabel("Dec:"))
        self.le_dec = QLineEdit()
        self.le_dec.setPlaceholderText("-05° 23′ 28″  oppure  -5.39")
        self.le_dec.setToolTip("Declinazione — sessagesimale o gradi decimali")
        dec_row.addWidget(self.le_dec, 1)
        il.addLayout(dec_row)

        map_ctrl = QVBoxLayout()
        self.btn_wiki = QPushButton("🌐  Mappa IAU (Costellazione)")
        self.btn_wiki.setObjectName("SuccessBtn")
        self.btn_wiki.setMinimumHeight(28)
        self.btn_wiki.setToolTip("Scarica la mappa della costellazione da Wikipedia")
        self.btn_wiki.clicked.connect(self._on_map_wiki_btn)
        
        btn_dss_row = QHBoxLayout()
        self.btn_update_dss2 = QPushButton("🌌  Foto DSS2 (AR/Dec)")
        self.btn_update_dss2.setMinimumHeight(28)
        self.btn_update_dss2.setToolTip("Scarica la mappa fotografica DSS2 per le coordinate")
        self.btn_update_dss2.clicked.connect(self._on_map_dss2_btn)
        
        self.le_fov = QLineEdit("3.0")
        self.le_fov.setFixedWidth(42)
        self.le_fov.setValidator(QDoubleValidator(0.1, 90.0, 2, self))
        self.le_fov.setToolTip("FOV°")
        
        btn_dss_row.addWidget(self.btn_update_dss2)
        btn_dss_row.addWidget(QLabel("FOV°:"))
        btn_dss_row.addWidget(self.le_fov)
        
        map_ctrl.addWidget(self.btn_wiki)
        map_ctrl.addLayout(btn_dss_row)
        il.addLayout(map_ctrl)

        # Mappa stellare IAU (Wikipedia)
        wiki_lbl = QLabel("⭐ Mappa Costellazione (IAU)")
        wiki_lbl.setStyleSheet(f"color:{ACCENT2_COLOR}; font-weight:bold; font-size:8.5pt; padding:2px 0;")
        il.addWidget(wiki_lbl)
        self.lbl_map_wiki = QLabel()
        self.lbl_map_wiki.setAlignment(Qt.AlignCenter)
        self.lbl_map_wiki.setMinimumHeight(200)
        self.lbl_map_wiki.setStyleSheet(
            f"background-color:#000015; border:1px solid {BORDER_COLOR};"
            f"border-radius:6px; color:{SUBTLE_TEXT}; padding:8px;"
        )
        self.lbl_map_wiki.setText("Premi ‘🌐 Mappa IAU’ per caricare")
        self.lbl_map_wiki.setWordWrap(True)
        il.addWidget(self.lbl_map_wiki)

        # Mappa stellare DSS2
        dss_lbl = QLabel("🔭 Foto Cielo Profondo (DSS2)")
        dss_lbl.setStyleSheet(f"color:{ACCENT2_COLOR}; font-weight:bold; font-size:8.5pt; padding:2px 0;")
        il.addWidget(dss_lbl)
        self.lbl_map_dss2 = QLabel()
        self.lbl_map_dss2.setAlignment(Qt.AlignCenter)
        self.lbl_map_dss2.setMinimumHeight(200)
        self.lbl_map_dss2.setStyleSheet(
            f"background-color:#000015; border:1px solid {BORDER_COLOR};"
            f"border-radius:6px; color:{SUBTLE_TEXT}; padding:8px;"
        )
        self.lbl_map_dss2.setText("Premi ‘🌌 Foto DSS2’ per caricare")
        self.lbl_map_dss2.setWordWrap(True)
        il.addWidget(self.lbl_map_dss2)

        # Costellazione
        const_row = QHBoxLayout()
        const_row.addWidget(QLabel("Costellazione:"))
        self.cb_constellation = QComboBox()
        self.cb_constellation.setEditable(True)
        self.cb_constellation.addItems(CONSTELLATIONS)
        self.cb_constellation.setInsertPolicy(QComboBox.NoInsert)
        self.cb_constellation.lineEdit().setPlaceholderText("Cerca o scrivi costellazione…")
        const_row.addWidget(self.cb_constellation, 1)
        il.addLayout(const_row)

        il.addWidget(_hsep())

        # ── DATI DI ACQUISIZIONE ──────────────────────────────────────────────
        il.addWidget(_section_label("DATI DI ACQUISIZIONE"))

        il.addWidget(QLabel("Strumentazione (Telescopio + Camera):"))
        self.le_equipment = QLineEdit()
        self.le_equipment.setPlaceholderText("es. TS 72/432 + ZWO ASI294MC Pro")
        il.addWidget(self.le_equipment)

        acq = QHBoxLayout()
        acq.addWidget(QLabel("Tempo integrazione:"))
        self.le_integration = QLineEdit()
        self.le_integration.setPlaceholderText("es. 4h 30m")
        acq.addWidget(self.le_integration, 1)
        acq.addSpacing(6)
        acq.addWidget(QLabel("Data:"))
        self.de_date = QDateEdit()
        self.de_date.setDisplayFormat("dd/MM/yyyy")
        self.de_date.setCalendarPopup(True)
        self.de_date.setDate(QDate.currentDate())
        self.de_date.setFixedWidth(115)
        self.de_date.setToolTip("Data di acquisizione (apre il calendario)")
        acq.addWidget(self.de_date)
        il.addLayout(acq)

        il.addWidget(QLabel("Luogo di osservazione:"))
        self.le_location = QLineEdit()
        self.le_location.setPlaceholderText("es. Pescara, cielo Bortle 5")
        il.addWidget(self.le_location)

        il.addWidget(QLabel("Note / Descrizione:"))
        self.te_desc = QTextEdit()
        self.te_desc.setPlaceholderText(
            "Aggiungi note: condizioni meteo, filtri usati, software di elaborazione…"
        )
        self.te_desc.setMinimumHeight(68)
        self.te_desc.setMaximumHeight(130)
        il.addWidget(self.te_desc)

        il.addStretch(1)

        self.sidebar_scroll.setWidget(inner)
        ol.addWidget(self.sidebar_scroll)
        ol.addWidget(self._build_sidebar_buttons())

        self.sidebar_outerWidget.hide()
        return outer

    def _build_sidebar_buttons(self):
        w = QWidget()
        w.setStyleSheet(f"background-color:{PANEL_BG}; border-top:1px solid {BORDER_COLOR};")
        l = QHBoxLayout(w)
        l.setContentsMargins(12, 10, 12, 10)
        l.setSpacing(8)

        self.btn_save = QPushButton("💾  Salva")
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setMinimumHeight(34)
        self.btn_save.setToolTip("Salva i metadati per la selezione corrente  (Ctrl+S)")
        self.btn_save.clicked.connect(self.save_image_details)

        self.btn_explorer = QPushButton("📂  Explorer")
        self.btn_explorer.setMinimumHeight(34)
        self.btn_explorer.setToolTip("Mostra il file nella cartella in Esplora Risorse")
        self.btn_explorer.clicked.connect(self.show_in_explorer)

        self.btn_copy_coords = QPushButton("📋  Coords")
        self.btn_copy_coords.setMinimumHeight(34)
        self.btn_copy_coords.setToolTip("Copia AR e Dec negli appunti")
        self.btn_copy_coords.clicked.connect(self._copy_coords)

        self.btn_delete = QPushButton("🗑  Rimuovi")
        self.btn_delete.setObjectName("DangerBtn")
        self.btn_delete.setMinimumHeight(34)
        self.btn_delete.setToolTip("Rimuove le immagini dal catalogo (il file su disco non viene eliminato)")
        self.btn_delete.clicked.connect(self.delete_current_image)

        l.addWidget(self.btn_save, 2)
        l.addWidget(self.btn_explorer, 2)
        l.addWidget(self.btn_copy_coords, 1)
        l.addWidget(self.btn_delete, 1)
        return w

    # ── Resize event ─────────────────────────────────────────────────────────
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.current_image_id and self.sidebar_outerWidget.isVisible():
            self._update_preview()

    # ─────────────────────────────────────────────────────────────────────────
    # DATA LOADING
    # ─────────────────────────────────────────────────────────────────────────
    def load_images_from_db(self):
        self._is_loading = True
        self.all_images = database.get_all_images()
        print(f"DEBUG: Caricate {len(self.all_images)} immagini dal database.")

        # Popola i tipi PRIMA di applicare i filtri, altrimenti il ComboBox vuoto
        # filtra via tutte le immagini al primo avvio
        current_filter_type = self.filter_type.currentText()
        unique_types = set(img.get("type", "") for img in self.all_images if img.get("type", "").strip())
        type_list = ["Tutti i Tipi"] + sorted(list(unique_types))
        
        self.filter_type.blockSignals(True)
        self.filter_type.clear()
        self.filter_type.addItems(type_list)
        if current_filter_type in type_list:
            self.filter_type.setCurrentText(current_filter_type)
        else:
            self.filter_type.setCurrentIndex(0)
        self.apply_filters()
        self._is_loading = False

    def _on_search_changed(self, text):
        if len(text) > 1:
            self.all_images = database.search_images(text)
        else:
            self.all_images = database.get_all_images()
        self.apply_filters()

    def apply_filters(self):
        type_f  = self.filter_type.currentText()
        focal_f = self.filter_focal.currentText()

        self.image_table.setSortingEnabled(False)
        self.image_table.setRowCount(0)

        row_idx = 0
        for img in self.all_images:
            if type_f != "Tutti i Tipi" and img.get("type") != type_f:
                continue
            if focal_f != "Tutte le Focali":
                fc = img.get("focal_category", "")
                if "Wide Field" in focal_f and fc != "Wide Field":
                    continue
                if "Deep Sky" in focal_f and "Ultra" not in focal_f and fc != "Deep Sky":
                    continue
                if "Ultra Deep Sky" in focal_f and fc != "Ultra Deep Sky":
                    continue
            if not os.path.exists(img.get("path", "")):
                continue

            self.image_table.insertRow(row_idx)

            # Col 0 – thumbnail
            thumb = QTableWidgetItem()
            px = QPixmap(img["path"])
            if not px.isNull():
                thumb.setIcon(QIcon(px.scaled(66, 66, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            thumb.setData(Qt.UserRole, img)
            self.image_table.setItem(row_idx, 0, thumb)

            display = img.get("title") or img.get("filename", "")
            self.image_table.setItem(row_idx, 1, QTableWidgetItem(display))
            desc_text = img.get("description", "").replace("\n", " ")[:60]
            if len(img.get("description", "")) > 60: desc_text += "..."
            self.image_table.setItem(row_idx, 2, QTableWidgetItem(desc_text))
            self.image_table.setItem(row_idx, 3, QTableWidgetItem(img.get("type", "")))
            self.image_table.setItem(row_idx, 4, QTableWidgetItem(img.get("constellation", "")))
            self.image_table.setItem(row_idx, 5, QTableWidgetItem(img.get("ra", "")))
            self.image_table.setItem(row_idx, 6, QTableWidgetItem(img.get("dec", "")))
            self.image_table.setItem(row_idx, 7, QTableWidgetItem(img.get("integration_time", "")))
            self.image_table.setItem(row_idx, 8, QTableWidgetItem(img.get("equipment", "")))

            stars = "★" * img.get("rating", 0) + "☆" * (5 - img.get("rating", 0))
            r_item = QTableWidgetItem(stars)
            r_item.setForeground(QColor(STAR_COLOR))
            r_item.setTextAlignment(Qt.AlignCenter)
            self.image_table.setItem(row_idx, 9, r_item)

            row_idx += 1

        self.image_table.setSortingEnabled(True)
        n = self.image_table.rowCount()
        self.lbl_count.setText(f"{n} immagine{'i' if n != 1 else ''}")
        self.set_status(f"{n} immagini visualizzate")

    # ─────────────────────────────────────────────────────────────────────────
    # SELECTION
    # ─────────────────────────────────────────────────────────────────────────
    def on_selection_changed(self):
        # Controlla se siamo già in fase di aggiornamento o caricamento
        if getattr(self, '_ignore_selection_change', False) or self._is_loading:
            return
            
        # Protezione contro la ricorsione durante la visualizzazione di dialoghi modali
        self._ignore_selection_change = True
        try:
            rows = set(i.row() for i in self.image_table.selectedItems())
            if not rows:
                if self.sidebar_outerWidget.isVisible():
                    # Check modifiche prima di chiudere la barra per de-selezione
                    if self._check_unsaved_changes():
                        # L'utente vuole restare: re-seleziona
                        self._reselect_previous_rows()
                        return
                    self._hide_sidebar()
                self.current_image_id   = None
                self.current_image_path = None
                return

            # Se navighiamo via con una selezione attiva
            if self.current_image_id is not None and self.sidebar_outerWidget.isVisible():
                if self._check_unsaved_changes():
                    # L'utente vuole restare: re-seleziona la riga precedente
                    self._reselect_previous_rows()
                    return

            # Navigazione confermata o nessun'immagine precedente: carica la nuova selezione
            self._previous_selected_rows = list(rows)
            
            if not self.sidebar_outerWidget.isVisible():
                self._show_sidebar()

            if len(rows) == 1:
                row = list(rows)[0]
                item = self.image_table.item(row, 0)
                img  = item.data(Qt.UserRole)
                self._populate_sidebar(img)
                self.current_image_id   = img["id"]
                self.current_image_path = img.get("path", "")
            else:
                self._populate_sidebar_multi(len(rows))
                self.current_image_id   = None
                self.current_image_path = None

            count_text = self.lbl_count.text().split(" | ")[0]
            if self.current_image_path:
                self.lbl_count.setText(
                    f"{count_text}   |   Selezionato: {os.path.basename(self.current_image_path)}"
                )
            else:
                self.lbl_count.setText(f"{count_text}   |   {len(rows)} file selezionati")
        finally:
            self._ignore_selection_change = False

    def _reselect_previous_rows(self):
        prev_rows = getattr(self, '_previous_selected_rows', [])
        self.image_table.clearSelection()
        for r in prev_rows:
            self.image_table.selectRow(r)

    def _check_unsaved_changes(self):
        """Valuta se il pannello laterale ha modifiche pendenti rispetto al DB."""
        if self._is_loading:
            return False
            
        if not self.sidebar_outerWidget.isVisible() or not self.current_image_id:
            return False
            
        # Modalità edit multiplo non ancora gestita come unsaved form
        if len(self.image_table.selectedItems()) > self.image_table.columnCount():
            return False

        try:
            # Cerchiamo l'oggetto originale aggiornato caricato dal DB (all_images)
            original_img = next((img for img in self.all_images if img["id"] == self.current_image_id), None)
            if not original_img:
                return False

            # --- NORMALIZZAZIONE PER CONFRONTO ---
            
            # 1. Titolo
            current_title = self.le_title.text().strip()
            orig_title = (original_img.get("title") or original_img.get("filename") or "").strip()

            # 2. Focale (numericamente)
            try:
                curr_foc = float(self.le_focal.text().strip() or 0)
                orig_foc = float(original_img.get("focal_length") or 0)
            except ValueError:
                curr_foc = self.le_focal.text().strip()
                orig_foc = str(original_img.get("focal_length") or "")

            # 3. Data
            curr_date = self.de_date.date().toString("dd/MM/yyyy")
            orig_date = original_img.get("date_acquired") or ""
            # Se originale è vuoto, il widget mostra oggi per default. Consideriamo non modificato.
            if not orig_date and self.de_date.date() == QDate.currentDate():
                curr_date = ""
                orig_date = ""

            # 4. Altri campi testo
            def s(val): return (str(val) if val is not None else "").strip()

            is_dirty = (
                current_title != orig_title or
                s(self.cb_type.currentText()) != s(original_img.get("type", "Altro")) or
                s(self.cb_constellation.currentText()) != s(original_img.get("constellation")) or
                s(self.le_ra.text()) != s(original_img.get("ra")) or
                s(self.le_dec.text()) != s(original_img.get("dec")) or
                curr_foc != orig_foc or
                s(self.cb_focal_cat.currentText()) != s(original_img.get("focal_category", "Unknown")) or
                s(self.le_equipment.text()) != s(original_img.get("equipment")) or
                s(self.le_integration.text()) != s(original_img.get("integration_time")) or
                s(self.le_location.text()) != s(original_img.get("location")) or
                curr_date != orig_date or
                self.te_desc.toPlainText().strip() != s(original_img.get("description")) or
                s(self.le_tags.text()) != s(original_img.get("tags")) or
                self.star_rating.rating != (original_img.get("rating") or 0)
            )

            if is_dirty:
                reply = self.show_message(
                    "Modifiche non salvate",
                    "Hai delle modifiche non salvate nel pannello laterale.\n\n"
                    "Vuoi perdere le modifiche?",
                    QMessageBox.Question,
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return True
        except Exception as e:
            print(f"DEBUG: Errore in dirty check: {e}")
            return False

        return False

    def _populate_sidebar(self, img):
        self._is_loading = True
        self.current_image_id   = img["id"]
        self.current_image_path = img["path"]

        self.le_title.setText(img.get("title") or img.get("filename", ""))
        self.le_title.setEnabled(True)
        self.lbl_original_file.setText(img.get("filename", ""))

        self._update_preview()

        self.cb_type.setCurrentText(img.get("type") or "Altro")
        focal = img.get("focal_length")
        self.le_focal.setText(str(focal) if focal else "")
        self.cb_focal_cat.setCurrentText(img.get("focal_category") or "Unknown")
        self.le_tags.setText(img.get("tags", ""))
        self.star_rating.rating = img.get("rating", 0)

        self.le_ra.setText(img.get("ra", ""))
        self.le_dec.setText(img.get("dec", ""))
        self.cb_constellation.setCurrentText(img.get("constellation", ""))

        ra_v  = img.get("ra", "")
        dec_v = img.get("dec", "")
        c_v = img.get("constellation", "")
        if c_v:
            self._start_map_wiki(c_v)
        if ra_v and dec_v:
            self._start_map_dss2(ra_v, dec_v)
        if not c_v:
            self.lbl_map_wiki.clear()
            self.lbl_map_wiki.setText("Premi '🌐 Mappa IAU' per caricare")
        if not (ra_v and dec_v):
            self.lbl_map_dss2.clear()
            self.lbl_map_dss2.setText("Premi '🌌 Foto DSS2' per caricare")

        self.le_equipment.setText(img.get("equipment", ""))
        self.le_integration.setText(img.get("integration_time", ""))

        date_s = img.get("date_acquired", "")
        d = QDate.fromString(date_s, "dd/MM/yyyy") if date_s else QDate()
        self.de_date.setDate(d if d.isValid() else QDate.currentDate())

        self.le_location.setText(img.get("location", ""))
        self.te_desc.setPlainText(img.get("description", ""))

        # Abilita pulsanti
        for b in (self.btn_save, self.btn_delete, self.btn_explorer,
                  self.btn_open_sys, self.btn_wiki, self.btn_update_dss2):
            b.setEnabled(True)
        self.btn_copy_coords.setEnabled(bool(ra_v))
        self._is_loading = False

    def _populate_sidebar_multi(self, count):
        self._is_loading = True
        self.current_image_id   = None
        self.current_image_path = None

        self.le_title.setText(f"Modifica multipla — {count} immagini")
        self.le_title.setEnabled(False)
        self.lbl_original_file.setText("")
        self.lbl_preview.clear()
        self.lbl_preview.setText(f"Modifica massiva\n{count} immagini selezionate")
        self.lbl_map_wiki.clear()
        self.lbl_map_wiki.setText("Non disponibile\nin selezione multipla")
        self.lbl_map_dss2.clear()
        self.lbl_map_dss2.setText("Non disponibile\nin selezione multipla")

        for w in (self.le_ra, self.le_dec, self.le_focal, self.le_tags,
                  self.le_equipment, self.le_integration, self.le_location):
            w.clear()
        self.te_desc.clear()
        self.cb_constellation.setCurrentText("")
        self.star_rating.rating = 0

        for b in (self.btn_copy_coords, self.btn_wiki, self.btn_update_dss2,
                  self.btn_open_sys, self.btn_explorer):
            b.setEnabled(False)
        self.btn_save.setEnabled(True)
        self.btn_delete.setEnabled(True)
        self._is_loading = False

    # ── Preview ───────────────────────────────────────────────────────────────
    def _update_preview(self):
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            self.lbl_preview.clear()
            self.lbl_preview.setText("Anteprima non disponibile\n(file non trovato)")
            return
        px = QPixmap(self.current_image_path)
        if px.isNull():
            self.lbl_preview.clear()
            self.lbl_preview.setText("Impossibile caricare l'anteprima")
            return
        vp_w = self.sidebar_scroll.viewport().width() - 28
        if vp_w < 50:
            vp_w = 300
        scaled = px.scaledToWidth(vp_w, Qt.SmoothTransformation)
        if scaled.height() > 330:
            scaled = px.scaledToHeight(330, Qt.SmoothTransformation)
        self.lbl_preview.setPixmap(scaled)

    # ── Sky Map ───────────────────────────────────────────────────────────────
    def _on_map_wiki_btn(self):
        c_v = self.cb_constellation.currentText().strip()
        self._start_map_wiki(c_v)

    def _start_map_wiki(self, constellation):
        if not constellation:
            self.lbl_map_wiki.setText("Seleziona una costellazione per caricare la mappa.")
            return

        self.lbl_map_wiki.clear()
        self.lbl_map_wiki.setText(
            f"  Download mappa Wikipedia in corso…\n"
            f"  Costellazione: {constellation}"
        )
        self._set_map_btns_enabled(False)
        
        # Ferma eventuale fetch precedente
        if self._map_fetcher and self._map_fetcher.isRunning():
            try:
                self._map_fetcher.finished.disconnect()
                self._map_fetcher.error.disconnect()
            except Exception:
                pass
            self._map_fetcher.terminate()
            self._map_fetcher.wait(500)

        self._map_fetcher = SkyMapFetcher(constellation)
        self._map_fetcher.finished.connect(self._on_map_ready_wiki)
        self._map_fetcher.error.connect(self._on_map_error_wiki)
        self._map_fetcher.finished.connect(lambda _: self._restore_map_btns())
        self._map_fetcher.error.connect(lambda _: self._restore_map_btns())
        self._map_fetcher.start()

    def _on_map_dss2_btn(self):
        self._set_map_btns_enabled(False)
        self._start_map_dss2(self.le_ra.text(), self.le_dec.text())

    def _start_map_dss2(self, ra_str, dec_str):
        if not ra_str.strip() or not dec_str.strip():
            self.lbl_map_dss2.setText("Inserisci AR e Dec per caricare la mappa DSS2.")
            return

        ra_d, dec_d = _parse_coordinates(ra_str, dec_str)
        if ra_d is None:
            self.lbl_map_dss2.setText(
                "Formato coordinate non riconosciuto.\n"
                "Esempi validi:\n"
                "  AR:  05h 35m 17s   oppure  83.82\n"
                "  Dec: -05° 23′ 28″  oppure  -5.39"
            )
            return

        try:
            fov = float(self.le_fov.text().replace(",", "."))
            fov = max(0.1, min(90.0, fov))
        except (ValueError, AttributeError):
            fov = 3.0

        self.lbl_map_dss2.clear()
        self.lbl_map_dss2.setText(
            f"  Download mappa DSS2 in corso…\n"
            f"  RA: {ra_d:.4f}°   Dec: {dec_d:.4f}°   FOV: {fov}°"
        )

        if self._map_fetcher and self._map_fetcher.isRunning():
            try:
                self._map_fetcher.finished.disconnect()
                self._map_fetcher.error.disconnect()
            except Exception:
                pass
            self._map_fetcher.terminate()
            self._map_fetcher.wait(500)

        self._map_fetcher = SkyMapFetcherDSS2(ra_d, dec_d, fov)
        self._map_fetcher.finished.connect(self._on_map_ready_dss2)
        self._map_fetcher.error.connect(self._on_map_error_dss2)
        self._map_fetcher.finished.connect(lambda _: self._restore_map_btns())
        self._map_fetcher.error.connect(lambda _: self._restore_map_btns())
        self._map_fetcher.start()

    def _set_map_btns_enabled(self, enabled):
        if hasattr(self, 'btn_wiki'):
            self.btn_wiki.setEnabled(enabled)
            self.btn_update_dss2.setEnabled(enabled)

    def _restore_map_btns(self):
        self._set_map_btns_enabled(True)

    def _on_map_ready_wiki(self, pixmap):
        self._display_map_pixmap(pixmap, self.lbl_map_wiki)

    def _on_map_ready_dss2(self, pixmap):
        self._display_map_pixmap(pixmap, self.lbl_map_dss2)

    def _display_map_pixmap(self, pixmap, target_label):
        if pixmap.isNull():
            target_label.setText("Mappa ricevuta non valida.")
            return
        vp_w = self.sidebar_scroll.viewport().width() - 28
        if vp_w < 50:
            vp_w = 400
        scaled = pixmap.scaledToWidth(vp_w, Qt.SmoothTransformation)
        if scaled.height() > 450:
            scaled = pixmap.scaledToHeight(450, Qt.SmoothTransformation)
        target_label.setPixmap(scaled)

    def _on_map_error_wiki(self, err):
        self.lbl_map_wiki.setText(
            f"Errore nel download della mappa.\n"
            f"Verifica la connessione internet.\n\n{err[:80]}"
        )

    def _on_map_error_dss2(self, err):
        self.lbl_map_dss2.setText(
            f"Errore nel download della mappa DSS2.\n"
            f"Verifica la connessione internet.\n\n{err[:80]}"
        )

    # ── Auto focal cat ────────────────────────────────────────────────────────
    def _auto_focal_cat(self, text):
        try:
            mm = float(text)
        except ValueError:
            return
        if mm < 200:
            self.cb_focal_cat.setCurrentText("Wide Field")
        elif mm <= 1000:
            self.cb_focal_cat.setCurrentText("Deep Sky")
        else:
            self.cb_focal_cat.setCurrentText("Ultra Deep Sky")

    # ─────────────────────────────────────────────────────────────────────────
    # ACTIONS
    # ─────────────────────────────────────────────────────────────────────────
    def add_images_dialog(self):
        dlg = QFileDialog(self)
        dlg.setWindowTitle("Seleziona Immagini Astronomiche")
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilter(
            "Immagini (*.png *.jpg *.jpeg *.tif *.tiff *.fit *.fits *.xisf)"
        )
        _apply_dark_titlebar(dlg)
        if dlg.exec_():
            files = dlg.selectedFiles()
            added = sum(1 for f in files if database.add_image(f) is not None)
            self.load_images_from_db()
            self.set_status(f"{added} immagini aggiunte al catalogo.", 4000)

    def add_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Seleziona Cartella", "", QFileDialog.ShowDirsOnly
        )
        if not folder:
            return
        exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff",
                ".fit", ".fits", ".xisf"}
        count = 0
        for entry in os.scandir(folder):
            if entry.is_file() and os.path.splitext(entry.name)[1].lower() in exts:
                if database.add_image(entry.path) is not None:
                    count += 1
        self.load_images_from_db()
        self.set_status(f"{count} immagini importate dalla cartella.", 4000)
        if count:
            self.show_message(
                "Cartella importata",
                f"Aggiunte {count} immagini da:\n{folder}"
            )
        else:
            self.show_message(
                "Nessuna immagine trovata",
                f"Nessuna immagine compatibile trovata in:\n{folder}",
                QMessageBox.Warning
            )

    def save_image_details(self):
        rows = set(i.row() for i in self.image_table.selectedItems())
        if not rows:
            return

        is_multi = len(rows) > 1

        # Validazione focale
        focal_txt = self.le_focal.text().strip()
        try:
            focal = float(focal_txt) if focal_txt else 0.0
        except ValueError:
            self.show_message("Valore non valido",
                              "Il campo Focale deve contenere un numero (es. 750).",
                              QMessageBox.Warning)
            return

        # Validazione coordinate (solo se compilate entrambe)
        ra_v  = self.le_ra.text().strip()
        dec_v = self.le_dec.text().strip()
        if ra_v and dec_v:
            ra_d, dec_d = _parse_coordinates(ra_v, dec_v)
            if ra_d is None:
                self.show_message(
                    "Coordinate non valide",
                    "Il formato delle coordinate AR/Dec non è riconosciuto.\n\n"
                    "Esempi validi:\n"
                    "  AR:  05h 35m 17s   oppure  83.82\n"
                    "  Dec: -05° 23′ 28″  oppure  -5.39",
                    QMessageBox.Warning
                )
                return
        elif (ra_v and not dec_v) or (not ra_v and dec_v):
            self.show_message("Coordinate incomplete",
                              "Compila sia AR che Dec, oppure lascia entrambi vuoti.",
                              QMessageBox.Warning)
            return

        img_type    = self.cb_type.currentText()
        focal_cat   = self.cb_focal_cat.currentText()
        desc        = self.te_desc.toPlainText()
        constellation = self.cb_constellation.currentText().strip()
        equipment   = self.le_equipment.text().strip()
        integration = self.le_integration.text().strip()
        location    = self.le_location.text().strip()
        date_acq    = self.de_date.date().toString("dd/MM/yyyy")
        tags        = self.le_tags.text().strip()
        rating      = self.star_rating.rating

        saved_ids = []
        for row in rows:
            img   = self.image_table.item(row, 0).data(Qt.UserRole)
            title = (img.get("title", "") if is_multi
                     else self.le_title.text().strip())
            database.update_image(
                img["id"], title, img_type, focal, focal_cat, desc,
                ra_v, dec_v, constellation, equipment, integration, location,
                date_acq, tags, rating
            )
            saved_ids.append(img["id"])

        # Ricarica e blocca check per un attimo
        self._is_loading = True
        self.load_images_from_db()
        self._is_loading = False

        # Ripristina selezione
        for r in range(self.image_table.rowCount()):
            item = self.image_table.item(r, 0)
            if item and item.data(Qt.UserRole)["id"] in saved_ids:
                self.image_table.selectRow(r)

        self.set_status(f"Salvate {len(saved_ids)} immagine/i.", 3000)

    def delete_current_image(self):
        rows = set(i.row() for i in self.image_table.selectedItems())
        if not rows:
            return
        reply = self.show_message(
            "Conferma rimozione",
            f"Rimuovere {len(rows)} immagine/i dal catalogo?\n"
            "(Il file sul disco NON sarà eliminato.)",
            QMessageBox.Question, QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            for row in rows:
                img = self.image_table.item(row, 0).data(Qt.UserRole)
                database.delete_image(img["id"])
            self._hide_sidebar()
            self.current_image_id   = None
            self.current_image_path = None
            self.load_images_from_db()
            self.set_status(f"{len(rows)} immagine/i rimossa/e.", 3000)

    def show_in_explorer(self):
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            self.show_message("File non trovato",
                              "Il file originale non è accessibile.", QMessageBox.Warning)
            return
        if sys.platform == "win32":
            subprocess.Popen(
                f'explorer /select,"{os.path.normpath(self.current_image_path)}"'
            )
        else:
            import webbrowser
            webbrowser.open("file://" + os.path.dirname(self.current_image_path))

    def _open_fullscreen_if_path(self):
        if self.current_image_path and os.path.exists(self.current_image_path):
            dlg = ImageViewerDialog(self.current_image_path, self)
            dlg.exec_()

    def _open_fullscreen_viewer(self, index):
        row  = index.row()
        item = self.image_table.item(row, 0)
        if not item:
            return
        img = item.data(Qt.UserRole)
        if os.path.exists(img.get("path", "")):
            ImageViewerDialog(img["path"], self).exec_()

    def _open_image_os(self):
        if not self.current_image_path or not os.path.exists(self.current_image_path):
            return
        if sys.platform == "win32":
            os.startfile(os.path.normpath(self.current_image_path))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", self.current_image_path])
        else:
            subprocess.Popen(["xdg-open", self.current_image_path])

    def _copy_coords(self):
        ra  = self.le_ra.text().strip()
        dec = self.le_dec.text().strip()
        if ra or dec:
            QApplication.clipboard().setText(f"AR: {ra}   Dec: {dec}")
            self.set_status("Coordinate copiate negli appunti.", 2500)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Esporta catalogo CSV", "catalogo_astro.csv", "CSV (*.csv)"
        )
        if path:
            n = database.export_to_csv(path)
            self.show_message(
                "Esportazione completata",
                f"Esportate {n} immagini in:\n{path}"
            )

    def _show_stats(self):
        StatsDialog(self).exec_()

    # ── Keyboard shortcuts ────────────────────────────────────────────────────
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_S:
            self.save_image_details()
        else:
            super().keyPressEvent(e)
