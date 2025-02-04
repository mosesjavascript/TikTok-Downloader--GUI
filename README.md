# TikTok Video Downloader

## Description

This is a GUI-based TikTok Video Downloader built using Python. The software allows users to paste a TikTok video URL, select a save location, and download the video in high quality (MP4 format). The interface is designed with a modern look using `ttkthemes` and `ttkbootstrap`.

### Features

- Download TikTok videos in high quality (MP4 format).
- User-friendly graphical interface.
- Allows users to choose a save location before downloading.
- Uses `yt-dlp` for extracting and downloading videos.
- Modern UI with `ttkbootstrap` and `ttkthemes`.
- Custom icon support.

### Libraries Used

The following Python libraries are used in this project:

| Library       | Purpose                                                                 |
|---------------|-------------------------------------------------------------------------|
| `tkinter`     | Provides the graphical user interface (GUI) framework.                   |
| `yt-dlp`      | Downloads videos from TikTok and other platforms.                       |
| `ttkthemes`   | Enhances the look and feel of the tkinter GUI.                           |
| `ttkbootstrap`| Provides modern Bootstrap-themed widgets for tkinter.                   |
| `os`          | Used for handling file paths and checking the existence of the icon file.|

## Installation

1. **Install Python** (if not already installed): [Download Python](https://www.python.org/downloads/).

2. **Install required dependencies** by running the following command:

    ```bash
    pip install yt-dlp ttkthemes ttkbootstrap
    ```

3. **Clone the repository or download the script**:

    ```bash
    git clone https://github.com/yourusername/TikTok-Downloader.git
    cd TikTok-Downloader
    ```

4. **Run the script**:

    ```bash
    python tiktok_downloader.py
    ```

## How the Code Works

### GUI Setup:
- The application is built using `tkinter`.
- `ThemedTk` (from `ttkthemes`) is used to apply a modern UI theme.
- `ttkbootstrap` provides enhanced Bootstrap-style widgets.
- The application window is set to 450x250 pixels and is non-resizable.
- A custom icon (`clock.ico`) is applied if it exists.

### Downloading Process:
- The user enters a TikTok video URL.
- The `download_video` function validates the URL and prompts the user to select a save location.
- The `yt-dlp` library is used to fetch and download the best available video and audio streams.
- The downloaded file is merged and saved in MP4 format.
- Success or error messages are displayed accordingly.

## Usage

1. Open the application.
2. Enter a valid TikTok video URL in the input field.
3. Click the **"Download Video"** button.
4. Choose a folder where the video will be saved.
5. Wait for the download to complete and check the selected folder for the video.

## Notes

- Ensure that `yt-dlp` is updated to the latest version for compatibility with TikTok:

    ```bash
    pip install --upgrade yt-dlp
    ```

- If downloading fails, check your internet connection and ensure the TikTok URL is accessible.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
