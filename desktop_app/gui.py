from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QSlider, QComboBox, QFormLayout, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCursor

SETTINGS_QSS = """
QWidget {
    background-color: #18191D;
    color: #E2E8F0;
    font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
}
QLabel {
    color: #94A3B8;
    font-size: 12px;
    font-weight: bold;
}
QSlider::groove:horizontal {
    border: 1px solid #334155;
    height: 6px;
    background: #0F172A;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #3B82F6;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #FFFFFF;
    border: 2px solid #3B82F6;
    width: 14px;
    height: 14px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 7px;
}
QComboBox {
    background-color: #23252B;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    color: #E2E8F0;
    font-weight: 500;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox:hover {
    border: 1px solid #3B82F6;
}
QComboBox QAbstractItemView {
    background-color: #23252B;
    border: 1px solid #334155;
    selection-background-color: #3B82F6;
    color: white;
}
"""

class SubtitleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setMouseTracking(True)
        self.dragging = False
        self.resize_margin = 20
        self.resize_mode = None
        self.current_font_size = 28
        self.history = []
        
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(400, 150)
        self.resize(1000, 200)
        
        self.central_widget = QWidget()
        self.central_widget.setMouseTracking(True)
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.bg_widget = QWidget()
        self.bg_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.bg_widget.setMouseTracking(True)
        self.bg_widget.setStyleSheet(f"background-color: rgba(0, 0, 0, 150); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);")
        
        bg_layout = QVBoxLayout()
        bg_layout.setContentsMargins(20, 20, 20, 20)
        
        self.subtitle_text = QTextEdit()
        self.subtitle_text.setReadOnly(True)
        self.subtitle_text.setStyleSheet("background: transparent; border: none; color: white;")
        self.subtitle_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.subtitle_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.subtitle_text.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.subtitle_text.setCursorWidth(0)
        self.subtitle_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        bg_layout.addWidget(self.subtitle_text)
        self.bg_widget.setLayout(bg_layout)
        layout.addWidget(self.bg_widget)
        
        self.central_widget.setLayout(layout)
        self.render_subtitles()

    def update_subtitle(self, orig_text, trans_text, is_final):
        self._started_speaking = True
        html = ""
        # 渲染历史记录 (保留最近3句)
        for past_o, past_t in self.history[-3:]:
             html += self._render_line(past_o, past_t, is_active=False)
        
        # 渲染当前正在识别的句子
        if orig_text.strip():
            html += self._render_line(orig_text, trans_text, is_active=True)
            
        self.subtitle_text.setUpdatesEnabled(False)
        self.subtitle_text.setHtml(html)
        
        # 移动光标到底部，自动完成滚动而不产生视觉闪断
        cursor = self.subtitle_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.subtitle_text.setTextCursor(cursor)
        
        self.subtitle_text.setUpdatesEnabled(True)
        
        # 如果句子结束，则将其推入历史记录
        if is_final and orig_text.strip():
            # 防止重复推入相同的最后一句话
            if len(self.history) == 0 or self.history[-1][0] != orig_text:
                self.history.append((orig_text, trans_text))
            if len(self.history) > 10:
                self.history.pop(0)

    def _render_line(self, orig, trans, is_active):
        trans_size = int(self.current_font_size * 0.75)
        # 历史记录稍微变暗一点点
        alpha = "1.0" if is_active else "0.75"
        color_orig = f"rgba(255, 255, 255, {alpha})"
        color_trans = f"rgba(147, 197, 253, {alpha})" # Tailwind blue-300
        
        html = f'<div style="margin-bottom: 8px;">'
        html += f'<span style="color: {color_orig}; font-weight: 500; font-family: \'Microsoft YaHei\'; font-size: {self.current_font_size}px; letter-spacing: 1px;">{orig}</span>'
        if trans:
            html += f'<br><span style="color: {color_trans}; font-family: \'Microsoft YaHei\'; font-size: {trans_size}px; letter-spacing: 1px;">{trans}</span>'
        html += '</div>'
        return html

    def set_font_size(self, size):
        self.current_font_size = size
        self.render_subtitles()
        
    def render_subtitles(self):
        html = ""
        # 始终保持最近的2-3句话上下文
        for past_o, past_t in self.history[-3:]:
            if past_o.strip():
                html += self._render_line(past_o, past_t, is_active=False)
                
        # 初始化没有任何语音时的占位提示
        if not html and not hasattr(self, '_started_speaking'):
            html = self._render_line("🌟 模型与环境就绪，等待语音输入...", "", is_active=True)
            
        self.subtitle_text.setHtml(html)
        
    def set_bg_opacity(self, opacity):
        self.bg_widget.setStyleSheet(f"background-color: rgba(0, 0, 0, {opacity}); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);")

    # Drag and Resize
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            y = event.position().y()
            w = self.width()
            h = self.height()
            
            if x >= w - self.resize_margin and y >= h - self.resize_margin:
                self.resize_mode = 'bottom-right'
            elif x >= w - self.resize_margin:
                self.resize_mode = 'right'
            elif y >= h - self.resize_margin:
                self.resize_mode = 'bottom'
            else:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                self.resize_mode = None
            event.accept()

    def mouseMoveEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        w = self.width()
        h = self.height()

        if x >= w - self.resize_margin and y >= h - self.resize_margin:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif x >= w - self.resize_margin:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif y >= h - self.resize_margin:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if self.resize_mode:
            new_w = x if 'right' in self.resize_mode else w
            new_h = y if 'bottom' in self.resize_mode else h
            self.resize(int(max(new_w, self.minimumWidth())), int(max(new_h, self.minimumHeight())))
        elif self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resize_mode = None


