from gtts import gTTS
import os

# 定义要转换的文本和语言
text = "今天是个好天气"
language = 'zh-CN'  # 对于中文设置为'zh-CN'

# 创建gTTS对象
my_tts = gTTS(text=text, lang=language)
# 保存语音文件
my_tts.save("output.mp3")
