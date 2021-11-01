import tkinter as tk
from tkinter import messagebox
from nhentai_download import nhentai_download
from PIL import Image, ImageTk

# THREAD = 16
FONT = ('微軟正黑體', 16)

nhentai = nhentai_download()
# init
window = tk.Tk()
window.title('nhentai download')
window.geometry('1200x800')


def preview_event():
    sixnum = sixnum_var.get()
    if sixnum == '':
        pass
    else:
        nhentai.set_sixnum(sixnum)
        info = nhentai.info()

        lb_lauthor = tk.Label(window, text='作者:', font=FONT)
        lb_lauthor.grid(row=4, column=0, sticky='W', columnspan=2)
        lb_author = tk.Label(window, text=info['author'], font=FONT)
        lb_author.grid(row=5, column=0, sticky='W', columnspan=2)

        lb_ltitle = tk.Label(window, text='標題', font=FONT)
        lb_ltitle.grid(row=6, column=0, sticky='W', columnspan=2)
        lb_title = tk.Label(window, text=info['title'], font=FONT)
        lb_title.grid(row=7, column=0, sticky='W', columnspan=2)

        lb_lotherinfo = tk.Label(window, text='其他資訊:', font=FONT)
        lb_lotherinfo.grid(row=8, column=0, sticky='W', columnspan=2)
        lb_otherinfo = tk.Label(window, text=info['other'], font=FONT)
        lb_otherinfo.grid(row=9, column=0, sticky='W', columnspan=2)

        lb_totalpages = tk.Label(window, text='總頁數:' +
                                 info['pages']+'p', font=FONT)
        lb_totalpages.grid(row=10, column=0, sticky='W', columnspan=3)

        cover_image = nhentai.show_cover()
        img = ImageTk.PhotoImage(cover_image.resize((600, 800)))
        image = tk.Canvas(window, width=600, height=800, bg='white')
        image.place(x=600, y=0)
        image.create_image(0, 0, anchor=tk.NW, image=img)

        window.mainloop()


def dlpdf_event():
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
    messagebox.showinfo('nhentai download', '下載完成!')


# labels and entries
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

# bottom
button_preview = tk.Button(window, text='預覽', font=FONT, command=preview_event)
button_preview.grid(row=3, column=0)

button_dlpdf = tk.Button(window, text='下載PDF',
                         font=FONT, command=dlpdf_event)
button_dlpdf.grid(row=3, column=1)

button_dlimg = tk.Button(window, text='下載圖片', font=FONT, command=dlimg_event)
button_dlimg.grid(row=3, column=2)
# show
window.mainloop()
