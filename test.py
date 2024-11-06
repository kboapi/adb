import uiautomator2 as u2
import subprocess
import time

# Connect to the device
d = u2.connect('R5CX14QKD3W')

d.debug = True
d.info
# # print(d.app_info("com.android.chrome"))
# print(d.device_info)


# d.app_stop_all(excludes=['com.facebook.katana'])
# d.app_clear('com.facebook.katana')
# d.app_clear(excludes=['com.facebook.katana'])
# Ensure the screen is on
# d.screen_on()

# # Use `adb shell` to perform additional tasks
# def run_adb_command(cmd):
#     """Run an ADB shell command and print the output."""
#     result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
#     print(result.stdout)
#     print(result.stderr)

# # Example ADB commands
# run_adb_command("input keyevent KEYCODE_WAKEUP")  # Turn on the screen
# run_adb_command("input swipe 300 1000 300 500")  # Swipe up (for swipe unlock)


def close_unwanted_apps(d,excluded_apps=None):
    d.press('home')
    d.app_start('com.termux')
    d.app_clear('com.kasikorn.retail.mbanking.wap')
    d.app_clear('com.android.chrome')
    # d.app_clear('com.gawk.smsforwarder')
    d.press('home')


close_unwanted_apps(d)