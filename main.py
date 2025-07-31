import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import glob
import re

PRIMARY_COLOR = "#800000"
BG_COLOR = "#181818"
FG_COLOR = "#f2f2f2"

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CyMed Downloader")
        self.root.geometry("600x380")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        frame = tk.Frame(root, bg=BG_COLOR)
        frame.pack(padx=30, pady=30)

        tk.Label(frame, text="CyMed Downloader", font=("Segoe UI", 28, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=(0, 20))

        tk.Label(frame, text="YouTube URL:", font=("Segoe UI", 12), fg=FG_COLOR, bg=BG_COLOR).pack(anchor="w")
        self.url_entry = tk.Entry(frame, width=50, font=("Segoe UI", 12), bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, highlightbackground=PRIMARY_COLOR, highlightcolor=PRIMARY_COLOR, highlightthickness=1, relief="flat")
        self.url_entry.pack(pady=(0, 20))

        self.type_var = tk.StringVar(value="video")
        tk.Radiobutton(frame, text="Video (mp4, select resolution)", variable=self.type_var, value="video", font=("Segoe UI", 11), fg=FG_COLOR, bg=BG_COLOR, selectcolor=PRIMARY_COLOR, activebackground=BG_COLOR, activeforeground=PRIMARY_COLOR).pack(anchor="w")
        tk.Radiobutton(frame, text="Audio (mp3)", variable=self.type_var, value="audio", font=("Segoe UI", 11), fg=FG_COLOR, bg=BG_COLOR, selectcolor=PRIMARY_COLOR, activebackground=BG_COLOR, activeforeground=PRIMARY_COLOR).pack(anchor="w")

        self.res_var = tk.StringVar(value="1080")
        res_options = ["144", "360", "720", "1080", "1440", "2160"]
        res_frame = tk.Frame(frame, bg=BG_COLOR)
        res_frame.pack(anchor="w", pady=(10, 20))
        tk.Label(res_frame, text="Resolution:", font=("Segoe UI", 12), fg=FG_COLOR, bg=BG_COLOR).pack(side="left")
        tk.OptionMenu(res_frame, self.res_var, *res_options).pack(side="left", padx=10)

        tk.Button(frame, text="Download", font=("Segoe UI", 13, "bold"), bg=PRIMARY_COLOR, fg=FG_COLOR, activebackground=BG_COLOR, activeforeground=PRIMARY_COLOR, command=self.download).pack(pady=(1, 1), fill="x")

        self.status = tk.Label(frame, text="", font=("Segoe UI", 10), fg=PRIMARY_COLOR, bg=BG_COLOR)
        self.status.pack()

    def download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status.config(text="Please enter a YouTube URL.")
            return

        match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
        if match:
            url = f"https://www.youtube.com/watch?v={match.group(1)}"

        self.status.config(text="Downloading, please wait...")
        self.root.update_idletasks()
        try:
            if self.type_var.get() == "video":
                cmd = [
                    "yt-dlp",
                    "-f", f"bestvideo[height={self.res_var.get()}]+bestaudio/best[height={self.res_var.get()}]",
                    "-o", "%(title)s.%(ext)s",
                    url
                ]
                ext = "*.mp4"
            else:
                cmd = [
                    "yt-dlp",
                    "-f", "bestaudio",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "-o", "%(title)s.%(ext)s",
                    url
                ]
                ext = "*.mp3"
            subprocess.run(cmd, check=True)
            files = glob.glob(ext)
            if files:
                latest_file = max(files, key=os.path.getctime)
                self.status.config(text=f"Downloaded: {latest_file}")
                messagebox.showinfo("Success", f"Downloaded: {latest_file}")
            else:
                self.status.config(text="No downloaded file found.")
        except Exception as e:
            self.status.config(text=f"Download failed: {e}")
            messagebox.showerror("Error", f"yt-dlp failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()