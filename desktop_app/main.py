import os
import sys
import site

# --- 自动将 pip 安装的 CUDA DLL 路径加入环境变量，修复 cublas64_12.dll 找不到的问题 ---
try:
    for site_dir in site.getsitepackages():
        cublas_path = os.path.join(site_dir, "nvidia", "cublas", "bin")
        cudnn_path = os.path.join(site_dir, "nvidia", "cudnn", "bin")
        if os.path.exists(cublas_path) and cublas_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = cublas_path + os.pathsep + os.environ["PATH"]
        if os.path.exists(cudnn_path) and cudnn_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = cudnn_path + os.pathsep + os.environ["PATH"]
except Exception:
    pass
# -------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication
from gui import SubtitleWindow, SettingsWindow
from transcriber import TranscriptionWorker
from audio_capture import AudioCaptureThread

def main():
    app = QApplication(sys.argv)
    
    # 1. Initialize UI
    subtitle_window = SubtitleWindow()
    settings_window = SettingsWindow(subtitle_window)
    subtitle_window.show()
    settings_window.show()

    # 2. Setup audio capture
    audio_thread = AudioCaptureThread()
    audio_thread.start()

    # 3. Setup Transcription logic
    transcription_worker = TranscriptionWorker(audio_thread.audio_queue)
    transcription_worker.update_signal.connect(subtitle_window.update_subtitle)
    transcription_worker.start()

    # Connect settings to transcription worker
    settings_window.language_changed.connect(transcription_worker.set_source_language)
    settings_window.mode_changed.connect(transcription_worker.set_display_mode)
    settings_window.model_changed.connect(transcription_worker.set_model_name)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
