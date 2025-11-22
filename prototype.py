import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os

# --- ロジック部分（ダウンロードの処理） ---
def download_video():
    url = entry_url.get() # 入力欄からURLを取得
    
    if not url:
        messagebox.showwarning("注意", "URLを入力してください")
        return

    # 保存先を現在のフォルダに設定
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s', # ファイル名を「動画タイトル.拡張子」にする
        'format': 'best',               # 一番良い画質を選ぶ
    }

    status_label.config(text="ダウンロード中...お待ちください")
    root.update() # 画面の表示を更新

    try:
        # yt-dlpを使ってダウンロード実行
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("完了", "ダウンロードに成功しました！")
        status_label.config(text="待機中")
        entry_url.delete(0, tk.END) # 入力欄をクリア

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")
        status_label.config(text="エラー発生")

# --- GUI部分（見た目の作成） ---
root = tk.Tk()
root.title("My YouTube Downloader")
root.geometry("400x200") # 画面サイズ

# 1. 案内ラベル
label = tk.Label(root, text="YouTubeのURLを入力してください:")
label.pack(pady=10)

# 2. 入力欄
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

# 3. 実行ボタン
# command=download_video で、ボタンを押した時に上の関数を実行するよう紐付けます
btn_download = tk.Button(root, text="ダウンロード開始", command=download_video)
btn_download.pack(pady=20)

# 4. 状態表示ラベル
status_label = tk.Label(root, text="待機中", fg="gray")
status_label.pack(pady=5)

# アプリを起動し続ける
root.mainloop()