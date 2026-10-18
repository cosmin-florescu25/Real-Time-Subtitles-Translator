import mss
import mss.tools
from pathlib import Path
from screeninfo import get_monitors

# Function to take a screenshot of a specific area of the screen
def take_screenshot():
    destination_folder = Path('images')
    destination_folder.mkdir(exist_ok=True)
    file_name = 'documentation_image.png'
    full_path = str(destination_folder / file_name)

    monitor_info = get_monitors()[0]
    monitor_height = monitor_info.height
    monitor_width = monitor_info.width

    heigh_fraction = 1/6.6
    height = int(monitor_height * heigh_fraction)

    taskbar_height = 105
    width_fraction = 0.5
    width = int(monitor_width * width_fraction)

    top = int(monitor_height - height - taskbar_height)
    left = int((monitor_width - width) / 2)

    m_values = {
        "top": top,
        "left": left,
        "width": width,
        "height": height
    }

    with mss.mss() as sct:
        sct.grab(m_values)
        output = "sct-{top}x{left}_{width}x{height}.png".format(**m_values)
        
        screen_shot = sct.grab(m_values)
        mss.tools.to_png(screen_shot.rgb, screen_shot.size, output=full_path)
    return {**m_values}

if __name__ == "__main__":
    take_screenshot()