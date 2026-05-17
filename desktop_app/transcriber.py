import threading
import queue
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from faster_whisper import WhisperModel
import argostranslate.package
import argostranslate.translate
import time

class TranscriptionWorker(QThread):
    # 发送：原文，翻译文，是否是这一句话的最终段
    update_signal = pyqtSignal(str, str, bool) 

    def __init__(self, audio_queue: queue.Queue):
        super().__init__()
        self.audio_queue = audio_queue
        self.running = True
        self.source_language = "ja" 
        self.display_mode = "translated"
        self.model_name = "small"
        self.reload_model_flag = False
        
        self.sample_rate = 16000
        self.model = None

    def set_model_name(self, model_name):
        if self.model_name != model_name:
            self.model_name = model_name
            self.reload_model_flag = True

    def init_translators(self):
        self.update_signal.emit("正在配置翻译环境 (首次需要下载模型)...", "", False)
        try:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()

            def install_if_needed(from_code, to_code):
                package_to_install = next(
                    filter(
                        lambda x: x.from_code == from_code and x.to_code == to_code,
                        available_packages
                    ), None
                )
                if package_to_install:
                    print(f"Installing translation model: {from_code} -> {to_code}")
                    argostranslate.package.install_from_path(package_to_install.download())

            # Argos Translate 通常需要英语作为枢纽(Pivot)语言
            install_if_needed('en', 'zh')
            install_if_needed('ja', 'en')
        except Exception as e:
            print("Failed to install translator models:", e)
            
        self.update_signal.emit("初始化完成，您可以开始播放语音。", "", True)

    def set_source_language(self, lang):
        if self.source_language != lang:
            self.source_language = lang
            self.update_signal.emit("", "", True)

    def set_display_mode(self, mode):
        self.display_mode = mode

    def translate(self, text, from_lang):
        if not text.strip():
            return ""
        try:
            if from_lang == "ja":
                # ja -> en
                en_text = argostranslate.translate.translate(text, "ja", "en")
                # en -> zh
                return argostranslate.translate.translate(en_text, "en", "zh")
            else:
                return argostranslate.translate.translate(text, from_lang, "zh")
        except Exception as e:
            print("Translation error:", e)
            return ""

    def load_model(self):
        self.update_signal.emit(f"正在加载本地模型 {self.model_name}...", "", False)
        try:
            self.model = WhisperModel(self.model_name, device="cuda", compute_type="float16")
        except Exception as e:
            self.model = WhisperModel(self.model_name, device="cpu", compute_type="int8")
        self.update_signal.emit(f"已成功加载模型: {self.model_name}", "", True)

    def run(self):
        self.load_model()
        self.init_translators()
        
        audio_buffer = np.array([], dtype=np.float32)
        silence_duration = 0.0
        
        # 参数调优：平衡准确率与实时性
        chunk_duration = 0.5  # 每次收集 0.5 秒就做一次判断
        silence_threshold = 0.005 # 极小音量阈值，根据输入设备调整
        max_buffer_duration = 15.0 # 最长一句话录制 15 秒强制截断
        turn_end_silence = 1.0 # 当连续静音超过 1 秒，认为本句结束

        last_trans_text = ""
        last_orig_text = ""

        while self.running:
            if self.reload_model_flag:
                self.reload_model_flag = False
                self.load_model()
                audio_buffer = np.array([], dtype=np.float32)
                silence_duration = 0.0
                last_orig_text = ""
                last_trans_text = ""
                
            audio_chunk = np.array([], dtype=np.float32)
            # 收集一小段时间的音频 (chunk_duration)
            start_time = time.time()
            while time.time() - start_time < chunk_duration and self.running:
                try:
                    data = self.audio_queue.get(timeout=0.1)
                    audio_chunk = np.concatenate((audio_chunk, data))
                except queue.Empty:
                    continue
                    
            if len(audio_chunk) == 0:
                continue

            # 判断这 0.5 秒是否是静音
            rms = np.sqrt(np.mean(audio_chunk**2))
            is_silence = rms < silence_threshold

            if is_silence:
                silence_duration += chunk_duration
            else:
                silence_duration = 0.0

            audio_buffer = np.concatenate((audio_buffer, audio_chunk))
            buffer_duration = len(audio_buffer) / self.sample_rate

            # 句子结束的条件：连续静音超过阈值，或者由于缓存过大强制截断
            is_final = False
            if (silence_duration >= turn_end_silence and buffer_duration > 1.0) or buffer_duration >= max_buffer_duration:
                is_final = True
                
            # 当缓冲音频极短且又是静音时，完全不需要送入模型（避免幻觉）
            if buffer_duration < 1.0 and is_silence:
                if silence_duration > turn_end_silence:
                    audio_buffer = np.array([], dtype=np.float32)
                continue

            # 只有当非静音或者当前已经积累了一定长度时，再进行推断
            text = ""
            try:
                # 增大 beam_size 提升准确率 (RTX 4060 足以应对 beam_size=5 的运算量)
                # 移除内部破坏语气的 vad_filter (我们已经在外层控制了空白分句)
                # 开启 condition_on_previous_text=True 找回上下文语义连贯性
                segments, _ = self.model.transcribe(
                    audio_buffer, 
                    language=self.source_language, 
                    beam_size=5,
                    condition_on_previous_text=True,
                    without_timestamps=True
                )
                text = "".join([segment.text for segment in segments]).strip()
            except Exception as e:
                pass

            if text and text != last_orig_text:
                translated_text = ""
                if self.display_mode == "translated":
                    translated_text = self.translate(text, self.source_language)
                    last_trans_text = translated_text
                self.update_signal.emit(text, last_trans_text, is_final)
                last_orig_text = text
            elif is_final and text:
                # 即使识别没有变化，也要把 is_final 信号发出去
                self.update_signal.emit(text, last_trans_text, True)

            if is_final:
                # 彻底清空，进入下一句的聆听
                audio_buffer = np.array([], dtype=np.float32)
                silence_duration = 0.0
                last_orig_text = ""
                last_trans_text = ""

    def stop(self):
        self.running = False
