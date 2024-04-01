import tkinter
import requests
import re

# 获取单词翻译数据
def fetch_translation(word):
    url = "https://fanyi.baidu.com/sug"
    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
    }
    data = {'kw': word}
    response = requests.post(url=url, data=data, headers=headers)
    if response.status_code == 200:
        translation_data = response.json().get('data', [])
        return translation_data
    else:
        return []

# 清空文本框
def clear_text_widgets():
    text1.delete(1.0, tkinter.END)
    text2.delete(1.0, tkinter.END)

# 显示翻译结果
def display_translation(translation_data):
    if not translation_data:
        text1.insert(tkinter.INSERT, "未找到翻译结果。\n")
        return
    primary_translation = translation_data[0]
    text1.insert(tkinter.INSERT, f"{primary_translation['k']}\n{primary_translation['v']}\n\n")
    for item in translation_data[1:]:
        text2.insert(tkinter.INSERT, f"{item['k']}:\n{item['v']}\n\n")

# 检查用户输入是否符合规范
def validate_input(word):
    if not word:
        return False
    pattern = r'^[\u4e00-\u9fa5a-zA-Z]+$'  # 只包含中文或英文字母
    return re.match(pattern, word)

# 开始翻译
def start_translation():
    global count
    word = entry_word.get().strip()  # 获取输入的单词，并去除首尾空格
    if not validate_input(word):
        clear_text_widgets()
        text1.insert(tkinter.INSERT, "请输入只包含中文或英文字母的单词。\n")
        return
    clear_text_widgets()     # 清空文本框
    translation_data = fetch_translation(word)  # 获取翻译数据
    display_translation(translation_data)       # 显示翻译结果
    count += 1

# 创建主窗口
win = tkinter.Tk()
win.title('小小翻译')
win.geometry('400x360+300+300')

count = 0  # 计数器

# 创建标签、输入框、按钮和文本框
label1 = tkinter.Label(win, text='输入单词')
label1.grid(row=1, column=0)
entry_word = tkinter.Entry(win, width=20)
entry_word.grid(row=1, column=1)
button = tkinter.Button(win, text="翻译", command=start_translation)
button.grid(row=1, column=2)
label2 = tkinter.Label(win, text='翻译结果')
label2.grid(row=3, column=0)
b = tkinter.Label(win, text="\n")
b.grid(row=4, column=1)
text1 = tkinter.Text(win, height=5, width=40)
label3 = tkinter.Label(win, text='类似单词')
label3.grid(row=5, column=0)
text2 = tkinter.Text(win, height=15, width=40)
text1.grid(row=3, column=1)
text2.grid(row=5, column=1)

win.mainloop()
