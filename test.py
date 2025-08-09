import subprocess
import time
import win32gui
import win32con
import win32api
import threading
import queue


def get_all_notepad_windows():
    """Get list of all current Notepad windows"""
    windows = []

    def enum_callback(hwnd, lParam):
        try:
            class_name = win32gui.GetClassName(hwnd)
            if class_name == "Notepad" and win32gui.GetParent(hwnd) == 0:
                windows.append(hwnd)
        except:
            pass
        return True

    win32gui.EnumWindows(enum_callback, None)
    return windows


def monitor_for_new_window(existing_windows, result_queue, stop_event):
    """Monitor for new Notepad windows in a separate thread"""
    last_check = set(existing_windows)

    while not stop_event.is_set():
        current = set(get_all_notepad_windows())
        new_windows = current - last_check

        if new_windows:
            # Found a new window!
            new_hwnd = list(new_windows)[0]
            print(f"Monitor found new window: {new_hwnd}")

            # IMMEDIATELY hide it
            try:
                win32gui.ShowWindow(new_hwnd, win32con.SW_HIDE)
                print("New window hidden immediately!")
                result_queue.put(new_hwnd)
                return
            except:
                pass

        last_check = current
        time.sleep(0.01)  # Check very frequently


def animate_slide(hwnd, start_x, start_y, end_x, end_y, steps=120, total_time=1.8):
    """Animate window sliding from start to end position"""
    delay = total_time / steps

    for i in range(steps + 1):
        # Smooth easing function
        t = i / steps
        eased_t = t * t * (3.0 - 2.0 * t)  # Smoothstep

        current_x = int(start_x + (end_x - start_x) * eased_t)
        current_y = int(start_y + (end_y - start_y) * eased_t)

        # Move window
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            current_x,
            current_y,
            0,
            0,
            win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
        )

        # Progress updates
        if i % 30 == 0:
            progress = int((i / steps) * 100)
            print(f"Slide progress: {progress}% - Position: ({current_x}, {current_y})")

        time.sleep(delay)

    # Remove topmost flag and bring to front
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_NOTOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )


def thingy(check: threading.Event):
    # Get screen dimensions
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    print(f"Screen size: {screen_width}x{screen_height}")

    # Get existing Notepad windows before starting new one
    existing_windows = get_all_notepad_windows()
    print(f"Found {len(existing_windows)} existing Notepad windows")

    # Window dimensions
    window_width = 800
    window_height = 600

    # Calculate positions
    start_x = -window_width - 50  # Start completely off-screen (left)
    center_x = (screen_width - window_width) // 2
    center_y = (screen_height - window_height) // 2

    print(f"Animation: ({start_x}, {center_y}) → ({center_x}, {center_y})")

    try:
        # Set up monitoring thread to catch and hide new window immediately
        result_queue = queue.Queue()
        stop_event = threading.Event()

        print("Starting window monitor thread...")
        monitor_thread = threading.Thread(
            target=monitor_for_new_window,
            args=(existing_windows, result_queue, stop_event),
        )
        monitor_thread.start()

        # Small delay to ensure monitor is running
        time.sleep(0.1)

        # Start Notepad normally (the monitor will catch and hide it)
        print("Starting Notepad (monitor will hide it immediately)...")
        process = subprocess.Popen("notepad.exe")
        pid = process.pid
        print(f"Started Notepad with PID: {pid}")

        # Wait for the monitor to find and hide the new window
        try:
            notepad_hwnd = result_queue.get(timeout=8)
            stop_event.set()  # Stop monitoring
            monitor_thread.join()
        except queue.Empty:
            print("Timeout waiting for new window!")
            stop_event.set()
            monitor_thread.join()
            return

        print(f"Got hidden Notepad window: {notepad_hwnd}")

        # Verify it's hidden
        is_visible = win32gui.IsWindowVisible(notepad_hwnd)
        print(f"Window is currently visible: {is_visible}")

        # Position the window at starting location while hidden
        print("Positioning hidden window at starting location...")
        win32gui.SetWindowPos(
            notepad_hwnd,
            win32con.HWND_TOP,
            start_x,
            center_y,
            window_width,
            window_height,
            win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE,
        )

        # Show it at the off-screen position
        print("Showing window at off-screen starting position...")
        win32gui.ShowWindow(notepad_hwnd, win32con.SW_SHOW)

        # Verify position
        rect = win32gui.GetWindowRect(notepad_hwnd)
        is_visible_now = win32gui.IsWindowVisible(notepad_hwnd)
        print(f"Window now visible: {is_visible_now}, Position: {rect}")

        # Small pause
        time.sleep(0.25)

        # Start the slide animation
        print("Starting slide animation from left edge to center...")
        animate_slide(notepad_hwnd, start_x, center_y, center_x, center_y)

        print("Animation complete! Notepad is now centered.")

        # Bring to front
        win32gui.SetForegroundWindow(notepad_hwnd)
        check.set()

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    i = 0
    check = threading.Event()
    thread = None
    while i < 100:
        if i == 10:
            thread = threading.Thread(target=thingy, args=(check,)).start()
        if check.is_set():
            print("Thread signaled completion.")
            check.clear()
        else:
            print(i)
        time.sleep(0.1)

        i += 1
    if thread is not None:
        thread.join()
