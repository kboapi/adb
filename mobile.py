import asyncio
import websockets
import json
import time
import uiautomator2
from uiautomator2 import Direction
from bin.lib.lib_adb import LibAdb
from threading import Thread
import requests
data_adb = []
def loop_check_adb():
    global data_adb
    while True:
        try:
            main_adb = LibAdb()
            data_adb = main_adb.list_adb()
            time.sleep(1)
        except:
            pass

Thread(target=loop_check_adb, daemon=True).start()  # Use daemon=True to allow exiting when main thread ends


def get_devices_all():
    main_adb = LibAdb()
    data_adb = main_adb.list_adb()
    return  data_adb

def close_unwanted_apps(d):
    """Close unwanted apps on the Android device."""
    d.press('home')
    d.app_start('com.termux')
    d.app_stop('com.kasikorn.retail.mbanking.wap')
    d.app_stop('com.android.chrome')
    d.press('home')

def close_all_apps(d):
    """Closes all apps in the recent apps screen."""
    d.press('home')
    d.press('recent')
    time.sleep(1)
    d(resourceId=f"com.miui.home:id/clearAnimView").click()

async def connect_websocket(ip,name_device):
    uri = f"ws://{ip}:7766/ws/{name_device}"

    while True:  # Loop to attempt reconnection
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket server")

                try:
                    while True:
                        response = await websocket.recv()
                        command_data = json.loads(response)

                        # Check and execute commands received from the server
                        devices = get_devices_all()
                        device_id = devices[0]
                        adb = None
                        try:
                            adb = uiautomator2.connect(device_id)
                        except:
                            response = {"status": False, "msg": "Device is not specified."}
                            pass
                            
                        if command_data.get("action") == "unlock":
                            if adb.info['currentPackageName'] == "com.android.systemui":
                                adb.screen_on()
                                adb.swipe_ext(Direction.FORWARD)
                                response = {"status": True, "msg": "ปลดล็อก สำเร็จ"}
                            else:
                                response = {"status": True, "msg": "มือถือปลดล็อกแล้ว"}

                        elif command_data.get("action") == "lock":
                            adb.screen_off()
                            response = {"status": True, "msg": "ล็อก สำเร็จ"}
                        elif command_data.get("action") == "check_device":
                            main_adb = LibAdb()
                            data_adb = main_adb.list_adb()
                            if data_adb[0] is not None:
                                response = {"status": True, "msg": f"พบอุปกรณ์: {data_adb[0]}"}
                            else:
                                response = {"status": False, "msg": f"ไม่พบอุปกรณ์ที่เชื่อมต่อ"}
                        elif command_data.get("action") == "clear_all":
                            close_all_apps(adb)
                            response = {"status": True, "msg": "clear สำเร็จ"}

                        # print(response)
                       
                        # payload = json.dumps(response)
                        # headers = {
                        # 'Content-Type': 'application/json'
                        # }

                        # responses = requests.request("POST", command_data.get("callbackUrl"), headers=headers, data=payload)
                        # print(responses.json())
                        await websocket.send(json.dumps(response))
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed by the server, trying to reconnect...")

        except Exception as e:
            print(f"Connection error: {e}. Trying to reconnect...")
            await asyncio.sleep(2)  # Wait before trying to reconnect

# Main block to run the WebSocket client
if __name__ == "__main__":
    asyncio.run(connect_websocket("206.189.81.158","test"))
    # asyncio.run(connect_websocket("localhost","test"))
