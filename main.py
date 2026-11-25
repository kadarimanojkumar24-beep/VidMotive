
import sys, re, webbrowser, threading
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFrame

URL_RE = re.compile(r'https?://[^\s]+', re.I)

def platform_for(url):
    u=url.lower()
    if "instagram.com" in u: return "Instagram Reel / Post"
    if "youtube.com" in u or "youtu.be" in u: return "YouTube"
    if "tiktok.com" in u: return "TikTok"
    if "facebook.com" in u or "fb.watch" in u: return "Facebook"
    if "x.com" in u or "twitter.com" in u: return "X"
    return "Video / Web link"

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(390, 470)
        self.drag_pos=None
        self.last_url=""
        self.build_ui()
        self.move_to_corner()

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(700)

    def move_to_corner(self):
        screen=QGuiApplication.primaryScreen().availableGeometry()
        self.move(screen.right()-self.width()-24, screen.bottom()-self.height()-24)

    def build_ui(self):
        root=QFrame()
        root.setObjectName("card")
        root.setStyleSheet("""
        #card { background: rgba(14,18,35,245); border:1px solid #34446e;
                border-radius:24px; }
        QLabel { color:#eaf0ff; }
        QLineEdit { background:#10162b; color:#dce5ff; border:1px solid #3c4b75;
                    border-radius:12px; padding:10px; }
        QPushButton { background:#5867f2; color:white; border:0; border-radius:12px;
                      padding:10px 14px; font-weight:600; }
        QPushButton:hover { background:#6d7cff; }
        #close { background:transparent; color:#9ba8ca; font-size:18px; }
        #hint { color:#91a0c4; }
        #score { color:#8ee6ff; font-size:22px; font-weight:700; }
        """)
        layout=QVBoxLayout(root); layout.setContentsMargins(20,18,20,20); layout.setSpacing(12)

        top=QHBoxLayout()
        title=QLabel("✦ VIDMOTIVE AI"); title.setFont(QFont("Segoe UI",15,QFont.Bold))
        close=QPushButton("×"); close.setObjectName("close"); close.clicked.connect(self.close)
        top.addWidget(title); top.addStretch(); top.addWidget(close)
        layout.addLayout(top)

        sub=QLabel("Copy a video link anywhere. I'll detect it.")
        sub.setObjectName("hint"); layout.addWidget(sub)

        self.url=QLineEdit(); self.url.setPlaceholderText("Paste a video URL…")
        layout.addWidget(self.url)

        row=QHBoxLayout()
        analyze=QPushButton("ANALYZE")
        analyze.clicked.connect(self.analyze)
        watch=QPushButton("WATCH ORIGINAL")
        watch.clicked.connect(self.open_original)
        row.addWidget(analyze); row.addWidget(watch)
        layout.addLayout(row)

        self.platform=QLabel("Waiting for a video link…")
        self.platform.setFont(QFont("Segoe UI",12,QFont.Bold)); layout.addWidget(self.platform)

        self.message=QLabel("Your copied link will appear here automatically.")
        self.message.setWordWrap(True); layout.addWidget(self.message)

        self.score=QLabel("—"); self.score.setObjectName("score")
        self.score.setAlignment(Qt.AlignCenter); layout.addWidget(self.score)

        hint=QLabel("Tip: use Share → Copy Link on your phone, or Ctrl+C on Windows.")
        hint.setObjectName("hint"); hint.setWordWrap(True); layout.addWidget(hint)
        layout.addStretch()

        outer=QVBoxLayout(self); outer.setContentsMargins(0,0,0,0); outer.addWidget(root)

    def check_clipboard(self):
        text=QApplication.clipboard().text().strip()
        if text and text != self.last_url:
            m=URL_RE.search(text)
            if m and any(x in m.group(0).lower() for x in
                          ("instagram.com","youtube.com","youtu.be","tiktok.com","facebook.com","fb.watch","x.com","twitter.com")):
                self.last_url=m.group(0).rstrip(").,")
                self.url.setText(self.last_url)
                self.analyze()
                self.show()
                self.raise_()
                self.activateWindow()

    def analyze(self):
        u=self.url.text().strip()
        if not u: return
        p=platform_for(u)
        self.platform.setText("●  "+p)
        self.message.setText(
            "A video link was detected. Open the original content to watch it. "
            "Use the AI panel here as a quick motivation layer before you watch."
        )
        # Demo score; replace with your backend/AI scoring later.
        score={"Instagram Reel / Post":91,"YouTube":86,"TikTok":89,"Facebook":82,"X":78}.get(p,75)
        self.score.setText(f"Motivation potential  {score}%")

    def open_original(self):
        u=self.url.text().strip()
        if u: webbrowser.open(u)

    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton: self.drag_pos=e.globalPosition().toPoint()-self.frameGeometry().topLeft()

    def mouseMoveEvent(self,e):
        if self.drag_pos is not None and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint()-self.drag_pos)

    def mouseReleaseEvent(self,e):
        self.drag_pos=None

app=QApplication(sys.argv)
app.setApplicationName("VidMotive AI")
w=Widget(); w.show()
sys.exit(app.exec())
