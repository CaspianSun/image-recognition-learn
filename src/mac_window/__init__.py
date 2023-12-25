import subprocess
from src.screenshot import screenshot


def get_active_window_info():
    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        set frontAppName to name of first application process whose frontmost is true
        set frontAppId to bundle identifier of first application process whose frontmost is true
        set frontAppWindow to title of first window of (first application process whose frontmost is true)
    end tell
    return {frontApp, frontAppName, frontAppId, frontAppWindow}
    '''
    try:
        output = subprocess.check_output(["osascript", "-e", script])
        return output.decode("utf-8").strip().split(", ")
    except subprocess.CalledProcessError:
        return None


def get_all_window_info():
    script = '''
    tell application "System Events"
        set windowDetails to ""
        repeat with proc in (every process where background only is false)
            repeat with win in windows of proc
                set procName to name of proc as string
                set windowDetails to windowDetails & procName & "\n"
            end repeat
        end repeat
        return windowDetails
    end tell
    '''
    try:
        output = subprocess.check_output(["osascript", "-e", script])
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return str(e)


def get_window_position(app_name):
    position_script = f"""
    tell application "System Events"
        tell process "{app_name}"
            get position of first window
        end tell
    end tell
    """
    size_script = f"""
    tell application "System Events"
        tell process "{app_name}"
            get size of first window
        end tell
    end tell
    """
    try:
        position_result = subprocess.check_output(['osascript', '-e', position_script])
        size_result = subprocess.check_output(['osascript', '-e', size_script])

        position_result = position_result.decode("utf-8").strip().split(", ")
        size_result = size_result.decode("utf-8").strip().split(", ")
        position = (int(position_result[0]), int(position_result[1]))
        size = (int(size_result[0]), int(size_result[1]))
        return position, size
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, None

def set_window_position_and_size(app_name, position, size):
    x, y = position
    width, height = size
    script = f'''
    tell application "System Events" to tell process "{app_name}"
        set position of first window to {{{x}, {y}}}
        set size of first window to {{{width}, {height}}}
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)


def bring_window_to_front(app_id):
    # CFBundleIdentifier
    script = f'tell application id "{app_id}" to activate'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error bringing {app_id} to front: {e}")


if __name__ == '__main__':
    position, size = get_window_position("wechatdevtools")
    set_window_position_and_size("wechatdevtools", (0, 25), (1400, 1000))
    position, size = get_window_position("wechatdevtools")
    bring_window_to_front("com.tencent.webplusdevtools")
    screenshot(position, size)
