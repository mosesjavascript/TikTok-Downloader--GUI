import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

def download_video():
    url = entry_url.get()
    if not url:
        messagebox.showerror("Error", "Please enter a TikTok video URL")
        return
    
    save_path = filedialog.askdirectory()
    if not save_path:
        return
    
    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'best'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

# GUI Setup
root = tk.Tk()
root.title("TikTok Video Downloader")
root.geometry("400x200")

tk.Label(root, text="Enter TikTok Video URL:").pack(pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

download_btn = tk.Button(root, text="Download Video", command=download_video)
download_btn.pack(pady=5)

root.mainloop()
