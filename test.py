# import uiautomator2 as u2
# import subprocess
# import time

# Connect to the device
# d = u2.connect('ZPMFORA6SWWWGY6T')

# d.debug = True
# d.info
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


# def close_unwanted_apps(d,excluded_apps=None):
#     d.press('home')
#     d.app_start('com.termux')
#     d.app_clear('com.kasikorn.retail.mbanking.wap')
#     d.app_clear('com.android.chrome')
#     # d.app_clear('com.gawk.smsforwarder')
#     d.press('home')


# close_unwanted_apps(d)

import uiautomator2 as u2
import time
import subprocess
# เชื่อมต่อกับอุปกรณ์ Android
from threading import Thread
stop_thread = False

# ฟังก์ชันสำหรับคลิกปุ่ม "อนุญาต"
def click_allow():
    global stop_thread
    while not stop_thread:
        time.sleep(2)  # รอให้หน้าจอพร้อม
        d.click(115, 1312)  # คลิกที่พิกัดแรก
        print("เริ่ม click")
        d.click(195, 1402)  # คลิกที่พิกัดที่สอง
        break  # หยุดหลังจากคลิกครั้งเดียว
d = u2.connect()
d.set_orientation("n") 
# ข้อความที่คุณต้องการวาง
command_to_paste = "pkg update -y && pkg upgrade -y && pkg install git -y && pkg install python -y"
# เปิดแอป Termux
d.app_start("com.termux")
time.sleep(3)  # รอให้แอป Termux เปิดขึ้น
try:
    footer_bank_textview = d(text="อนุญาต").get_text(timeout=0.1)
    print(footer_bank_textview)
    d(text="อนุญาต").click()
except:
    pass


command_to_paste = (
    "pkg upgrade -y && "
    "pkg install git -y && "
    "pkg install python -y && "
    "yes | pip install cython && "
    "pkg install libxml2 libxslt -y && "
    "pkg install -y python ndk-sysroot clang make libjpeg-turbo -y && "
    "pkg install clang -y && "
    "yes | pip install lxml && "
    "yes | pip install --pre uiautomator2 && "
    "yes | pip install pure-python-adb && "
    "pkg install android-tools -y && "
    "yes | pip install flask && "
    "yes | pip install xmltodict && "
    "pkg update -y"
)

# ใช้ ADB เพื่อคัดลอกข้อความไปยังคลิปบอร์ด
subprocess.run(f'adb shell "echo \'{command_to_paste}\' | tr -d \'\\n\' | am broadcast -a clipper.set -e text \\"{command_to_paste}\\""',
               shell=True)
print("ข้อความถูกคัดลอกไปยังคลิปบอร์ดแล้วผ่าน ADB")

# วางข้อความใน Termux และกด Enter เพื่อรันคำสั่ง

thread = Thread(target=click_allow)
thread.start()
d.send_keys(command_to_paste)
d.send_keys("\n")  # กด Enter เพื่อรันคำสั่ง
print("คำสั่งถูกวางและรันใน Termux แล้ว")
stop_thread = True  # ตั้งค่าสถานะเพื่อหยุด Thread
thread.join()  

# # เชื่อมต่อกับอุปกรณ์ Android
# adb = u2.connect()

# # เปิดแอป Termux
# adb.app_start("com.termux")
# time.sleep(2)  # รอให้แอป Termux เปิดขึ้น

# # รายการคำสั่งที่ต้องการรันใน Termux
# commands = [
#     "pkg update -y",
#     "pkg upgrade -y",
#     "pkg install git -y",
#     "pkg install python -y",
#     "pkg install clang -y",
#     "pkg install make -y",
#     "pkg install libjpeg-turbo -y",
#     "pkg install libxml2 libxslt -y",
#     "pkg install ndk-sysroot -y",
#     "pkg install android-tools -y",
#     "yes | pip install cython",
#     "yes | pip install lxml",
#     "yes | pip install --pre uiautomator2",
#     "yes | pip install pure-python-adb",
#     "yes | pip install flask",
#     "yes | pip install xmltodict"
# ]
# stop_thread = False

# # ฟังก์ชันสำหรับคลิกปุ่ม "อนุญาต"
# def click_allow():
#     global stop_thread
#     while not stop_thread:
#         time.sleep(2)  # รอให้หน้าจอพร้อม
#         adb.click(115, 1312)  # คลิกที่พิกัดแรก
#         print("เริ่ม click")
#         adb.click(195, 1402)  # คลิกที่พิกัดที่สอง
#         break  # หยุดหลังจากคลิกครั้งเดียว

# # วนลูปเพื่อส่งแต่ละคำสั่งไปยัง Termux
# for command in commands:
#     for char in command:  # ส่งทีละตัวอักษร
        
        # try:
        #     footer_bank_textview = adb(text="อนุญาต").get_text(timeout=0.1)
        #     print(footer_bank_textview)
        #     adb(text="อนุญาต").click()
        # except:
        #     pass

        # thread = Thread(target=click_allow)
#         thread.start()
#         adb.send_keys(char)
#         stop_thread = True  # ตั้งค่าสถานะเพื่อหยุด Thread
#         thread.join()  

#     adb.send_keys("\n")  # กด Enter เพื่อรันคำสั่ง
