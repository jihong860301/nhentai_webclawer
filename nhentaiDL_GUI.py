import tkinter as tk
from tkinter import messagebox
from nhentai_download import nhentai_download
from PIL import Image, ImageTk

# 設定常數
FONT = ('微軟正黑體', 16)
WINDOW_SIZE = '1200x800'
TITLE = 'nhentai download'
# 如果下載路徑未設定，預設為與程式同資料夾
# 如果六位數未設定，預設為按下預覽與下載皆不會有事情發生
# 如果執行數未設定，預設為16

# 初始化
nhentai = nhentai_download()

window = tk.Tk()
window.title(TITLE)
window.geometry(WINDOW_SIZE)

authorVar = tk.StringVar()
titleVar = tk.StringVar()
otherinfoVar = tk.StringVar()
pageVar = tk.StringVar()


def preview_event():
    # 預覽事件，按下預覽按鈕後發生的事情
    # 1.下載本子的基本資料
    # 2.顯示基本資料在GUI上
    # 3.下載封面圖片
    # 4.顯示在GUI右半側
    sixnum = sixnum_var.get()
    if sixnum == '':
        pass
    else:
        nhentai.set_sixnum(sixnum)
        info = nhentai.info()

        authorVar.set(info['author'])
        titleVar.set(info['title'].replace('-','\n'))
        otherinfoVar.set(info['other'])
        pageVar.set(info['pages']+'p')

        cover_image = nhentai.show_cover()
        cover_image = image_resize(cover_image)
        y_pos = (800-cover_image.size[1])/2
        img = ImageTk.PhotoImage(cover_image)
        image = tk.Canvas(window, width=600, height=800, bg='white')
        image.place(x=600, y=0)
        image.create_image(0, y_pos, anchor=tk.NW, image=img)

        window.mainloop()


def dlpdf_event():
    # 下載PDF事件，在按下"下載PDF"後發生
    # 六位數未設定的情況下不會有任何事發生
    # 如果下載路徑與執行序數未設定皆為預設
    # 下載完成跳出視窗提醒
    sixnum = sixnum_var.get()
    dlpath = dlpath_var.get()
    threads = thread_var.get()
    if not sixnum == '':
        if not dlpath == '':
            nhentai.set_dldir(dlpath)
        if not threads == '':
            nhentai.set_threads(int(threads))
        nhentai.dlpdf()

        dlfinish_popwindow()


def dlimg_event():
    # 下載圖片事件，在按下"下載圖片"後發生
    # 六位數未設定的情況下不會有任何事發生
    # 如果下載路徑與執行序數未設定皆為預設
    # 下載完成跳出視窗提醒
    sixnum = sixnum_var.get()
    dlpath = dlpath_var.get()
    threads = thread_var.get()
    if not sixnum == '':
        if not dlpath == '':
            nhentai.set_dldir(dlpath)
        if not threads == '':
            nhentai.set_threads(int(threads))
        nhentai.dlimages()

        dlfinish_popwindow()


def dlfinish_popwindow():
    # 下載完成的提示視窗
    messagebox.showinfo('nhentai download', '下載完成!')


def image_resize(img):
    # 預覽圖片的大小重新塑形
    img = img.resize((600, int(img.size[1]*(600/img.size[0]))))
    return img


# 基本的版面配置(Label與Entry)
lb_path = tk.Label(window, text='下載路徑:',
                   font=FONT)
lb_path.grid(row=0, column=0, sticky='W')
dlpath_var = tk.StringVar()
entry_path = tk.Entry(window, textvariable=dlpath_var,
                      font=FONT)
entry_path.grid(row=0, column=1)

lb_sixnum = tk.Label(window, text='神秘六位數:',
                     font=FONT)
lb_sixnum.grid(row=1, column=0, sticky='W')
sixnum_var = tk.StringVar()
entry_sixnum = tk.Entry(window, textvariable=sixnum_var,
                        font=FONT)

entry_sixnum.grid(row=1, column=1)

lb_thread = tk.Label(window, text='執行序數:',
                     font=FONT)
lb_thread.grid(row=2, column=0, sticky='W')
thread_var = tk.StringVar()
entry_thread = tk.Entry(window, textvariable=thread_var,
                        font=FONT)
entry_thread.grid(row=2, column=1)

# 按鈕配置
button_preview = tk.Button(window, text='預覽', font=FONT, command=preview_event)
button_preview.grid(row=3, column=0)

button_dlpdf = tk.Button(window, text='下載PDF',
                         font=FONT, command=dlpdf_event)
button_dlpdf.grid(row=4, column=0)

button_dlimg = tk.Button(window, text='下載圖片', font=FONT, command=dlimg_event)
button_dlimg.grid(row=5, column=0)

# 作品資訊
lb_lauthor = tk.Label(window, text='作者:', font=FONT)
lb_lauthor.grid(row=6, column=0, sticky='W', columnspan=2)
lb_author = tk.Label(window, textvariable=authorVar, font=FONT)
lb_author.grid(row=7, column=0, sticky='W', columnspan=2)


lb_ltitle = tk.Label(window, text='標題', font=FONT)
lb_ltitle.grid(row=8, column=0, sticky='W', columnspan=2)
lb_title = tk.Label(window, textvariable=titleVar, font=FONT)
lb_title.grid(row=9, column=0, sticky='W', columnspan=2)


lb_lotherinfo = tk.Label(window, text='其他資訊:', font=FONT)
lb_lotherinfo.grid(row=10, column=0, sticky='W', columnspan=2)
lb_otherinfo = tk.Label(window, textvariable=otherinfoVar, font=FONT)
lb_otherinfo.grid(row=11, column=0, sticky='W', columnspan=2)

lb_ltotalpages = tk.Label(window, text='總頁數:', font=FONT)
lb_ltotalpages.grid(row=12, column=0, sticky='W', columnspan=2)
lb_otherinfo = tk.Label(window, textvariable=pageVar, font=FONT)
lb_otherinfo.grid(row=13, column=0, sticky='W', columnspan=2)


# 顯示於GUI上
window.mainloop()
