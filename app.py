import streamlit as st
import yt_dlp
import os

st.title("📺 YouTube Downloader Web")

# 1. URL入力
url = st.text_input("YouTubeのURLを入力してください")

# 2. 設定（音声のみか動画か選べるように進化！）
option = st.selectbox("形式を選択", ["動画 (MP4)", "音声のみ (MP3)"])

# 3. ダウンロードボタン
if st.button("ダウンロード開始"):
    if not url:
        st.warning("URLを入力してください")
    else:
        # 進行状況を表示するエリア
        status_text = st.empty()
        status_text.text("処理中...")
        
        # 保存先（一時的に現在のフォルダ）
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }
        
        if option == "音声のみ (MP3)":
            ydl_opts['format'] = 'bestaudio/best'
            # MP3変換等の設定はffmpegが必要なため、今回は簡易的にm4a等で保存されます
        else:
            ydl_opts['format'] = 'best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            st.success(f"完了！ファイル名: {filename}")
            st.balloons() # お祝いのエフェクト

            # Web上でファイルをダウンロードさせるボタンを表示
            with open(filename, "rb") as file:
                btn = st.download_button(
                    label="ファイルをPCに保存する",
                    data=file,
                    file_name=filename,
                    mime="application/octet-stream"
                )

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")