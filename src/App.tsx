import React from 'react';
import { 
  Terminal, Package, Download, HardDrive, 
  Cpu, Music, Subtitles, Settings, Layers
} from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-[#0B0C0E] text-slate-200 font-sans selection:bg-blue-500/30">
      <div className="max-w-4xl mx-auto px-6 py-12">
        <header className="mb-12 border-b border-slate-700/50 pb-8">
          <h1 className="text-4xl font-bold text-white mb-4 tracking-tight flex items-center gap-3">
            <Subtitles className="text-blue-500" size={36} />
            实时字幕 Windows 桌面应用
          </h1>
          <p className="text-slate-400 text-lg leading-relaxed">
            根据您的需求，我们已经为您构建了一个基于 <span className="text-blue-400">faster-whisper</span> 和 <span className="text-blue-400">PyQt6</span> 的本地纯离线实时字幕软件。
            该软件专门针对您的环境 (Windows 11, i9-12900HX, RTX 4060) 进行了架构设计。您可以将其打包为独立的 `.exe` 程序。
          </p>
        </header>

        <main className="space-y-10">
          {/* Tech Stack section */}
          <section>
            <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
              <Layers className="text-blue-500" />
              实现的技术路线
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-[#18191D] border border-slate-700/50 shadow-lg p-5 rounded-xl">
                <h3 className="text-lg font-medium text-white mb-2 flex items-center gap-2">
                  <Music size={18} className="text-blue-500"/> 音频捕获 (WASAPI Loopback)
                </h3>
                <p className="text-sm text-slate-400">
                  使用 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">PyAudioWPatch</code> 捕获 Windows 扬声器的底层输出流。无需虚拟声卡即可读取任何软件（会议软件、浏览器）的声音。
                </p>
              </div>
              
              <div className="bg-[#18191D] border border-slate-700/50 shadow-lg p-5 rounded-xl">
                <h3 className="text-lg font-medium text-white mb-2 flex items-center gap-2">
                  <Cpu size={18} className="text-blue-500" /> 语音识别 (ASR)
                </h3>
                <p className="text-sm text-slate-400">
                  结合 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">faster-whisper</code> 与 CTranslate2。通过累积式 Buffer 与 <strong className="text-slate-200">动态 VAD 静音检测</strong> 杜绝模型“幻觉”与闪烁错误，并扩大了推理的上下文长度以提升单句识别正确率。
                </p>
              </div>

              <div className="bg-[#18191D] border border-slate-700/50 shadow-lg p-5 rounded-xl">
                <h3 className="text-lg font-medium text-white mb-2 flex items-center gap-2">
                  <HardDrive size={18} className="text-blue-500"/> 桥接离线翻译 (Pivot)
                </h3>
                <p className="text-sm text-slate-400">
                  选用 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">argostranslate</code>。针对日语转中文加入了 <strong className="text-slate-200">ja-&gt;en-&gt;zh</strong> 智能内桥接，彻底解决直接调用报错且无翻译返回的问题，全部在本地即刻完成转换。
                </p>
              </div>

              <div className="bg-[#18191D] border border-slate-700/50 shadow-lg p-5 rounded-xl">
                <h3 className="text-lg font-medium text-white mb-2 flex items-center gap-2">
                  <Settings size={18} className="text-blue-500"/> UI 框架 (PyQt6)
                </h3>
                <p className="text-sm text-slate-400">
                  使用 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">PyQt6</code> 构建字幕与设置两个独立窗口。利用无边框 (Frameless) 与 WA_TranslucentBackground 属性实现半透明悬浮字幕，通过重写鼠标事件完成任意尺寸拖动调整。
                </p>
              </div>
            </div>
          </section>

          {/* Deployment section */}
          <section>
            <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
              <Download className="text-blue-500" />
              如何导出与部署到本地使用
            </h2>
            
            <div className="bg-[#18191D] border border-slate-700/50 shadow-lg rounded-xl overflow-hidden">
              <div className="p-6 border-b border-slate-700/50">
                <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                  <span className="flex items-center justify-center bg-blue-500/20 text-blue-400 w-6 h-6 rounded-full text-xs font-bold shadow-[0_0_8px_rgba(59,130,246,0.5)]">1</span>
                  下载代码
                </h3>
                <p className="text-sm text-slate-400">
                  在 Google AI Studio 界面右上角，依次点击 <strong className="text-slate-200">选项 (三点菜单) &gt; Export &gt; Download ZIP</strong>。
                  解压后进入内部的 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">desktop_app</code> 文件夹。
                </p>
              </div>

              <div className="p-6 border-b border-slate-700/50">
                <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                  <span className="flex items-center justify-center bg-blue-500/20 text-blue-400 w-6 h-6 rounded-full text-xs font-bold shadow-[0_0_8px_rgba(59,130,246,0.5)]">2</span>
                  安装 Anaconda 与依赖环境
                </h3>
                <p className="text-sm text-slate-400 mb-3">
                  推荐使用 <strong className="text-slate-200">Anaconda</strong> 创建 <strong className="text-blue-400">Python 3.10</strong> 虚拟环境。确保您的电脑已安装 NVIDIA 显卡驱动以及 CUDA 12 Toolkit 与 cuDNN 8+，以便 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">faster-whisper</code> 在 GPU 上加速。
                </p>
                <div className="bg-[#0B0C0E] p-4 rounded-md font-mono text-xs text-blue-300 overflow-x-auto border border-slate-800 shadow-inner">
                  # 打开 Anaconda Prompt<br />
                  conda create -n subtitle_env python=3.10 -y<br />
                  conda activate subtitle_env<br />
                  <br />
                  # 进入 desktop_app 目录<br />
                  cd desktop_app<br />
                  <br />
                  # 安装所有依赖工具<br />
                  pip install -r requirements.txt
                </div>
              </div>

              <div className="p-6 border-b border-slate-700/50">
                <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                  <span className="flex items-center justify-center bg-blue-500/20 text-blue-400 w-6 h-6 rounded-full text-xs font-bold shadow-[0_0_8px_rgba(59,130,246,0.5)]">3</span>
                  运行测试
                </h3>
                <div className="bg-[#0B0C0E] p-4 rounded-md font-mono text-xs text-blue-300 overflow-x-auto border border-slate-800 shadow-inner">
                  python main.py
                </div>
                <p className="text-sm text-slate-400 mt-3">
                  首次运行时会自动下载 Whisper (Small) 模型和本地翻译语言包，需要一定时间。模型下载完成后，播放任何音频/视频，字幕框就会显示内容。您可以拖动字幕边缘调整大小。
                </p>
              </div>

              <div className="p-6">
                <h3 className="text-white font-medium mb-3 flex items-center gap-2">
                  <span className="flex items-center justify-center bg-blue-500/20 text-blue-400 w-6 h-6 rounded-full text-xs font-bold shadow-[0_0_8px_rgba(59,130,246,0.5)]">4</span>
                  使用 PyInstaller 打包为独立软件 (.exe)
                </h3>
                <p className="text-sm text-slate-400 mb-3">
                  当环境配置完成且能够成功运行后，将其打包为可以双击打开的 Windows 可执行文件。
                </p>
                <div className="bg-[#0B0C0E] p-4 rounded-md font-mono text-xs text-blue-300 overflow-x-auto border border-slate-800 shadow-inner">
                  pyinstaller --name "RealTimeSubtitle" --noconsole --onedir main.py
                </div>
                <p className="text-sm text-slate-400 mt-3">
                  <strong className="text-blue-400">注：</strong> CTranslate2 和 PyTorch 的体积很大。使用 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">--onedir</code>（默认就是目录模式）比打包成单文件 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">--onefile</code> 启动快得多。
                  打包后，<code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">dist/RealTimeSubtitle</code> 目录中会包含 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">RealTimeSubtitle.exe</code>。由于使用了外部模型，您可能需要手动将 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">huggingface</code> 的模型缓存或 <code className="text-slate-300 bg-[#23252B] px-1 py-0.5 rounded border border-slate-700/30">argostranslate</code> 的缓存复制到程序所在的目录周围（若要在其他电脑上使用）。
                </p>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
