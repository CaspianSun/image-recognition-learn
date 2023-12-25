import pyautogui


def screenshot(position, size):
    if position and size:
        x, y = position
        width, height = size
        img = pyautogui.screenshot(region=(x, y, width, height))
        img.save("window_screenshot.png")
