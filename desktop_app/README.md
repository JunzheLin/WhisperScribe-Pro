# 实时字幕 Windows 桌面应用 (Real-Time Subtitle)

基于 `faster-whisper` (CTranslate2) 和 `PyQt6` 的本地纯离线实时音频识别与翻译透明字幕工具。

## 🛠️ 技术路线

*   **音频捕获 (WASAPI Loopback):**
    使用 `PyAudioWPatch` 捕获 Windows 扬声器的底层输出流。无需虚拟声卡即可读取任何应用（会议软件、浏览器、系统提示音）的声音。
*   **连续推断机制与动态 VAD:**
    通过设置滑动音频缓冲区积累语音，结合 `faster-whisper` 的内建 VAD 功能 (`vad_filter=True`)，自动滤除静音以防止模型产生“幻觉”(重复上一句无意义的话)。当语音间断时间超过阈值(1秒)时，算法会自动切断缓冲区将其定型存入历史。这平衡了“上下文不够导致翻译荒谬”与“等待时间太长导致高延迟”两大矛盾。
*   **枢纽翻译 (Pivot Translation):**
    考虑到离线模型 `argostranslate` 并未大量提供直接的日转中 (ja->zh) 连结字典，应用采用桥接架构，后台安装 [ja->en] 与 [en->zh] 两套模型，系统底层会在极短时间内通过英语做桥梁完成高质量的中文转换，不漏译不报错。
*   **暗色历史字幕流动流:**
    字幕悬辅窗采用文本编辑器结构，最新的内容为高亮原色显示，往期识别到的最后三句会自动透明度减弱成为上下文锚点，帮助使用者串联整个对话的含义。并且支持随意调整宽高实现字数拓展或换行。

---

## ⚙️ 环境要求

*   **操作系统:** Windows 10 / Windows 11
*   **显卡:** NVIDIA 显卡 (例如 RTX 4060)
*   **驱动环境:** 
    *   已安装最新的 NVIDIA 显卡驱动
    *   [CUDA Toolkit 12.x](https://developer.nvidia.com/cuda-downloads)
    *   [cuDNN 8.x 或 9.x](https://developer.nvidia.com/cudnn) (如果不配置 cuDNN，faster-whisper 的 GPU 加速可能会受限，回退到 CPU)
*   **环境管理工具:** 推荐使用 [Anaconda](https://www.anaconda.com/download/) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

---

## 🚀 Anaconda 安装与配置指南

我们强烈推荐您使用 Anaconda 来独立管理 Python 环境，这能最大程度防止项目间的依赖冲突，方便管理 CTranslate2/PyTorch 等底层编译库。推荐使用 **Python 3.10**，这是目前与各类 AI 库与 PyQT6 兼容性最稳定的版本。

### 1. 下载并安装 Anaconda
如果您尚未安装 Anaconda（或 Miniconda），请前往官网下载并依照默认提示将其安装在您的电脑上。确保在安装时选择“将 Anaconda 添加到环境变量”，或者习惯使用附带的 `Anaconda Prompt`。

### 2. 创建并激活 Conda 虚拟环境
打开终端（推荐使用 `Anaconda Prompt` 或 Windows PowerShell），执行以下命令：

```bash
# 创建一个名为 subtitle_env 的虚拟环境，并明确指定 Python 版本为 3.10
conda create -n subtitle_env python=3.10 -y

# 激活刚刚创建的虚拟环境
conda activate subtitle_env
```

### 3. 进入项目目录并安装依赖
在终端中，使用 `cd` 命令切换到您解压出来的 `desktop_app` 文件夹中：

```bash
# 请将下面路径替换为您实际解压的 desktop_app 文件夹所在绝对路径或相对路径
cd 您的路径/desktop_app

# 安装所需的所有 Python 依赖包 (在激活的 conda 环境中使用 pip 安装非常安全且有效)
pip install -r requirements.txt
```

---

## 🎧 运行与使用测试

**步骤 1:** 确保您已经激活了环境 (`conda activate subtitle_env`)，并在 `desktop_app` 目录下执行：

```bash
python main.py
```

**步骤 2:** 
*   **初始化下载:** 首次运行时，程序会自动在后台请求下载 `faster-whisper` 的中小型模型 (Small) 和本地翻译包，这需要几分钟时间（取决于您的网络），请耐心观察终端中的提示。
*   **开始使用:** 待初始化完成后，字幕窗口显示 "等待语音输入..."。此时，您可以播放包含日语或英语的媒体音频。系统扬声器产生声波后，程序会飞速识别并在半透明窗口上层出中英/中日双语字幕。

---

## 📦 如何使用 Pyinstaller 打包为独立软件 (.exe)

当环境配置完成并在本地测试能够成功运行后，您可以使用 Pyinstaller 将其打包为可以脱离 Python 环境运行的独立 Windows 可执行文件。

在已激活的 conda 环境与 `desktop_app` 文件夹中执行：

```bash
# 推荐打包为大家喜闻乐见的文件夹结构模式 (相比单文件模式，启动快得多)
pyinstaller --name "RealTimeSubtitle" --noconsole --onedir main.py
```

*   打包完成后，前往 `desktop_app/dist/RealTimeSubtitle/` 目录，您会看到 `RealTimeSubtitle.exe`，双击即可无控制台黑框运行。
*   **💡 特别提示:** 由于本地部署的 AI 模型默认缓存于用户的 `~/.cache/huggingface/` 以及 `~/.local/share/argos-translate/` 等路径，虽然您打包成了 exe，但若将其放到另一台【彻头彻尾没有网络】的电脑上，可能会因为找不到对应的模型二进制文件而无法启动。\n如果希望做成真正纯净、即拷即用的“绿色版”，可考虑在代码中锁定 `.cache` 路径至程序根目录，然后连同下载好的模型一道分发给他人阅读。