class SettingsWindow(QWidget):
    language_changed = pyqtSignal(str)
    mode_changed = pyqtSignal(str)
    model_changed = pyqtSignal(str)

    def __init__(self, subtitle_window: SubtitleWindow):
        super().__init__()
        self.subtitle_window = subtitle_window
        self.setWindowTitle("WhisperScribe Pro - 设置")
        self.resize(380, 420)
        self.setStyleSheet(SETTINGS_QSS)
        self.initUI()
        
    def initUI(self):
        layout = QFormLayout()
        layout.setContentsMargins(20, 25, 20, 25)
        layout.setVerticalSpacing(20)

        self.font_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_slider.setMinimum(12)
        self.font_slider.setMaximum(72)
        self.font_slider.setValue(28)
        self.font_slider.valueChanged.connect(self.on_font_size_changed)
        layout.addRow("字号大小", self.font_slider)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(255)
        self.opacity_slider.setValue(150)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        layout.addRow("背景透明度", self.opacity_slider)

        self.lang_cb = QComboBox()
        self.lang_cb.addItems(["ja (日语)", "en (英语)"]) # 默认日语以防测试
        self.lang_cb.currentTextChanged.connect(self.on_language_changed)
        layout.addRow("音频语言", self.lang_cb)

        self.mode_cb = QComboBox()
        self.mode_cb.addItems(["原文 + 中文翻译", "仅原文"])
        self.mode_cb.currentTextChanged.connect(self.on_mode_changed)
        layout.addRow("显示模式", self.mode_cb)

        self.model_cb = QComboBox()
        self.model_cb.addItems(["small (默认,平衡)", "tiny (最快,精度低)", "base (较快,稍重)", "medium (较慢,高精)", "large-v3 (极慢,极高)"])
        self.model_cb.currentTextChanged.connect(self.on_model_changed)
        layout.addRow("识别模型", self.model_cb)

        # 添加模型和缓存提示说明，因为用户问了默认存储位置
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("background: transparent; border: 1px solid #334155; color: #94A3B8; font-size: 13px;")
        info_text.setPlainText("模型下载位置 (如果找不到请开启显示隐藏文件):\n"
                               "- Whisper语音识别模型:\n"
                               "  C:\\Users\\<您的用户名>\\.cache\\huggingface\\hub\\\n"
                               "- ArgosTranslate翻译模型:\n"
                               "  C:\\Users\\<您的用户名>\\.local\\share\\argos-translate\\packages\\\n\n"
                               "可自由切换上方模型版本以兼顾速度与准确度，初次切换等待下载。")
        info_layout = QVBoxLayout()
        info_layout.addWidget(info_text)
        layout.addRow("帮助信息", info_layout)

        self.setLayout(layout)

    def on_model_changed(self, text):
        model_name = text.split(" ")[0]
        self.model_changed.emit(model_name)

    def on_font_size_changed(self, value):
        self.subtitle_window.set_font_size(value)

    def on_opacity_changed(self, value):
        self.subtitle_window.set_bg_opacity(value)

    def on_language_changed(self, text):
        lang = text.split(" ")[0]
        self.language_changed.emit(lang)

    def on_mode_changed(self, text):
        if "仅原文" in text:
            self.mode_changed.emit("source_only")
        else:
            self.mode_changed.emit("translated")
