# WhisperScribe Pro 

[English](#english) | [中文](#中文) | [日本語](#日本語)

---
<img width="1888" height="1061" alt="image" src="https://github.com/user-attachments/assets/381f925e-e022-43bb-89df-1f9c1fcfd562" />
<a name="english"></a>

## English

### Introduction
WhisperScribe Pro is a local, secure, real-time audio transcription and translation desktop application. It captures system audio via WASAPI Loopback, transcribes it locally using `faster-whisper`, and translates it into Chinese offline using `argostranslate`.

### Technologies and Architecture
*   **Audio Capture:** `PyAudioWPatch` grabs Windows speaker output directly via WASAPI Loopback, eliminating the need for virtual audio cables.
*   **Speech Recognition (ASR):** `faster-whisper` (backed by CTranslate2) provides high-performance local inference. It uses a dynamic sliding window buffer and built-in Voice Activity Detection (VAD) to slice sentences efficiently without causing hallucinations or high latency.
*   **Offline Translation:** `argostranslate` provides local, offline translation. It uses a Pivot Translation approach (`ja -> en -> zh`) to handle Japanese to Chinese translations accurately where direct models may fail or perform poorly. 
*   **GUI:** `PyQt6` is used to build a frameless, transparent, on-top subtitle window that supports resizing and dragging. It features an anchor context system showing the last few recognized sentences above the current one.

### Hardware Requirements
*   **Minimum:** 8GB RAM, modern multi-core CPU (runs in CPU Int8 mode).
*   **Recommended:** NVIDIA GPU with 6GB+ VRAM (e.g., RTX 3060 / 4060 or better) to utilize CUDA + float16 acceleration.

### Model Selection and Save Locations
The application downloads AI models locally upon first use.
*   **Whisper Models Location:** `C:\Users\<Your_Username>\.cache\huggingface\hub\`
*   **ArgosTranslate Models Location:** `C:\Users\<Your_Username>\.local\share\argos-translate\packages\`

**Whisper Model Comparison:**
| Model | Parameters | Relative Speed | VRAM/RAM Usage | Accuracy | Recommended For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **tiny** | 39 M | ~10x | ~1 GiB | Low | Ultra low-end devices |
| **base** | 74 M | ~7x | ~1 GiB | Moderate | Basic tasks |
| **small** | 244 M | ~4x | ~2 GiB | Good | Balanced, suitable for RTX 4060 |
| **medium** | 769 M | ~2x | ~5 GiB | High | High accuracy needs |
| **large-v3** | 1550 M | 1x | ~8 GiB | Excellent | Professional transcription |

### Installation Guide
1. **Prerequisites:** Python 3.10 or newer (tested on 3.10.x). Ensure `ffmpeg` is installed and added to your system PATH.
2. **Clone/Download** the repository.
3. **Install Dependencies:**
   ```bash
   pip install faster-whisper argostranslate PyQt6 PyAudioWPatch numpy
   ```
   *Note: For GPU acceleration, ensure you have the appropriate CUDA Toolkit (11.x or 12.x) and cuDNN installed corresponding to your PyTorch/CTranslate2 version.*

### Usage Guide
1. Start the application:
   ```bash
   python desktop_app/main.py
   ```
2. The initial run requires downloading the Whisper and Translate models, which may take some time depending on your network.
3. Once loaded, the Settings window and Subtitle overlay will appear. 
4. Play any audio on your computer. The subtitles will render in real-time.
5. You can change font size, opacity, audio language, and AI model via the settings. Click and drag the subtitle box to move it, or drag the edges to resize.

### Packaging Guide
To build a standalone executable:
1. **Activate your environment:** Ensure your Python environment is active (e.g., Anaconda environment).
2. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
3. **Run the precise build command:**
   *(Make sure to run this from the project root. The path below corresponds to a Conda env example. Adjust your username/env name if different)*
   ```bash
   pyinstaller --name "WhisperScribePro" --noconfirm --onedir --windowed --add-data "C:\Users\ljz\.conda\envs\subtitle_env310\Lib\site-packages\faster_whisper\assets;faster_whisper/assets" desktop_app\main.py
   ```

**Critical Packaging Concepts:**
*   **Why `--add-data`?** Normal PyInstaller commands might miss crucial static asset files (like VAD models) required by `faster_whisper`, causing crashes on run. The explicit path maps these correctly.
*   **Anaconda Environment:** Running `pyinstaller` from within your activated environment allows it to trace and bundle all necessary python dependencies automatically.
*   **Do NOT package the AI Models:** The downloaded Whisper and Argos models in your C drive should **not** be included in the bundle. The application includes initialization logic to auto-download these models upon first launch on any new computer. Bundling them would result in an impractically large application size safely avoided by runtime downloading.

---

<a name="中文"></a>
## 中文

### 简介
WhisperScribe Pro 是一款安全、完全本地运行的实时音频转写与翻译桌面应用。它通过 WASAPI Loopback 捕获系统音频，使用 `faster-whisper` 进行本地识别，并通过 `argostranslate` 进行离线跨语种翻译。

### 技术实现与技术路线
*   **音频捕获：** 使用 `PyAudioWPatch` 通过 WASAPI Loopback 直接抓取 Windows 扬声器输出，无需安装虚拟声卡。
*   **语音识别 (ASR)：** 核心识别引擎采用基于 CTranslate2 优化的 `faster-whisper`。采用独创的流式滑动音频缓冲区 (Sliding Window Buffer) 结合动态 VAD（语音活动检测）切分，在提供毫秒级刷新反馈的同时，有效过滤静音防止模型“幻觉”。
*   **离线翻译：** 集成 `argostranslate`，全部模型离线本地运行。针对部分语种采用枢纽翻译 (Pivot Translation) 技术（例如 `ja -> en -> zh`），突破直接调用低资源语种可能失败或不准确的问题。
*   **GUI 界面：** 基于 `PyQt6` 构建。实现了无边框、背景半透明、永远置顶且不干扰鼠标穿透（针对非边界区域）的动态字幕悬浮窗。提供保留历史上下文锚点的精美暗色排版。

### 硬件要求
*   **最低配置：** 8GB 内存，现代多核 CPU（Int8 推理模式）。
*   **推荐配置：** 拥有 6GB 及以上显存的 NVIDIA 显卡（如 RTX 3060 / RTX 4060），可充分利用 CUDA + float16 达成极速推理。

### 模型选择和模型保存位置
模型在初次启动时会自动下载：
*   **Whisper 语音模型默认存储位置：** `C:\Users\<您的用户名>\.cache\huggingface\hub\`
*   **ArgosTranslate 翻译模型默认存储位置：** `C:\Users\<您的用户名>\.local\share\argos-translate\packages\`

**Whisper 各路模型详细参数与性能对比：**
| 模型名称 | 参数量 | 相对推理速度 | 显存/内存占用 | 准确度 | 适用场景及推荐 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **tiny** | 39 M | ~10x | ~1 GiB | 较低 | 极低配置设备 |
| **base** | 74 M | ~7x | ~1 GiB | 中等 | 基础轻量级任务 |
| **small** | 244 M | ~4x | ~2 GiB | 良好 | **默认推荐及平衡点** (适合 RTX 4060) |
| **medium** | 769 M | ~2x | ~5 GiB | 高 | 高精度要求 |
| **large-v3** | 1550 M | 1x | ~8 GiB | 极高 | 极致准确度和专业转录 |

### 安装指南
1. **环境准备：** Python 3.10+ (推荐 3.10.x)。系统中需要安装 `ffmpeg` 并配置系统环境变量（PATH）。
2. **下载源码：** 将项目拉取至本地。
3. **安装依赖环境：**
   ```bash
   pip install faster-whisper argostranslate PyQt6 PyAudioWPatch numpy
   ```
   *注意：为了开启 GPU CUDA 加速，需确保 NVIDIA 驱动已更新，并配置了对应的 CUDA Toolkit (11.x 或 12.x) 及 cuDNN。*

### 运行测试使用指南
1. 运行主程序：
   ```bash
   python desktop_app/main.py
   ```
2. **首次运行：** 程序会静默下载设定的 Whisper 模型和翻译所需字典文件，此时命令行和字幕会有相应提示，取决于您的网速，请耐心等待。
3. **正式使用：** 启动后，播放任意系统音频（如网页视频或会议软件），透明字幕框将实时抛出识别与翻译文字。
4. **自定义设置：** 使用附带的 "设置" 窗口实时切换语音模型（切换后立即下载/加载）、更改源语言、调节窗口透明度以及自适应缩放字幕框界面（将鼠标悬停在悬浮窗边缘即可拖拉大小）。

### 打包软件指南
如果需要对外发布免 Python 环境的独立可用版本，可使用 PyInstaller 打包：
1. **激活环境：** 确保你已经在命令行中激活了对应的虚拟环境（例如 `conda activate subtitle_env310`）。
2. **安装打包工具：**
   ```bash
   pip install pyinstaller
   ```
3. **执行打包指令（请在项目根目录运行）：**
   ```bash
   pyinstaller --name "WhisperScribePro" --noconfirm --onedir --windowed --add-data "C:\Users\ljz\.conda\envs\subtitle_env310\Lib\site-packages\faster_whisper\assets;faster_whisper/assets" desktop_app\main.py
   ```
   
**打包逻辑与模型说明（避坑指南）：**
*   **为何必须带 `--add-data` 参数？** 基础的打包指令（如以前给过的通用版本）无法让 PyInstaller 识别到 `faster-whisper` 底层的静态资产文件（例如静音检测 VAD 需要的 `silero_vad.onnx`）。如果不使用该参数将它们显式拷贝进去，打包出的 exe 运行到识别那一步绝对会崩溃。
*   **关于 Conda 环境抓取：** 你不需要手动去设定 python 环境引擎在哪里。只要你在带有 `(subtitle_env310)` 前缀的命令行终端下运行上述命令，PyInstaller 就会自动扫描并把这个环境里所有用到的第三方库完整打包进去。
*   **关于 AI 模型提取（重要）：千万不要去打包存放在 C 盘中达到数个 GB 大小的模型文件！** 我们的代码中已经写好了“初次使用自动下载模型且验证文件完整”的功能。将打包出来的软件发送给他人使用时，对方首次打开软件就会自动拉取并在后台把网络模型下载到他们自己电脑的 C 盘对应位置中去。强行把几十 GB 塞进安装包中会导致打包时间崩溃且分享极其繁琐。

---

<a name="日本語"></a>
## 日本語

### はじめに
WhisperScribe Pro は、安全かつ完全にローカルで動作するリアルタイム音声認識・翻訳デスクトップアプリケーションです。WASAPI Loopback 経由でシステム音声をキャプチャし、`faster-whisper` でローカル文字起こしを実行、`argostranslate` を用いてオフラインで翻訳を行います。

### 技術実装とアーキテクチャ
*   **音声キャプチャ:** `PyAudioWPatch` を使用し、仮想オーディオケーブル不要で Windows のスピーカー出力を WASAPI Loopback 経由で直接取得します。
*   **音声認識 (ASR):** CTranslate2 に最適化された `faster-whisper` をコアエンジンに採用。独自のスライディングウィンドウバッファと動的 VAD (音声アクティビティ検出) を組み合わせ、ミリ秒単位のフィードバックを提供しつつ、無音部分を排除して AI が引き起こす「幻覚 (Hallucination)」を防ぎます。
*   **オフライン翻訳:** `argostranslate` を統合。一部の言語ペアではピボット翻訳 (Pivot Translation, 例: `ja -> en -> zh`) を採用し、直接翻訳時のエラーや精度低下を回避しています。
*   **GUI インターフェース:** `PyQt6` をベースに構築。ボーダーレス、半透明背景、常に最前面表示の設定を備えた字幕ウィンドウを提供します。最新の認識・翻訳テキストを強調し、過去の文章をコンテキストアンカーとして暗めに表示する、美しいダークテーマの UI です。

### システム要件 (ハードウェア要件)
*   **最小要件:** 8GB RAM, 最新のマルチコア CPU (Int8 推論モードで動作)。
*   **推奨要件:** 6GB 以上の VRAM を搭載した NVIDIA GPU (例: RTX 3060 / RTX 4060 以上)。CUDA + float16 アクセラレーションによる超高速推論を実現。

### モデルの選択と保存場所
AI モデルは初回起動時に自動的にローカルにダウンロードされます。
*   **Whisper モデルのデフォルト保存先:** `C:\Users\<システムのユーザー名>\.cache\huggingface\hub\`
*   **ArgosTranslate 翻訳モデルのデフォルト保存先:** `C:\Users\<システムのユーザー名>\.local\share\argos-translate\packages\`

**Whisper 各モデルの詳細パラメータとパフォーマンス比較:**
| モデル名 | パラメータ数 | 相対推論速度 | VRAM/RAM 使用量 | 精度 | 適用シーンと推奨 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **tiny** | 39 M | ~10x | ~1 GiB | 低 | 低スペックデバイス用 |
| **base** | 74 M | ~7x | ~1 GiB | 中 | 基本的なタスク |
| **small** | 244 M | ~4x | ~2 GiB | 良好 | **デフォルト推奨 (RTX 4060 等に最適)** |
| **medium** | 769 M | ~2x | ~5 GiB | 高 | 高精度が求められる場合 |
| **large-v3** | 1550 M | 1x | ~8 GiB | 非常に高 | 究極の精度や専門的な文字起こし |

### インストールガイド
1. **環境の準備:** Python 3.10+ (3.10.x を推奨)。システムに `ffmpeg` をインストールし、環境変数 PATH に追加する必要があります。
2. **ソースコードのダウンロード:** リポジトリをローカルにクローンまたはダウンロードします。
3. **依存パッケージのインストール:**
   ```bash
   pip install faster-whisper argostranslate PyQt6 PyAudioWPatch numpy
   ```
   *注意: GPU CUDA アクセラレーションを有効にするには、NVIDIA ドライバが最新であること、および対応する CUDA Toolkit (11.x または 12.x) と cuDNN が適切にインストールされていることを確認してください。*

### 実行とテストの使用ガイド
1. メインプログラムの実行:
   ```bash
   python desktop_app/main.py
   ```
2. **初回起動:** 設定された Whisper モデルと翻訳用の辞書ファイルがバックグラウンドでダウンロードされます。ネットワーク速度によっては時間がかかる場合がありますので、プロンプトを確認しつつお待ちください。
3. **通常使用:** 起動後、システムの任意の音声 (ブラウザの動画や Web 会議など) を再生すると、透明な字幕ウィンドウにリアルタイムで文字起こしと翻訳テキストが表示されます。
4. **カスタマイズ設定:** 付属の「設定」ウィンドウを使用して、音声モデルの切り替え (切り替え後に自動ダウンロード/ロード)、入力言語の変更、ウィンドウの透明度の調整、字幕 UI サイズの変更 (字幕ウィンドウの端をドラッグしてサイズ変更) をリアルタイムに行うことができます。

### ソフトウェアパッケージ化ガイド
Python 環境を持たないユーザー向けにスタンドアロンの実行可能ファイル (exe) として配布する場合は、`PyInstaller` を使用します。
1. **環境のアクティベート:** Python 仮想環境がアクティブであることを確認します（例：Anaconda 環境 `subtitle_env310`）。
2. **パッケージ化ツールのインストール:**
   ```bash
   pip install pyinstaller
   ```
3. **正確なパッケージ化コマンドの実行（プロジェクトのルートで実行）:**
   ```bash
   pyinstaller --name "WhisperScribePro" --noconfirm --onedir --windowed --add-data "C:\Users\ljz\.conda\envs\subtitle_env310\Lib\site-packages\faster_whisper\assets;faster_whisper/assets" desktop_app\main.py
   ```
   
**パッケージ化における重要かつ注意すべき概念：**
*   **なぜ `--add-data` が必要なのか？** 一般的なパッケージ化コマンドだけでは、`faster_whisper` に必要な内部のアセット（VADモデルなど）が除外され、エラーで動作しなくなります。これを防ぐためにパスを明示的にマッピングしています。
*   **Anaconda 環境について:** アクティブ化された環境で `pyinstaller` を実行するだけで、コンパイラは関連する全てのPython依存関係を自動的に収集してバンドルします。
*   **AI モデルはバンドルしないこと：** CドライブのキャッシュにダウンロードされたGB単位の Whisper / ArgosTranslate モデルを exe 内にパックすることは強く推奨されません。アプリには初回起動時の自動ダウンロードロジックが組み込まれています。そのため、そのまま配布すれば、ユーザーが初めて起動した際に各々の PC にモデルが自動で取得・配置され、不必要に巨大なアプリファイルを避けることができます。
