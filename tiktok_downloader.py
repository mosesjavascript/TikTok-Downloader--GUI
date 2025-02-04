import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
from ttkthemes import ThemedTk
import ttkbootstrap as ttk
import os

def download_video():
    url = entry_url.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a TikTok video URL")
        return
    
    save_path = filedialog.askdirectory()
    if not save_path:
        return
    
    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]',  # Ensures best video and audio quality
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

# GUI Setup
root = ThemedTk(theme="breeze")
root.title("TikTok Video Downloader")
root.geometry("450x250")
root.resizable(False, False)

# Set icon
icon_path = "clock.ico"  # Update this with the correct path to your icon file
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)



ttk.Label(frame, text="Enter TikTok Video URL:", font=("Arial", 12)).pack(pady=5)
entry_url = ttk.Entry(frame, width=55, font=("Arial", 10))
entry_url.pack(pady=5)

download_btn = ttk.Button(frame, text="Download Video", command=download_video, bootstyle="primary")
download_btn.pack(pady=10)

root.mainloop()
