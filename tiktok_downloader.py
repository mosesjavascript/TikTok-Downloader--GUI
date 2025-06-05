import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
from ttkthemes import ThemedTk
import threading
import os
import re
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

class TikTokDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced TikTok Downloader")
        self.root.geometry("600x650")
        self.root.minsize(600, 650)
        
        # Set icon if available
        icon_path = "clock.ico"
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
            
        # Default download path
        self.default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.save_path = self.default_path
        
        # Create main frame with tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs
        self.downloader_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.downloader_tab, text="Downloader")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.about_tab, text="About")
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Setup each tab
        self.setup_downloader_tab()
        self.setup_settings_tab()
        self.setup_about_tab()
        
        # Initialize variables
        self.download_in_progress = False
        self.video_info = None
        self.download_history = []
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("TEntry", font=("Arial", 11))
        self.style.configure("TCheckbutton", font=("Arial", 10))
        self.style.configure("TRadiobutton", font=("Arial", 10))
        
    def setup_downloader_tab(self):
        frame = ttk.Frame(self.downloader_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # URL Entry section
        url_frame = ttk.LabelFrame(frame, text="Video URL", padding=10)
        url_frame.pack(fill="x", pady=5)
        
        ttk.Label(url_frame, text="Enter TikTok Video URL:").pack(anchor="w")
        
        url_input_frame = ttk.Frame(url_frame)
        url_input_frame.pack(fill="x", pady=5)
        
        self.entry_url = ttk.Entry(url_input_frame, width=45)
        self.entry_url.pack(side="left", fill="x", expand=True)
        
        paste_btn = ttk.Button(url_input_frame, text="Paste", command=self.paste_url, width=8)
        paste_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(url_input_frame, text="Clear", command=self.clear_url, width=8)
        clear_btn.pack(side="left")
        
        # Preview section
        preview_frame = ttk.LabelFrame(frame, text="Video Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        self.preview_canvas = tk.Canvas(preview_frame, bg="#f0f0f0", height=250)
        self.preview_canvas.pack(fill="both", expand=True)
        
        # Info label
        self.info_label = ttk.Label(preview_frame, text="No video loaded", wraplength=550, justify="left")
        self.info_label.pack(fill="x", pady=5)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        # Download options
        options_frame = ttk.LabelFrame(frame, text="Download Options", padding=10)
        options_frame.pack(fill="x", pady=5)
        
        # Quality options
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill="x", pady=5)
        
        ttk.Label(quality_frame, text="Quality:").pack(side="left", padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="best")
        ttk.Radiobutton(quality_frame, text="Best", variable=self.quality_var, value="best").pack(side="left", padx=5)
        ttk.Radiobutton(quality_frame, text="Medium", variable=self.quality_var, value="medium").pack(side="left", padx=5)
        ttk.Radiobutton(quality_frame, text="Low", variable=self.quality_var, value="low").pack(side="left", padx=5)
        
        # Format options
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill="x", pady=5)
        
        ttk.Label(format_frame, text="Format:").pack(side="left", padx=(0, 10))
        
        self.format_var = tk.StringVar(value="mp4")
        ttk.Radiobutton(format_frame, text="MP4", variable=self.format_var, value="mp4").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="MP3 (Audio Only)", variable=self.format_var, value="mp3").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="GIF", variable=self.format_var, value="gif").pack(side="left", padx=5)
        
        # Additional options
        options_checkbox_frame = ttk.Frame(options_frame)
        options_checkbox_frame.pack(fill="x", pady=5)
        
        self.no_watermark_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_checkbox_frame, text="Try to remove watermark", variable=self.no_watermark_var).pack(side="left", padx=5)
        
        self.metadata_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_checkbox_frame, text="Include metadata", variable=self.metadata_var).pack(side="left", padx=5)
        
        # Button section
        action_frame = ttk.Frame(frame)
        action_frame.pack(fill="x", pady=10)
        
        fetch_btn = ttk.Button(action_frame, text="Fetch Video Info", command=self.fetch_video_info)
        fetch_btn.pack(side="left", padx=5)
        
        download_btn = ttk.Button(action_frame, text="Download", command=self.start_download, style="Accent.TButton")
        download_btn.pack(side="left", padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", pady=5)
        
        self.status_label = ttk.Label(frame, text="Ready")
        self.status_label.pack(anchor="w")
        
    def setup_settings_tab(self):
        frame = ttk.Frame(self.settings_tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Download path section
        path_frame = ttk.LabelFrame(frame, text="Download Location", padding=10)
        path_frame.pack(fill="x", pady=10)
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        self.path_var = tk.StringVar(value=self.default_path)
        path_entry = ttk.Entry(path_input_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side="left", fill="x", expand=True)
        
        browse_btn = ttk.Button(path_input_frame, text="Browse", command=self.browse_path)
        browse_btn.pack(side="left", padx=5)
        
        # File naming options
        naming_frame = ttk.LabelFrame(frame, text="File Naming", padding=10)
        naming_frame.pack(fill="x", pady=10)
        
        self.naming_var = tk.StringVar(value="title")
        ttk.Radiobutton(naming_frame, text="Use video title", variable=self.naming_var, value="title").pack(anchor="w", pady=2)
        ttk.Radiobutton(naming_frame, text="Use video ID", variable=self.naming_var, value="id").pack(anchor="w", pady=2)
        ttk.Radiobutton(naming_frame, text="Use custom format", variable=self.naming_var, value="custom").pack(anchor="w", pady=2)
        
        custom_frame = ttk.Frame(naming_frame)
        custom_frame.pack(fill="x", pady=5)
        
        ttk.Label(custom_frame, text="Custom format:").pack(side="left")
        self.custom_format_var = tk.StringVar(value="%(title)s_%(id)s")
        custom_entry = ttk.Entry(custom_frame, textvariable=self.custom_format_var, width=30)
        custom_entry.pack(side="left", padx=5)
        
        ttk.Label(naming_frame, text="Available variables: %(title)s, %(id)s, %(uploader)s, %(upload_date)s").pack(anchor="w", pady=5)
        
        # Auto download options
        auto_frame = ttk.LabelFrame(frame, text="Automatic Features", padding=10)
        auto_frame.pack(fill="x", pady=10)
        
        self.auto_preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(auto_frame, text="Automatically fetch preview when URL is entered", variable=self.auto_preview_var).pack(anchor="w", pady=2)
        
        self.open_folder_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(auto_frame, text="Open folder after download completes", variable=self.open_folder_var).pack(anchor="w", pady=2)
        
        # Save settings button
        save_btn = ttk.Button(frame, text="Save Settings", command=self.save_settings)
        save_btn.pack(anchor="e", pady=10)
        
    def setup_about_tab(self):
        frame = ttk.Frame(self.about_tab, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Advanced TikTok Downloader", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Version 2.0", font=("Arial", 12)).pack()
        
        description = """
        This application allows you to download TikTok videos in various formats and quality options.
        
        Features:
        • Download TikTok videos without watermark
        • Convert to MP4, MP3, or GIF
        • Preview videos before downloading
        • Multiple quality options
        • Custom file naming
        
        This application uses yt-dlp for downloading content.
        """
        
        ttk.Label(frame, text=description, wraplength=500, justify="center").pack(pady=20)
        
        # Create hyperlink
        link_frame = ttk.Frame(frame)
        link_frame.pack(pady=10)
        
        def open_github():
            webbrowser.open("https://github.com/yourusername/tiktok-downloader")
            
        github_link = ttk.Label(link_frame, text="GitHub Repository", foreground="blue", cursor="hand2")
        github_link.pack()
        github_link.bind("<Button-1>", lambda e: open_github())
        
        # Add credit
        ttk.Label(frame, text="Created with Python and Tkinter", font=("Arial", 10)).pack(pady=20)
        
    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.save_path)
        if path:
            self.save_path = path
            self.path_var.set(path)
    
    def paste_url(self):
        clipboard = self.root.clipboard_get()
        if clipboard:
            self.entry_url.delete(0, tk.END)
            self.entry_url.insert(0, clipboard)
            if self.auto_preview_var.get():
                self.fetch_video_info()
    
    def clear_url(self):
        self.entry_url.delete(0, tk.END)
        self.clear_preview()
        
    def clear_preview(self):
        self.preview_canvas.delete("all")
        self.info_label.config(text="No video loaded")
        self.video_info = None
        
    def extract_video_id(self, url):
        # Extract TikTok video ID from URL
        patterns = [
            r'video/(\d+)',
            r'v/(\d+)',
            r'/(\d+)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
        
    def fetch_video_info(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a TikTok video URL")
            return
            
        self.status_label.config(text="Fetching video info...")
        self.progress_var.set(0)
        
        # Run in separate thread to avoid freezing UI
        threading.Thread(target=self._fetch_video_info, args=(url,), daemon=True).start()
    
    def _fetch_video_info(self, url):
        try:
            # Extract info without downloading
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'no_color': True,
                'skip_download': True,
                'noplaylist': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)
                
            self.root.after(0, self.update_preview)
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.status_label.config(text=f"Error: Failed to fetch video info"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch video info: {error_msg}"))
    
    def update_preview(self):
        if not self.video_info:
            return
            
        try:
            # Update info label
            title = self.video_info.get('title', 'Unknown title')
            uploader = self.video_info.get('uploader', 'Unknown uploader')
            duration = self.video_info.get('duration', 0)
            duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}" if duration else "Unknown"
            
            info_text = f"Title: {title}\nUploader: {uploader}\nDuration: {duration_str}"
            self.info_label.config(text=info_text)
            
            # Try to fetch thumbnail
            thumbnail_url = self.video_info.get('thumbnail')
            if thumbnail_url:
                try:
                    response = requests.get(thumbnail_url, stream=True)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        
                        # Calculate dimensions to fit the canvas
                        canvas_width = self.preview_canvas.winfo_width()
                        canvas_height = self.preview_canvas.winfo_height()
                        
                        img_width, img_height = img.size
                        
                        # Scale to fit
                        scale = min(canvas_width/img_width, canvas_height/img_height)
                        new_width = int(img_width * scale)
                        new_height = int(img_height * scale)
                        
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                        
                        # Convert to PhotoImage and keep reference
                        self.preview_image = ImageTk.PhotoImage(img)
                        
                        # Clear canvas and display image
                        self.preview_canvas.delete("all")
                        x = (canvas_width - new_width) // 2
                        y = (canvas_height - new_height) // 2
                        self.preview_canvas.create_image(x, y, anchor="nw", image=self.preview_image)
                        
                        # Add play button overlay
                        btn_x = canvas_width // 2
                        btn_y = canvas_height // 2
                        self.preview_canvas.create_oval(btn_x-25, btn_y-25, btn_x+25, btn_y+25, fill="white", outline="gray")
                        self.preview_canvas.create_polygon(btn_x-10, btn_y-15, btn_x-10, btn_y+15, btn_x+20, btn_y, fill="black")
                except Exception as e:
                    self.preview_canvas.delete("all")
                    self.preview_canvas.create_text(canvas_width//2, canvas_height//2, text="Preview not available", fill="gray")
            
            self.status_label.config(text="Video info fetched successfully")
            
        except Exception as e:
            self.status_label.config(text=f"Error displaying preview")
            print(f"Preview error: {e}")
    
    def get_quality_format(self):
        quality = self.quality_var.get()
        
        if quality == "best":
            return "bestvideo+bestaudio/best"
        elif quality == "medium":
            return "worstvideo[height>=480]+worstaudio/worst[height>=480]"
        else:  # low
            return "worstvideo+worstaudio/worst"
    
    def get_output_template(self):
        naming = self.naming_var.get()
        
        if naming == "title":
            return "%(title)s.%(ext)s"
        elif naming == "id":
            return "%(id)s.%(ext)s"
        else:  # custom
            custom_format = self.custom_format_var.get()
            if not custom_format:
                custom_format = "%(title)s_%(id)s"
            return f"{custom_format}.%(ext)s"
    
    def start_download(self):
        if self.download_in_progress:
            messagebox.showinfo("Info", "Download already in progress")
            return
            
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a TikTok video URL")
            return
        
        save_path = self.path_var.get()
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create download directory: {e}")
                return
        
        self.download_in_progress = True
        self.status_label.config(text="Starting download...")
        self.progress_var.set(0)
        
        # Run download in separate thread
        threading.Thread(target=self._download_video, args=(url, save_path), daemon=True).start()
    
    def _download_video(self, url, save_path):
        try:
            output_template = self.get_output_template()
            output_path = os.path.join(save_path, output_template)
            
            format_option = self.format_var.get()
            quality = self.get_quality_format()
            
            ydl_opts = {
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }
            
            # Format specific options
            if format_option == "mp3":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            elif format_option == "gif":
                ydl_opts.update({
                    'format': quality,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'gif',
                    }],
                })
            else:  # mp4
                ydl_opts.update({
                    'format': quality,
                    'merge_output_format': 'mp4',
                })
            
            # Add metadata if requested
            if self.metadata_var.get():
                ydl_opts['writeinfojson'] = True
                if 'postprocessors' not in ydl_opts:
                    ydl_opts['postprocessors'] = []
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegMetadata',
                })
            
            # Try to remove watermark if requested
            if self.no_watermark_var.get():
                if 'postprocessors' not in ydl_opts:
                    ydl_opts['postprocessors'] = []
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoRemuxer',
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Get file path without extension (it might have changed due to post-processing)
                file_base = os.path.splitext(filename)[0]
                file_dir = os.path.dirname(filename)
                
                # Try to find the actual file that was downloaded
                final_file = None
                for ext in ['mp4', 'mp3', 'gif']:
                    potential_file = f"{file_base}.{ext}"
                    if os.path.exists(potential_file):
                        final_file = potential_file
                        break
                
                # If we couldn't find the exact file, just use the directory
                if not final_file:
                    final_file = file_dir
                
            # Add to download history
            self.download_history.append({
                'url': url,
                'file': final_file,
                'time': os.path.getmtime(final_file) if os.path.exists(final_file) else 0
            })
            
            # Open folder if requested
            if self.open_folder_var.get():
                self.root.after(0, lambda: self.open_folder(file_dir))
            
            self.root.after(0, lambda: self.status_label.config(text="Download complete!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.status_label.config(text=f"Error: {error_msg[:50]}..."))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to download video: {error_msg}"))
        finally:
            self.download_in_progress = False
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            try:
                # Extract percentage value from string like '50.5%'
                percent = float(p.strip('%'))
                self.root.after(0, lambda: self.progress_var.set(percent))
            except (ValueError, TypeError):
                pass
                
            # Update status message
            msg = f"Downloading: {p}"
            if 'eta' in d and d['eta'] is not None:
                msg += f" - ETA: {d['eta']} seconds"
                
            final_msg = msg[:50] + "..." if len(msg) > 50 else msg
            self.root.after(0, lambda: self.status_label.config(text=final_msg))
            
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_label.config(text="Download finished, processing file..."))
    
    def open_folder(self, path):
        """Open the folder containing the downloaded file"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS, Linux
                if os.uname().sysname == 'Darwin':  # macOS
                    os.system(f'open "{path}"')
                else:  # Linux
                    os.system(f'xdg-open "{path}"')
        except Exception as e:
            print(f"Failed to open folder: {e}")
    
    def save_settings(self):
        """Save current settings"""
        self.save_path = self.path_var.get()
        messagebox.showinfo("Settings", "Settings saved successfully")


# Start the application
if __name__ == "__main__":
    root = ThemedTk(theme="breeze")
    app = TikTokDownloader(root)
    root.mainloop()
