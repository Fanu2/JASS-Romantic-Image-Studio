
import sys, csv, math
from pathlib import Path

from PySide6.QtCore import Qt, QSize, QPointF, Signal
from PySide6.QtGui import (
    QPixmap, QPainter, QFont, QColor, QPen, QBrush, QFontDatabase,
    QLinearGradient, QRadialGradient
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QFileDialog, QMessageBox,
    QLineEdit, QComboBox, QSlider, QCheckBox, QFrame, QSplitter, QGroupBox,
    QColorDialog, QSpinBox, QDialog, QDialogButtonBox, QTextEdit
)

APP_TITLE = "JASS Romantic Image Studio V5 — Literary Stanza Explorer"
DATASET = Path(__file__).with_name("romantic_stanzas_500.csv")
SEPARATION_DATASET = Path(__file__).with_name("love_separation_150.csv")
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

TEMPLATES = {
    "Romantic": {
        "overlay": True, "overlay_alpha": 125, "frame": "soft",
        "accent": "#f2abc6", "font": "Georgia", "position": (0.5, 0.80),
        "decoration": "hearts"
    },
    "Love Letter": {
        "overlay": True, "overlay_alpha": 145, "frame": "letter",
        "accent": "#f4d6bd", "font": "Baskerville", "position": (0.5, 0.72),
        "decoration": "corner"
    },
    "Vintage": {
        "overlay": True, "overlay_alpha": 105, "frame": "vintage",
        "accent": "#e7c99d", "font": "Palatino Linotype", "position": (0.5, 0.78),
        "decoration": "floral"
    },
    "Sunset": {
        "overlay": True, "overlay_alpha": 110, "frame": "none",
        "accent": "#ffd2a6", "font": "Georgia", "position": (0.5, 0.78),
        "decoration": "glow"
    },
    "Minimal": {
        "overlay": False, "overlay_alpha": 0, "frame": "none",
        "accent": "#ffffff", "font": "Segoe UI", "position": (0.5, 0.84),
        "decoration": "none"
    },
    "Dreamy": {
        "overlay": True, "overlay_alpha": 95, "frame": "soft",
        "accent": "#d9c5ff", "font": "Georgia", "position": (0.5, 0.50),
        "decoration": "sparkle"
    },
}

