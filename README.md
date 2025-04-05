# Advanced TikTok Downloader

An easy-to-use desktop application for downloading TikTok videos with advanced features and a modern interface.

![TikTok Downloader](https://via.placeholder.com/800x450)

## Features

- **Multiple formats**: Download videos as MP4, MP3 (audio only), or GIF
- **Quality options**: Choose between best, medium, or low quality
- **Video preview**: See thumbnail and video info before downloading
- **Watermark removal**: Option to attempt watermark removal
- **Custom file naming**: Define your own file naming patterns
- **User-friendly interface**: Clean, tabbed design with easy navigation
- **Download tracking**: View progress with completion estimates
- **Customizable settings**: Configure download locations and preferences

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages (see below)


## Dependencies

- tkinter and ttkbootstrap: For the graphical user interface
- ttkthemes: For modern UI themes
- yt-dlp: For downloading TikTok videos
- Pillow: For image processing
- requests: For fetching thumbnails and metadata

Install all dependencies at once:

```bash
pip install tkinter ttkbootstrap ttkthemes yt-dlp pillow requests
```

## Usage Guide

### Basic Usage

1. Launch the application
2. Paste a TikTok video URL in the input field
3. Click "Fetch Video Info" to see a preview
4. Select your desired format and quality options
5. Click "Download" to save the video

### Advanced Options

#### Quality Settings

- **Best**: Highest video and audio quality available
- **Medium**: 480p or better quality
- **Low**: Lowest quality (saves bandwidth)

#### Format Options

- **MP4**: Standard video format with audio
- **MP3**: Extract audio only
- **GIF**: Convert video to animated GIF

#### Download Settings

- **Remove watermark**: Attempts to remove TikTok watermark
- **Include metadata**: Saves video information in a JSON file
- **Custom naming**: Define how downloaded files should be named

## Configuration

In the Settings tab, you can configure:

- **Download location**: Choose where files will be saved
- **File naming**: Use video title, ID, or custom naming pattern
- **Automatic features**: Enable/disable auto-preview and folder opening

## Known Issues

- Watermark removal may not work on all videos due to TikTok's changing formats
- Some very recent videos might not be downloadable due to yt-dlp updates
- GIF conversion might result in large file sizes for longer videos

## Troubleshooting

### Common Issues

1. **Download fails immediately**
   - Check your internet connection
   - Make sure the TikTok URL is valid and accessible

2. **Processing takes too long**
   - For longer videos, processing might take several minutes
   - Low-end systems might experience slowdowns during format conversion

3. **Cannot open downloaded files**
   - Ensure you have appropriate media players installed
   - Check if antivirus is blocking the application

### Updating yt-dlp

If downloads stop working, you might need to update yt-dlp:

```bash
pip install --upgrade yt-dlp
```


## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the download engine
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) for the modern UI components

---

⚠️ **Disclaimer**: This tool is for personal use only. Always respect copyright and terms of service of TikTok. The developers are not responsible for any misuse of this software.
