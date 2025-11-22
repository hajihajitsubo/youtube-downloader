import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import threading

# --- ロジック部分 ---
def start_download_thread():
    # ダウンロードは時間がかかるので、別のスレッド（担当者）に任せる
    # これをしないと、ダウンロード中に画面がフリーズしてしまいます
    thread = threading.Thread(target=download_video)
    thread.start()

def progress_hook(d):
    # yt-dlpから定期的に呼び出される関数（進捗状況の報告）
    if d['status'] == 'downloading':
        # パーセントを取得（例: "35.5%"）
        p = d.get('_percent_str', '0%').replace('%','')
        try:
            value = float(p)
            progress_bar['value'] = value # バーの長さを更新
            status_label.config(text=f"ダウンロード中... {value}%")
        except:
            pass
    elif d['status'] == 'finished':
        status_label.config(text="変換処理中...")
        progress_bar['value'] = 100

def download_video():
    url = entry_url.get()
    save_dir = entry_dir.get()

    if not url:
        messagebox.showwarning("注意", "URLを入力してください")
        return
    if not save_dir:
        messagebox.showwarning("注意", "保存先フォルダを選択してください")
        return

    # ボタンを一時的に押せないようにする（連打防止）
    btn_download.config(state=tk.DISABLED)
    
    # yt-dlpの設定
    ydl_opts = {
        'outtmpl': f'{save_dir}/%(title)s.%(ext)s', # 選択したフォルダに保存
        'format': 'best',
        'noplaylist':True,
        'progress_hooks': [progress_hook], # 進捗を報告させる設定
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("完了", "ダウンロードに成功しました！")
        status_label.config(text="完了")
        entry_url.delete(0, tk.END)
        progress_bar['value'] = 0

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")
        status_label.config(text="エラー発生")
    
    finally:
        # 終わったらボタンをまた押せるように戻す
        btn_download.config(state=tk.NORMAL)

def select_folder():
    # フォルダ選択ダイアログを開く
    path = filedialog.askdirectory()
    if path:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, path)

# --- GUI部分 ---
root = tk.Tk()
root.title("My YouTube Downloader v2")
root.geometry("500x300")

# 1. URL入力エリア
frame_url = tk.Frame(root)
frame_url.pack(pady=10)
tk.Label(frame_url, text="URL:").pack(side=tk.LEFT)
entry_url = tk.Entry(frame_url, width=40)
entry_url.pack(side=tk.LEFT, padx=5)

# 2. 保存先選択エリア
frame_dir = tk.Frame(root)
frame_dir.pack(pady=5)
tk.Label(frame_dir, text="保存先:").pack(side=tk.LEFT)
entry_dir = tk.Entry(frame_dir, width=30)
entry_dir.pack(side=tk.LEFT, padx=5)
# デスクトップなどをデフォルトに入れておくことも可能
entry_dir.insert(0, ".") 
btn_dir = tk.Button(frame_dir, text="参照", command=select_folder)
btn_dir.pack(side=tk.LEFT)

# 3. 実行ボタン（start_download_threadを呼ぶように変更）
btn_download = tk.Button(root, text="ダウンロード開始", command=start_download_thread, bg="#dddddd")
btn_download.pack(pady=20)

# 4. 進捗バー（新機能！）
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# 5. 状態表示
status_label = tk.Label(root, text="待機中", fg="gray")
status_label.pack(pady=5)

root.mainloop()