class Canvas(QWidget):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap()
        self.text = ""
        self.font_family = "Georgia"
        self.font_size = 42
        self.text_color = QColor("#fff5f8")
        self.accent = QColor("#f2abc6")
        self.shadow = True
        self.overlay = True
        self.overlay_opacity = 125
        self.position = QPointF(.5, .80)
        self.decoration = "hearts"
        self.frame = "soft"
        self.template = "Romantic"
        self.dragging = False
        self.last_pos = None
        self.setMinimumSize(500, 450)
        self.setMouseTracking(True)

    def image_rect(self):
        if self.pixmap.isNull():
            return None
        scale = min(self.width()/self.pixmap.width(), self.height()/self.pixmap.height())
        w, h = self.pixmap.width()*scale, self.pixmap.height()*scale
        return (self.width()-w)/2, (self.height()-h)/2, w, h, scale

    def set_image(self, path):
        self.pixmap = QPixmap(str(path))
        self.update()

    def set_text(self, text):
        self.text = text
        self.update()

    def set_template(self, name):
        self.template = name
        cfg = TEMPLATES[name]
        self.overlay = cfg["overlay"]
        self.overlay_opacity = cfg["overlay_alpha"]
        self.frame = cfg["frame"]
        self.accent = QColor(cfg["accent"])
        self.font_family = cfg["font"]
        self.position = QPointF(*cfg["position"])
        self.decoration = cfg["decoration"]
        self.update()

    def _draw_decorations(self, p, x, y, w, h):
        """
        Draw deliberately small, transparent decorative accents.
        Important: decorations must NEVER paint a full-canvas background.
        """
        c = QColor(self.accent)
        c.setAlpha(185)

        if self.decoration == "none":
            return

        if self.decoration == "hearts":
            # Use a glyph rather than a filled painter path. This avoids
            # accidental large-path fills covering the photograph.
            p.save()
            p.setPen(Qt.NoPen)
            p.setBrush(c)
            font = QFont("DejaVu Sans", max(12, int(min(w, h) * 0.035)))
            p.setFont(font)
            for px, py, scale in [
                (x + w * .07, y + h * .09, 1.0),
                (x + w * .91, y + h * .12, .78),
                (x + w * .90, y + h * .89, .68),
            ]:
                s = max(12, int(font.pointSize() * scale))
                f = QFont("DejaVu Sans", s)
                p.setFont(f)
                p.drawText(int(px - s/2), int(py + s/2), "♥")
            p.restore()

        elif self.decoration == "sparkle":
            p.save()
            p.setPen(QPen(c, 2))
            p.setBrush(Qt.NoBrush)
            for px, py, s in [
                (x + w*.08, y + h*.10, 8),
                (x + w*.90, y + h*.13, 6),
                (x + w*.90, y + h*.88, 7),
            ]:
                p.drawLine(int(px-s), int(py), int(px+s), int(py))
                p.drawLine(int(px), int(py-s), int(px), int(py+s))
                p.drawLine(int(px-s*.55), int(py-s*.55),
                           int(px+s*.55), int(py+s*.55))
                p.drawLine(int(px+s*.55), int(py-s*.55),
                           int(px-s*.55), int(py+s*.55))
            p.restore()

        elif self.decoration == "corner":
            p.save()
            p.setPen(QPen(c, 2))
            p.setBrush(Qt.NoBrush)
            length = min(w, h) * .07
            gap = min(w, h) * .035
            # Four tiny corner ornaments, with no fill.
            for sx, sy, dx, dy in [
                (x+gap, y+gap, 1, 1),
                (x+w-gap, y+gap, -1, 1),
                (x+gap, y+h-gap, 1, -1),
                (x+w-gap, y+h-gap, -1, -1),
            ]:
                p.drawLine(int(sx), int(sy), int(sx+dx*length), int(sy))
                p.drawLine(int(sx), int(sy), int(sx), int(sy+dy*length))
            p.restore()

        elif self.decoration == "floral":
            # Small outline-only flowers. No large brush/fill is used.
            p.save()
            p.setPen(QPen(c, 1.6))
            p.setBrush(Qt.NoBrush)
            r = max(4, min(w, h) * .012)
            for cx, cy in [
                (x+w*.075, y+h*.10),
                (x+w*.925, y+h*.10),
                (x+w*.075, y+h*.90),
                (x+w*.925, y+h*.90),
            ]:
                for ang in range(0, 360, 72):
                    import math
                    a = math.radians(ang)
                    px = cx + math.cos(a) * r * 1.45
                    py = cy + math.sin(a) * r * 1.45
                    p.drawEllipse(int(px-r*.72), int(py-r*.72),
                                  int(r*1.44), int(r*1.44))
                p.drawEllipse(int(cx-r*.42), int(cy-r*.42),
                              int(r*.84), int(r*.84))
            p.restore()

        elif self.decoration == "glow":
            # Keep glow subtle and localized; never use a full opaque fill.
            p.save()
            grad = QRadialGradient(x+w*.50, y+h*.50, max(w,h)*.48)
            grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 28))
            grad.setColorAt(0.65, QColor(c.red(), c.green(), c.blue(), 10))
            grad.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 0))
            p.fillRect(int(x), int(y), int(w), int(h), grad)
            p.restore()

    def paint_scene(self, p, pix, x, y, w, h, export=False):
        p.drawPixmap(int(x), int(y), pix)
        if self.overlay:
            grad = QLinearGradient(0,y+h*.60,0,y+h)
            grad.setColorAt(0,QColor(7,8,14,0))
            grad.setColorAt(1,QColor(7,8,14,self.overlay_opacity))
            p.fillRect(int(x),int(y+h*.55),int(w),int(h*.45),grad)

        self._draw_decorations(p,x,y,w,h)

        if self.frame == "soft":
            p.setPen(QPen(QColor(self.accent.red(),self.accent.green(),self.accent.blue(),150), 3))
            p.drawRoundedRect(int(x+16),int(y+16),int(w-32),int(h-32),18,18)
        elif self.frame == "letter":
            p.setPen(QPen(QColor(self.accent.red(),self.accent.green(),self.accent.blue(),190), 2))
            p.drawRect(int(x+28),int(y+28),int(w-56),int(h-56))
            p.setPen(QPen(QColor(255,255,255,90),1))
            p.drawRect(int(x+38),int(y+38),int(w-76),int(h-76))
        elif self.frame == "vintage":
            p.setPen(QPen(QColor(self.accent.red(),self.accent.green(),self.accent.blue(),180), 5))
            p.drawRect(int(x+20),int(y+20),int(w-40),int(h-40))
            p.setPen(QPen(QColor(255,255,255,90),1))
            p.drawRect(int(x+31),int(y+31),int(w-62),int(h-62))

        if self.text:
            fs = int(self.font_size * (w / pix.width()))
            font = QFont(self.font_family, max(8,fs))
            font.setWeight(QFont.Weight.Medium)
            p.setFont(font)
            rect = p.boundingRect(
                int(x+55), int(y+h*self.position.y()-120),
                int(w-110), 240,
                Qt.TextWordWrap | Qt.AlignHCenter, self.text
            )
            rect.moveTop(max(int(y+25),min(rect.top(),int(y+h-rect.height()-25))))
            if self.shadow:
                p.setPen(QColor(0,0,0,205))
                p.drawText(rect.translated(3,4),Qt.TextWordWrap|Qt.AlignHCenter,self.text)
            p.setPen(self.text_color)
            p.drawText(rect,Qt.TextWordWrap|Qt.AlignHCenter,self.text)

    def paintEvent(self, event):
        p=QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.fillRect(self.rect(),QColor("#07090e"))
        if self.pixmap.isNull():
            p.setPen(QColor("#8991a2"))
            p.setFont(QFont("Segoe UI",16))
            p.drawText(self.rect(),Qt.AlignCenter,"Choose an image folder")
            return
        x,y,w,h,scale=self.image_rect()
        pix=self.pixmap.scaled(int(w),int(h),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.paint_scene(p,pix,x,y,w,h)
        p.end()

    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton and self.text and not self.pixmap.isNull():
            self.dragging=True; self.last_pos=e.position()

    def mouseMoveEvent(self,e):
        if self.dragging and self.last_pos:
            r=self.image_rect()
            if r:
                _,_,w,h,_=r
                d=e.position()-self.last_pos
                self.position.setX(max(.05,min(.95,self.position.x()+d.x()/w)))
                self.position.setY(max(.05,min(.95,self.position.y()+d.y()/h)))
                self.last_pos=e.position(); self.changed.emit(); self.update()

    def mouseReleaseEvent(self,e):
        self.dragging=False; self.last_pos=None

    def rendered(self):
        if self.pixmap.isNull(): return QPixmap()
        out=QPixmap(self.pixmap.size())
        p=QPainter(out)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        self.paint_scene(p,self.pixmap,0,0,out.width(),out.height(),True)
        p.end()
        return out

class TextDialog(QDialog):
    def __init__(self,parent,record=None):
        super().__init__(parent)
        self.setWindowTitle("Literary Stanza")
        self.resize(700,560)
        l=QVBoxLayout(self)

        self.author=QLineEdit(record.get("author","") if record else "")
        self.poem=QLineEdit((record.get("poem_title","") or record.get("work_title","")) if record else "")
        self.category=QLineEdit(record.get("category","Love & Devotion") if record else "Love & Devotion")
        self.mood=QLineEdit(record.get("mood","Tender") if record else "Tender")
        self.source=QLineEdit(record.get("source","") if record else "")
        self.stanza=QTextEdit(record.get("stanza","") if record else "")

        for name,w in [
            ("Author",self.author),
            ("Poem / Work",self.poem),
            ("Category",self.category),
            ("Mood",self.mood),
            ("Source",self.source),
            ("Stanza",self.stanza),
        ]:
            l.addWidget(QLabel(name))
            l.addWidget(w)

        b=QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel)
        b.accepted.connect(self.accept)
        b.rejected.connect(self.reject)
        l.addWidget(b)

    def record(self):
        return {
            "id":"",
            "image_slot":"",
            "author":self.author.text().strip(),
            "poem_title":self.poem.text().strip(),
            "category":self.category.text().strip(),
            "mood":self.mood.text().strip(),
            "stanza":self.stanza.toPlainText().strip(),
            "source":self.source.text().strip(),
            "license":""
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1650,980)
        self.records=[]
        self.images=[]
        self.current_image=None
        self.export_dir=None
        self.load_data()
        self.build()
        self.apply_theme()
        self.refresh_explorer()

    def load_data(self):
        self.records=[]
        if DATASET.exists():
            with DATASET.open("r",encoding="utf-8-sig",newline="") as f:
                self.records=list(csv.DictReader(f))
        # Also load the dedicated Love & Separation collection if present.
        if SEPARATION_DATASET.exists():
            with SEPARATION_DATASET.open("r",encoding="utf-8-sig",newline="") as f:
                extra=list(csv.DictReader(f))
            seen={(r.get("author",""),r.get("poem_title",""),r.get("stanza", "")) for r in self.records}
            for r in extra:
                key=(r.get("author",""),r.get("poem_title",""),r.get("stanza", ""))
                if key not in seen:
                    self.records.append(r)

    def save_data(self):
        fields=["id","image_slot","author","poem_title","category","mood","stanza","source","license"]
        with DATASET.open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
            w.writeheader()
            w.writerows(self.records)

    def section(self,t):
        x=QLabel(t)
        x.setObjectName("section")
        return x

    def build(self):
        c=QWidget()
        self.setCentralWidget(c)
        root=QVBoxLayout(c)
        root.setContentsMargins(18,18,18,18)
        root.setSpacing(11)

        h=QHBoxLayout()
        title=QLabel("♥ JASS <b>Romantic Image Studio</b> <span style='color:#eaa5c0'>V5</span>")
        title.setObjectName("title")
        h.addWidget(title)
        h.addWidget(QLabel("Literary Stanza Explorer • Creative Image Studio"))
        h.addStretch()
        root.addLayout(h)

        tb=QHBoxLayout()
        buttons=[
            ("📁 Images",self.choose_images),
            ("📂 Export",self.choose_export),
            ("💾 Export",self.export_current),
            ("✨ Batch",self.batch_export),
            ("🔄 Build 500",self.build_dataset),
            ("❤️ Love & Separation",self.show_love_separation),
            ("↻ Reload",self.reload_dataset),
            ("📝 Add Stanza",self.add_text),
            ("✏ Edit",self.edit_text),
        ]
        for txt,fn in buttons:
            b=QPushButton(txt)
            b.clicked.connect(fn)
            tb.addWidget(b)
        tb.addStretch()
        self.status=QLabel()
        self.status.setObjectName("status")
        tb.addWidget(self.status)
        root.addLayout(tb)

        sp=QSplitter(Qt.Horizontal)
        root.addWidget(sp,1)

        # Image gallery
        left=QFrame()
        left.setObjectName("panel")
        ll=QVBoxLayout(left)
        ll.addWidget(self.section("IMAGE GALLERY"))
        self.img_search=QLineEdit()
        self.img_search.setPlaceholderText("Search images…")
        self.img_search.textChanged.connect(self.filter_images)
        ll.addWidget(self.img_search)
        self.imgs=QListWidget()
        self.imgs.setIconSize(QSize(100,72))
        self.imgs.currentItemChanged.connect(self.image_selected)
        ll.addWidget(self.imgs,1)
        sp.addWidget(left)

        # Canvas
        center=QFrame()
        center.setObjectName("panel")
        cl=QVBoxLayout(center)
        cl.addWidget(self.section("CREATIVE CANVAS"))
        self.canvas=Canvas()
        self.canvas.changed.connect(self.canvas.update)
        cl.addWidget(self.canvas,1)
        tip=QLabel("Drag the stanza • choose a template • decorate • export")
        tip.setObjectName("tip")
        cl.addWidget(tip)
        sp.addWidget(center)

        # Literary explorer
        right=QFrame()
        right.setObjectName("panel")
        rl=QVBoxLayout(right)
        rl.addWidget(self.section("📚 STANZA EXPLORER"))

        self.search=QLineEdit()
        self.search.setPlaceholderText("Search author, poem, theme or stanza…")
        self.search.textChanged.connect(self.refresh_explorer)
        rl.addWidget(self.search)

        self.author_filter=QComboBox()
        self.author_filter.addItem("All authors")
        self.author_filter.currentTextChanged.connect(self.refresh_explorer)
        rl.addWidget(self.author_filter)

        self.poem_filter=QComboBox()
        self.poem_filter.addItem("All poems / works")
        self.poem_filter.currentTextChanged.connect(self.refresh_explorer)
        rl.addWidget(self.poem_filter)

        self.category_filter=QComboBox()
        self.category_filter.addItem("All categories")
        self.category_filter.currentTextChanged.connect(self.refresh_explorer)
        rl.addWidget(self.category_filter)

        self.results=QListWidget()
        self.results.setWordWrap(True)
        self.results.setSpacing(5)
        self.results.currentItemChanged.connect(self.explorer_selected)
        rl.addWidget(self.results,1)

        self.preview_title=QLabel("Select a stanza")
        self.preview_title.setObjectName("previewTitle")
        self.preview_title.setWordWrap(True)
        rl.addWidget(self.preview_title)

        self.preview=QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumHeight(150)
        rl.addWidget(self.preview)

        self.use_btn=QPushButton("🎨 Use Selected Stanza on Canvas")
        self.use_btn.clicked.connect(self.use_selected_stanza)
        rl.addWidget(self.use_btn)

        sp.addWidget(right)

        # Design controls
        design=QFrame()
        design.setObjectName("panel")
        dl=QVBoxLayout(design)
        dl.addWidget(self.section("DESIGN STUDIO"))

        dl.addWidget(QLabel("Template"))
        self.template=QComboBox()
        self.template.addItems(TEMPLATES.keys())
        self.template.currentTextChanged.connect(self.apply_template)
        dl.addWidget(self.template)

        style=QGroupBox("STYLE & DECORATION")
        g=QGridLayout(style)

        self.font=QComboBox()
        self.font.addItems(sorted(QFontDatabase.families()))
        if "Georgia" in QFontDatabase.families():
            self.font.setCurrentText("Georgia")
        self.font.currentTextChanged.connect(self.style_changed)
        g.addWidget(QLabel("Font"),0,0)
        g.addWidget(self.font,0,1)

        self.size=QSlider(Qt.Horizontal)
        self.size.setRange(18,100)
        self.size.setValue(42)
        self.size.valueChanged.connect(self.style_changed)
        g.addWidget(QLabel("Size"),1,0)
        g.addWidget(self.size,1,1)

        self.shadow=QCheckBox("Text shadow")
        self.shadow.setChecked(True)
        self.shadow.stateChanged.connect(self.style_changed)
        g.addWidget(self.shadow,2,0,1,2)

        self.decoration=QComboBox()
        self.decoration.addItems(["Hearts","Sparkle","Corner","Floral","Glow","None"])
        self.decoration.currentTextChanged.connect(self.style_changed)
        g.addWidget(QLabel("Decoration"),3,0)
        g.addWidget(self.decoration,3,1)

        color=QPushButton("🎨 Text Color")
        color.clicked.connect(self.choose_color)
        g.addWidget(color,4,0)

        accent=QPushButton("✦ Accent Color")
        accent.clicked.connect(self.choose_accent)
        g.addWidget(accent,4,1)

        presets=QHBoxLayout()
        for label,y in [("Top",.18),("Center",.50),("Bottom",.82)]:
            b=QPushButton(label)
            b.clicked.connect(lambda _,yy=y:self.set_position(.5,yy))
            presets.addWidget(b)
        g.addLayout(presets,5,0,1,2)

        dl.addWidget(style)
        dl.addStretch()
        sp.addWidget(design)
        sp.setSizes([250,650,510,360])

        self.refresh_filter_options()
        self.update_status()

    def apply_theme(self):
        self.setStyleSheet("""
        QMainWindow,QWidget{background:#0f121a;color:#f8f2f5;font-family:"Segoe UI";}
        QLabel#title{font-size:29px;font-weight:700;}
        QLabel#section{color:#efa8c4;font-size:12px;font-weight:700;letter-spacing:2px;}
        QLabel#status{color:#a8dcc4;}
        QLabel#tip{color:#929bad;padding:5px;}
        QLabel#previewTitle{color:#f2abc6;font-size:14px;font-weight:700;padding:4px;}
        QFrame#panel{background:#171b26;border:1px solid #2d3444;border-radius:16px;}
        QLineEdit,QComboBox,QTextEdit{background:#0b0e15;border:1px solid #343d51;border-radius:9px;padding:9px;color:white;}
        QListWidget{background:#0b0e15;border:1px solid #343d51;border-radius:10px;padding:5px;}
        QListWidget::item{padding:9px;border-radius:8px;}
        QListWidget::item:selected{background:#713d5b;}
        QPushButton{background:#272e3d;border:1px solid #3a455b;border-radius:9px;padding:9px 13px;font-weight:600;}
        QPushButton:hover{background:#713d5b;}
        QGroupBox{border:1px solid #30394c;border-radius:11px;margin-top:10px;padding-top:12px;}
        QGroupBox::title{subcontrol-origin:margin;left:12px;padding:0 6px;color:#eaa5c0;}
        QSlider::groove:horizontal{height:5px;background:#313a4e;border-radius:3px;}
        QSlider::handle:horizontal{width:16px;margin:-6px 0;border-radius:8px;background:#eca9c3;}
        """)

    def update_status(self):
        if DATASET.exists() or SEPARATION_DATASET.exists():
            sep_count=0
            if SEPARATION_DATASET.exists():
                try:
                    with SEPARATION_DATASET.open("r",encoding="utf-8-sig",newline="") as f:
                        sep_count=max(0,sum(1 for _ in csv.DictReader(f)))
                except Exception:
                    sep_count=0
            self.status.setText(f"📚 {len(self.records)} literary stanzas • ❤️ {sep_count} Love & Separation")
        else:
            self.status.setText("⚠ Dataset not found • click 🔄 Build 500")

    def refresh_filter_options(self):
        def fill(combo, values, first):
            current=combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(first)
            for v in sorted({x for x in values if x}):
                combo.addItem(v)
            if current in [combo.itemText(i) for i in range(combo.count())]:
                combo.setCurrentText(current)
            combo.blockSignals(False)

        fill(self.author_filter,[r.get("author","") for r in self.records],"All authors")
        fill(self.poem_filter,[r.get("poem_title","") or r.get("work_title","") for r in self.records],"All poems / works")
        fill(self.category_filter,[r.get("category","") for r in self.records],"All categories")

    def refresh_explorer(self):
        if not hasattr(self,"results"):
            return

        q=self.search.text().strip().lower()
        author=self.author_filter.currentText()
        poem=self.poem_filter.currentText()
        category=self.category_filter.currentText()

        self.results.blockSignals(True)
        self.results.clear()

        matches=[]
        for r in self.records:
            r_author=r.get("author","")
            r_poem=r.get("poem_title","") or r.get("work_title","")
            r_cat=r.get("category","")
            stanza=r.get("stanza","") or r.get("poem_text","")

            hay=" ".join([
                r_author,r_poem,r_cat,r.get("mood",""),stanza
            ]).lower()

            if q and q not in hay:
                continue
            if author!="All authors" and r_author!=author:
                continue
            if poem!="All poems / works" and r_poem!=poem:
                continue
            if category!="All categories" and r_cat!=category:
                continue
            matches.append(r)

        for r in matches:
            author=r.get("author","") or "Unknown author"
            poem=r.get("poem_title","") or r.get("work_title","") or "Untitled"
            stanza=(r.get("stanza","") or r.get("poem_text","")).replace("\n"," ")
            if len(stanza)>180:
                stanza=stanza[:177]+"…"
            label=f'{r.get("id","")} • {author} — {poem}\n{stanza}'
            item=QListWidgetItem(label)
            item.setData(Qt.UserRole,r)
            self.results.addItem(item)

        self.results.blockSignals(False)

        if self.results.count():
            self.results.setCurrentRow(0)
        else:
            self.preview_title.setText("No stanzas found")
            self.preview.clear()

    def explorer_selected(self,item,_):
        if not item:
            return
        r=item.data(Qt.UserRole)
        author=r.get("author","") or "Unknown author"
        poem=r.get("poem_title","") or r.get("work_title","") or "Untitled"
        cat=r.get("category","")
        mood=r.get("mood","")
        self.preview_title.setText(
            f"{author} — {poem}" + (f"  •  {cat}" if cat else "") +
            (f"  •  {mood}" if mood else "")
        )
        self.preview.setPlainText(r.get("stanza","") or r.get("poem_text",""))

    def use_selected_stanza(self):
        item=self.results.currentItem()
        if not item:
            QMessageBox.information(self,APP_TITLE,"Select a stanza first.")
            return
        r=item.data(Qt.UserRole)
        stanza=r.get("stanza","") or r.get("poem_text","")
        self.canvas.set_text(stanza)
        self.status.setText(
            f'Using stanza • {r.get("author","")} — '
            f'{r.get("poem_title","") or r.get("work_title","")}'
        )

    def build_dataset(self):
        script=Path(__file__).with_name("build_romantic_stanza_dataset.py")
        if not script.exists():
            QMessageBox.warning(self,APP_TITLE,"The dataset builder is missing.")
            return
        import subprocess
        try:
            subprocess.Popen([sys.executable,str(script)],cwd=str(script.parent))
            QMessageBox.information(
                self,APP_TITLE,
                "The dataset builder has been opened in a console window.\n\n"
                "When it finishes, close/restart this app and the 500-stanza "
                "library will appear in the Stanza Explorer."
            )
        except Exception as e:
            QMessageBox.critical(self,APP_TITLE,f"Could not start builder:\n{e}")

    def show_love_separation(self):
        if not SEPARATION_DATASET.exists():
            QMessageBox.information(
                self,APP_TITLE,
                "The Love & Separation collection has not been built yet.\n\n"
                "Click 🔄 Build 500 first, then click ↻ Reload."
            )
            return
        # Reset all other filters as well. Otherwise a previously selected
        # author/poem can silently intersect with Love & Separation and
        # produce an empty result list.
        self.search.clear()
        self.author_filter.setCurrentText("All authors")
        self.poem_filter.setCurrentText("All poems / works")
        self.category_filter.setCurrentText("Love & Separation")
        self.refresh_explorer()

    def reload_dataset(self):
        self.load_data()
        self.refresh_filter_options()
        self.refresh_explorer()
        self.update_status()
        if self.records:
            QMessageBox.information(
                self,APP_TITLE,
                f"Dataset loaded successfully: {len(self.records)} stanzas."
            )
        else:
            QMessageBox.warning(
                self,APP_TITLE,
                "No stanza records were found. Click 🔄 Build 500 first."
            )

    def choose_images(self):
        d=QFileDialog.getExistingDirectory(self,"Choose image folder")
        if not d:
            return
        self.images=[p for p in sorted(Path(d).iterdir()) if p.suffix.lower() in EXTS]
        self.imgs.clear()
        for p in self.images:
            i=QListWidgetItem(p.name)
            px=QPixmap(str(p))
            if not px.isNull():
                i.setIcon(px.scaled(100,72,Qt.KeepAspectRatio,Qt.SmoothTransformation))
            i.setData(Qt.UserRole,str(p))
            self.imgs.addItem(i)
        self.status.setText(f"{len(self.images)} images • {len(self.records)} stanzas")
        if self.imgs.count():
            self.imgs.setCurrentRow(0)

    def choose_export(self):
        d=QFileDialog.getExistingDirectory(self,"Choose export folder")
        if d:
            self.export_dir=Path(d)

    def image_selected(self,item,_):
        if item:
            self.current_image=Path(item.data(Qt.UserRole))
            self.canvas.set_image(self.current_image)

    def filter_images(self,q):
        q=q.lower()
        for i in range(self.imgs.count()):
            self.imgs.item(i).setHidden(q not in self.imgs.item(i).text().lower())

    def apply_template(self,name):
        self.canvas.set_template(name)
        cfg=TEMPLATES[name]
        self.font.setCurrentText(
            cfg["font"] if cfg["font"] in
            [self.font.itemText(i) for i in range(self.font.count())]
            else self.font.currentText()
        )
        self.style_changed()

    def style_changed(self):
        self.canvas.font_family=self.font.currentText()
        self.canvas.font_size=self.size.value()
        self.canvas.shadow=self.shadow.isChecked()
        self.canvas.decoration=self.decoration.currentText().lower()
        self.canvas.update()

    def choose_color(self):
        c=QColorDialog.getColor(self.canvas.text_color,self,"Text color")
        if c.isValid():
            self.canvas.text_color=c
            self.canvas.update()

    def choose_accent(self):
        c=QColorDialog.getColor(self.canvas.accent,self,"Accent color")
        if c.isValid():
            self.canvas.accent=c
            self.canvas.update()

    def set_position(self,x,y):
        self.canvas.position=QPointF(x,y)
        self.canvas.update()

    def add_text(self):
        d=TextDialog(self)
        if d.exec()!=QDialog.Accepted:
            return
        r=d.record()
        r["id"]=f"R{len(self.records)+1:03d}"
        r["image_slot"]=f"image_{len(self.records)+1:03d}"
        self.records.append(r)
        self.save_data()
        self.refresh_filter_options()
        self.refresh_explorer()
        self.update_status()

    def edit_text(self):
        item=self.results.currentItem()
        if not item:
            return
        old=item.data(Qt.UserRole)
        idx=next((i for i,r in enumerate(self.records)
                  if r.get("id")==old.get("id")),None)
        if idx is None:
            return
        d=TextDialog(self,self.records[idx])
        if d.exec()==QDialog.Accepted:
            n=d.record()
            n["id"]=old.get("id","")
            n["image_slot"]=old.get("image_slot","")
            self.records[idx]=n
            self.save_data()
            self.refresh_filter_options()
            self.refresh_explorer()
            self.update_status()

    def current_render(self):
        if self.canvas.pixmap.isNull() or not self.canvas.text:
            QMessageBox.information(
                self,APP_TITLE,"Choose an image and a stanza first."
            )
            return None
        return self.canvas.rendered()

    def export_current(self):
        out=self.current_render()
        if out is None:
            return
        if self.export_dir is None:
            self.choose_export()
        if self.export_dir is None:
            return
        self.export_dir.mkdir(parents=True,exist_ok=True)

        item=self.results.currentItem()
        rid=item.data(Qt.UserRole).get("id","stanza") if item else "stanza"
        base=self.current_image.stem if self.current_image else "image"
        name=f"{base}_{rid}_{self.template.currentText().lower().replace(' ','_')}.jpg"
        path=self.export_dir/name
        out.save(str(path),"JPG",97)
        self.status.setText(f"Exported {path.name}")

    def batch_export(self):
        if not self.images:
            QMessageBox.information(self,APP_TITLE,"Choose an image folder first.")
            return
        if self.export_dir is None:
            self.choose_export()
        if self.export_dir is None:
            return
        if not self.canvas.text:
            QMessageBox.information(self,APP_TITLE,"Choose a stanza first.")
            return

        self.export_dir.mkdir(parents=True,exist_ok=True)
        item=self.results.currentItem()
        rid=item.data(Qt.UserRole).get("id","stanza") if item else "stanza"
        original=self.canvas.pixmap
        count=0

        for pth in self.images:
            pix=QPixmap(str(pth))
            if pix.isNull():
                continue
            self.canvas.pixmap=pix
            out=self.canvas.rendered()
            name=f"{pth.stem}_{rid}_{self.template.currentText().lower().replace(' ','_')}.jpg"
            out.save(str(self.export_dir/name),"JPG",97)
            count+=1

        self.canvas.pixmap=original
        self.canvas.update()
        self.status.setText(f"Batch exported {count} images")

if __name__=="__main__":
    app=QApplication(sys.argv)
    w=MainWindow();w.show()
    sys.exit(app.exec())
