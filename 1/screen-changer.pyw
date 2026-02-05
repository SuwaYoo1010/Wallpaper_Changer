import os
import time
import random
import ctypes
import subprocess
import platform
from datetime import datetime, timedelta

# Wallpaper folder is set via WALLPAPER_FOLDER environment variable in the venv
WALLPAPER_FOLDER = os.environ.get("WALLPAPER_FOLDER", r"C:\Example\Directory")

# Interchangeable schedule times in 24-hour format
SCHEDULE_TIMES = [
    "07:00",
    "13:00",
    "18:00",
]

def get_images(folder):
    """Returns a list of valid image paths from the folder."""
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    images = []
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.lower().endswith(valid_extensions):
                images.append(os.path.join(folder, filename))
    return images

def set_wallpaper(image_path):
    """Sets the wallpaper based on the Operating System."""
    system_name = platform.system()
    abs_path = os.path.abspath(image_path)
    try:
        if system_name == "Windows":
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
        elif system_name == "Darwin":
            script = f'tell application "System Events" to set picture of every desktop to "{abs_path}"'
            subprocess.run(["osascript", "-e", script])
        elif system_name == "Linux":
            uri = f"file://{abs_path}"
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri])
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Wallpaper updated to: {os.path.basename(abs_path)}")
    except Exception as e:
        print(f"Error setting wallpaper: {e}")

def get_next_run_time(schedule_strs):
    """Calculates the exact datetime for the next scheduled change."""
    now = datetime.now()
    scheduled_times = []

    for time_str in schedule_strs:
        t = datetime.strptime(time_str, "%H:%M").time()
        scheduled_times.append(datetime.combine(now.date(), t))
    
    scheduled_times.sort()

    for sched_time in scheduled_times:
        if sched_time > now:
            return sched_time
        
    return scheduled_times[0] + timedelta(days=1)

def main():
    print("Scheduled Wallpaper Changer Started...")
    images = get_images(WALLPAPER_FOLDER)
    
    if not images:
        print("No images found!")
        return


    while True:
        next_run = get_next_run_time(SCHEDULE_TIMES)
        print(f"Next change scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

        while datetime.now() < next_run:
            time.sleep(10)

        set_wallpaper(random.choice(images))
        
        time.sleep(1) 

if __name__ == "__main__":
    main()
