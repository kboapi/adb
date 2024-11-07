import asyncio
import websockets
import json
import time
import uiautomator2
from uiautomator2 import Direction
from bin.lib.lib_adb import LibAdb
import xmltodict
import argparse
data_adb = []

# Utility functions
def get_devices_all():
    main_adb = LibAdb()
    return main_adb.list_adb()

def close_unwanted_apps(d):
    """Close unwanted apps on the Android device."""
    d.press('home')
    d.app_start('com.termux')
    d.app_stop('com.kasikorn.retail.mbanking.wap')
    d.app_stop('com.android.chrome')
    d.press('home')

def get_ui_elements_info(device):
    # Dump the UI hierarchy (XML format)
    ui_hierarchy = device.dump_hierarchy()

    # Convert the XML hierarchy to a Python dictionary using xmltodict
    ui_dict = xmltodict.parse(ui_hierarchy)

    # Convert the dictionary to JSON (you can also keep it as dict if you don't need JSON specifically)
    # ui_json = json.dumps(ui_dict, indent=4, ensure_ascii=False)

    return ui_dict  # Return JSON formatted UI data
async def connect_websocket(ip,name_device):
    uri = f"ws://{ip}:7766/ws/{name_device}"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket server")

                while True:
                    try:
                        message = await websocket.recv()
                        command_data = json.loads(message)
                        devices = get_devices_all()
                        device_id = devices[0]
                        adb = None
                        try:
                            adb = uiautomator2.connect(device_id)
                        except:
                            response = {"status": False, "msg": "Device is not specified."}
                            pass

                        # Handle the "transfer" action
                        if command_data.get("action") == "transfer":
                            start_time = time.time()
                            time_out = 60

                            device = command_data.get("device")
                            if not device:
                                devices = get_devices_all()
                                device = devices[0]

                            token = command_data.get("token")
                            link = f"https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/{token}"
                            pin = "112233"

                            if device not in data_adb:
                                response = {"status": False, "msg": "check name device"}
                                await websocket.send(json.dumps(response))
                                continue

                            package = "com.kasikorn.retail.mbanking.wap"
                            adb = uiautomator2.connect(device)
                            print(adb.info)

                            if adb.info['currentPackageName'] == "com.android.systemui":
                                adb.screen_on()
                                adb.swipe_ext(Direction.FORWARD)

                            close_unwanted_apps(adb)
                            adb.app_stop(package)
                            adb.open_url(link)

                            while True:
                                if time.time() - start_time >= time_out:
                                    adb.app_stop(package)
                                    response = {"status": False, "msg": "time_out"}
                                    await websocket.send(json.dumps(response))
                                    break

                                try:
                                    adb(text="ขออภัย").get_text(timeout=0.1)
                                    adb.app_stop(package)
                                    response = {"status": False, "msg": "check token"}
                                    await websocket.send(json.dumps(response))
                                    break
                                except:
                                    pass

                                try:
                                    check_pin = adb(text="กรุณาใส่รหัสผ่าน").get_text(timeout=0.1)
                                    print(check_pin)
                                    break
                                except:
                                    pass

                            time.sleep(1)
                            for p in pin:
                                adb(resourceId=f"com.kasikorn.retail.mbanking.wap:id/linear_layout_button_activity_{p}").click()
                                time.sleep(0.5)

                            data_json = {}
                            while True:
                                if time.time() - start_time >= time_out:
                                    adb.app_stop(package)
                                    response = {"status": False, "msg": "time_out"}
                                    await websocket.send(json.dumps(response))
                                    break

                                try:
                                    adb(text="ยืนยันรายการ").get_text(timeout=0.1)
                                    data_info = adb(className="android.widget.TextView")
                                    data_json = {
                                        "from": data_info[-5].get_text(),
                                        "to": data_info[-4].get_text(),
                                        "amount": data_info[-3].get_text(),
                                        "fee": data_info[-2].get_text(),
                                        "number": data_info[-1].get_text(),
                                    }
                                    break
                                except:
                                    pass

                            while True:
                                if time.time() - start_time >= time_out:
                                    adb.app_stop(package)
                                    response = {"status": False, "msg": "time_out"}
                                    await websocket.send(json.dumps(response))
                                    break

                                try:
                                    adb(text="ยืนยัน").click(timeout=0.5)
                                except:
                                    pass

                                try:
                                    adb(text="ดำเนินการเสร็จสิ้น").get_text(timeout=0.1)
                                    time.sleep(1)
                                    adb.app_stop(package)
                                    response = {"status": True, "msg": data_json}
                                    await websocket.send(json.dumps(response))
                                    break
                                except:
                                    pass
                        elif command_data.get("action") == "unlock":
                            if adb.info['currentPackageName'] == "com.android.systemui":
                                adb.screen_on()
                                adb.swipe_ext(Direction.FORWARD)
                                response = {"status": True, "msg": "ปลดล็อก สำเร็จ"}
                            else:
                                response = {"status": True, "msg": "มือถือปลดล็อกแล้ว"}
                        elif command_data.get("action") == "info":
                            try:
                                data = get_ui_elements_info(adb)
                                response = {"status": True, "msg": data}
                            except Exception as e:
                                response = {"status": False, "msg": f"Failed to get UI elements info: {str(e)}"}
                                pass
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
                        else:
                            response = {"status": False, "msg": f"action not allow"}
                        await websocket.send(json.dumps(response))
                    except websockets.exceptions.ConnectionClosed:
                        print("Connection closed, reconnecting...")
                        # pass
                        break
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 2 seconds...")
            await asyncio.sleep(2)  # Reconnect delay

# Main block to run the WebSocket client
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="โปรแกรมรับค่าพารามิเตอร์มือถือจากบรรทัดคำสั่ง")
    parser.add_argument('--username', type=str, help='Username Kbiz')
    args = parser.parse_args()
    print(f"kbiz user: {args.username}")
    asyncio.run(connect_websocket("206.189.81.158","test"))
