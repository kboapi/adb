import time
from flask import Flask,request,g,render_template,redirect,url_for,session
import uiautomator2
from uiautomator2 import Direction
from ppadb.client import Client as AdbClient
from bin.lib.lib_adb import LibAdb
from threading import Thread
import xmltodict
import subprocess
import json



app = Flask(__name__)
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

Thread(target=loop_check_adb).start()
def run_adb_command(cmd):
    """Run an ADB shell command and print the output."""
    result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
def close_unwanted_apps(d,excluded_apps=None):
    d.press('home')
    d.app_start('com.termux')
    d.app_stop('com.kasikorn.retail.mbanking.wap')
    d.app_stop('com.android.chrome')
    # d.app_clear('com.gawk.smsforwarder')
    d.press('home')



def filter_bank_shortCode(bankCode):
    """
    Function to filter bank name and return bank code
    
    Args:
        bank_name: Name of the bank in Thai or English, or bank code
        
    Returns:
        Bank code if found, None otherwise
    """
    # Define bank mapping
    bank_mapping = [
        {
            'bankCode': '030',
            'shortCode': 'GSB',
            'bankNameEn': 'Government Savings Bank',
            'bankNameTh': 'ออมสิน',
        },
        {
            'bankCode': '002',
            'shortCode': 'BBL',
            'bankNameEn': 'Bangkok Bank',
            'bankNameTh': 'กรุงเทพ',
        },
        {
            'bankCode': '004',
            'shortCode': 'KBANK',
            'bankNameEn': 'Kasikorn Bank',
            'bankNameTh': 'กสิกรไทย',
        },
        {
            'bankCode': '006',
            'shortCode': 'KTB',
            'bankNameEn': 'Krung Thai Bank',
            'bankNameTh': 'กรุงไทย',
        },
        {
            'bankCode': '011',
            'shortCode': 'tmb',
            'bankNameEn': 'TMBThanachart Bank',
            'bankNameTh': 'ทหารไทยธนชาต',
        },
        {
            'bankCode': '014',
            'shortCode': 'SCB',
            'bankNameEn': 'Siam Commercial Bank',
            'bankNameTh': 'ไทยพาณิชย์',
        },
        {
            'bankCode': '020',
            'shortCode': 'SCBT',
            'bankNameEn': 'Standard Chartered Bank (Thai)',
            'bankNameTh': 'แสตนดาร์ดชาร์เตอร์ (ไทย)',
        },
        {
            'bankCode': '022',
            'shortCode': 'CIMB',
            'bankNameEn': 'CIMB Thai Bank',
            'bankNameTh': 'ซีไอเอ็มบีไทย',
        },
        {
            'bankCode': '024',
            'shortCode': 'UOB',
            'bankNameEn': 'United Overseas Bank (Thai)',
            'bankNameTh': 'ยูโอบี',
        },
        {
            'bankCode': '025',
            'shortCode': 'krungsri',
            'bankNameEn': 'Bank of Ayudhya',
            'bankNameTh': 'กรุงศรีอยุธยา',
        },
        {
            'bankCode': '073',
            'shortCode': 'lh',
            'bankNameEn': 'Land and Houses Bank',
            'bankNameTh': 'แลนด์แอนด์เฮาส์',
        },
        {
            'bankCode': '069',
            'shortCode': 'KKP',
            'bankNameEn': 'Kiatnakin Phatra Bank',
            'bankNameTh': 'เกียรตินาคินภัทร',
        },
        {
            'bankCode': '017',
            'shortCode': 'CITI',
            'bankNameEn': 'Citibank',
            'bankNameTh': 'ซิตี้แบงก์',
        },
        {
            'bankCode': '067',
            'shortCode': 'TISCO',
            'bankNameEn': 'Tisco Bank',
            'bankNameTh': 'ทิสโก้',
        },
        {
            'bankCode': '034',
            'shortCode': 'BAAC',
            'bankNameEn': 'BAAC',
            'bankNameTh': 'เพื่อการเกษตรและสหกรณ์การเกษตร',
        },
        {
            'bankCode': '066',
            'shortCode': 'isl',
            'bankNameEn': 'Islamic Bank of Thailand',
            'bankNameTh': 'ธ.อิสลาม',
        },
        {
            'bankCode': '018',
            'shortCode': 'SMBC',
            'bankNameEn': 'Sumitomo Mitsui Banking Corporation (SMBC)',
            'bankNameTh': 'ซูมิโตโม มิตซุย',
        },
        {
            'bankCode': '031',
            'shortCode': 'HSBC',
            'bankNameEn': 'Hong Kong & Shanghai Corporation Limited (HSBC)',
            'bankNameTh': 'ฮ่องกงและเซี่ยงไฮ้ จำกัด',
        },
        {
            'bankCode': '033',
            'shortCode': 'GHB',
            'bankNameEn': 'Government Housing Bank (GHB)',
            'bankNameTh': 'อาคารสงเคราะห์',
        },
        {
            'bankCode': '039',
            'shortCode': 'MHCB',
            'bankNameEn': 'Mizuho Corporate Bank Limited (MHCB)',
            'bankNameTh': 'มิซูโฮ คอร์เปอเรท สาขากรุงเทพฯ',
        },
        {
            'bankCode': '070',
            'shortCode': 'ICBC',
            'bankNameEn': 'Industrial and Commercial Bank of China (thai) Public Company Limited',
            'bankNameTh': 'ไอซีบีซี (ไทย) จำกัด (มหาชน)',
        },
        {
            'bankCode': '071',
            'shortCode': 'TCRB',
            'bankNameEn': 'The Thai Credit Retail Bank Public Company Limited (TCRB)',
            'bankNameTh': 'ไทยเครดิตเพื่อรายย่อย จำกัด (มหาชน)',
        },
        {
            'bankCode': '032',
            'shortCode': 'DBAG',
            'bankNameEn': 'DEUTSCHE BANK AG',
            'bankNameTh': 'ดอยซ์แบงก์ เอจี',
        },
        {
            'bankCode': '052',
            'shortCode': 'BOC',
            'bankNameEn': 'Bank of China (Thai) Public Company Limited (BOC)',
            'bankNameTh': 'แห่งประเทศจีน (ไทย) จำกัด (มหาชน)',
        },
        {
            'bankCode': '079',
            'shortCode': 'ANZ',
            'bankNameEn': 'ANZ Bank (Thai) Public Company Limited',
            'bankNameTh': 'เอเอ็นแซด (ไทย) จำกัด (มหาชน)',
        },
        {
            'bankCode': '029',
            'shortCode': 'IOBA',
            'bankNameEn': 'INDIAN OVERSEAS BANK',
            'bankNameTh': 'อินเดียนโอเวอร์ซีร์',
        },
        {
            'bankCode': '045',
            'shortCode': 'BNP',
            'bankNameEn': 'BNP Paribas Bank',
            'bankNameTh': 'บีเอ็นพี พารีบาส์',
        }
    ]
    
    # Check if bank_name is already a bank code
    for bank in bank_mapping:
        if bankCode == bank['bankCode']:
            return bank['shortCode']
    
    return None


def filter_bank_bankNameTh(bankCode):
    """
    Function to filter bank name and return bank code
    
    Args:
        bank_name: Name of the bank in Thai or English, or bank code
        
    Returns:
        Bank code if found, None otherwise
    """
    # Define bank mapping
    bank_mapping = [
        {
            'bankCode': '030',
            'shortCode': 'GSB',
            'bankNameEn': 'Government Savings Bank',
            'bankNameTh': 'ออมสิน',
        },
        {
            'bankCode': '002',
            'shortCode': 'BBL',
            'bankNameEn': 'Bangkok Bank',
            'bankNameTh': 'กรุงเทพ',
        },
        {
            'bankCode': '004',
            'shortCode': 'KBANK',
            'bankNameEn': 'Kasikorn Bank',
            'bankNameTh': 'กสิกรไทย',
        },
        {
            'bankCode': '006',
            'shortCode': 'KTB',
            'bankNameEn': 'Krung Thai Bank',
            'bankNameTh': 'กรุงไทย',
        },
        {
            'bankCode': '011',
            'shortCode': 'TTB',
            'bankNameEn': 'TMBThanachart Bank',
            'bankNameTh': 'ทหารไทยธนชาต',
        },
        {
            'bankCode': '014',
            'shortCode': 'SCB',
            'bankNameEn': 'Siam Commercial Bank',
            'bankNameTh': 'ไทยพาณิชย์',
        },
        {
            'bankCode': '020',
            'shortCode': 'SCBT',
            'bankNameEn': 'Standard Chartered Bank (Thai)',
            'bankNameTh': 'แสตนดาร์ดชาร์เตอร์ (ไทย)',
        },
        {
            'bankCode': '022',
            'shortCode': 'CIMB',
            'bankNameEn': 'CIMB Thai Bank',
            'bankNameTh': 'ซีไอเอ็มบีไทย',
        },
        {
            'bankCode': '024',
            'shortCode': 'UOB',
            'bankNameEn': 'United Overseas Bank (Thai)',
            'bankNameTh': 'ยูโอบี',
        },
        {
            'bankCode': '025',
            'shortCode': 'BAY',
            'bankNameEn': 'Bank of Ayudhya',
            'bankNameTh': 'กรุงศรีอยุธยา',
        },
        {
            'bankCode': '073',
            'shortCode': 'LHB',
            'bankNameEn': 'Land and Houses Bank',
            'bankNameTh': 'แลนด์แอนด์เฮาส์',
        },
        {
            'bankCode': '069',
            'shortCode': 'KKP',
            'bankNameEn': 'Kiatnakin Phatra Bank',
            'bankNameTh': 'เกียรตินาคินภัทร',
        },
        {
            'bankCode': '017',
            'shortCode': 'CITI',
            'bankNameEn': 'Citibank',
            'bankNameTh': 'ซิตี้แบงก์',
        },
        {
            'bankCode': '067',
            'shortCode': 'TISCO',
            'bankNameEn': 'Tisco Bank',
            'bankNameTh': 'ทิสโก้',
        },
        {
            'bankCode': '034',
            'shortCode': 'BAAC',
            'bankNameEn': 'BAAC',
            'bankNameTh': 'เพื่อการเกษตรและสหกรณ์การเกษตร',
        },
        {
            'bankCode': '066',
            'shortCode': 'ISBT',
            'bankNameEn': 'Islamic Bank of Thailand',
            'bankNameTh': 'อิสลามแห่งประเทศไทย',
        },
        {
            'bankCode': '018',
            'shortCode': 'SMBC',
            'bankNameEn': 'Sumitomo Mitsui Banking Corporation (SMBC)',
            'bankNameTh': 'ซูมิโตโม มิตซุย แบงกิ้ง คอร์ปอเรชั่น',
        },
        {
            'bankCode': '031',
            'shortCode': 'HSBC',
            'bankNameEn': 'Hong Kong & Shanghai Corporation Limited (HSBC)',
            'bankNameTh': 'ฮ่องกงและเซี่ยงไฮ้ จำกัด',
        },
        {
            'bankCode': '033',
            'shortCode': 'GHB',
            'bankNameEn': 'Government Housing Bank (GHB)',
            'bankNameTh': 'อาคารสงเคราะห์',
        },
        {
            'bankCode': '039',
            'shortCode': 'MHCB',
            'bankNameEn': 'Mizuho Corporate Bank Limited (MHCB)',
            'bankNameTh': 'มิซูโฮ คอร์เปอเรท สาขากรุงเทพฯ',
        },
        {
            'bankCode': '070',
            'shortCode': 'ICBC',
            'bankNameEn': 'Industrial and Commercial Bank of China (thai) Public Company Limited',
            'bankNameTh': 'ไอซีบีซี (ไทย) จำกัด (มหาชน)',
        },
        {
            'bankCode': '071',
            'shortCode': 'TCRB',
            'bankNameEn': 'The Thai Credit Retail Bank Public Company Limited (TCRB)',
            'bankNameTh': 'ไทยเครดิตเพื่อรายย่อย จำกัด (มหาชน)',
        },
        {
            'bankCode': '032',
            'shortCode': 'DBAG',
            'bankNameEn': 'DEUTSCHE BANK AG',
            'bankNameTh': 'ดอยซ์แบงก์ เอจี',
        },
        {
            'bankCode': '052',
            'shortCode': 'BOC',
            'bankNameEn': 'Bank of China (Thai) Public Company Limited (BOC)',
            'bankNameTh': 'แห่งประเทศจีน (ไทย) จำกัด (มหาชน)',
        },
        {
            'bankCode': '079',
            'shortCode': 'ANZ',
            'bankNameEn': 'ANZ Bank (Thai) Public Company Limited',
            'bankNameTh': 'เอเอ็นแซด (ไทย) จำกัด (มหาชน)',
        },
        {
            'bankCode': '029',
            'shortCode': 'IOBA',
            'bankNameEn': 'INDIAN OVERSEAS BANK',
            'bankNameTh': 'อินเดียนโอเวอร์ซีร์',
        },
        {
            'bankCode': '045',
            'shortCode': 'BNP',
            'bankNameEn': 'BNP Paribas Bank',
            'bankNameTh': 'บีเอ็นพี พารีบาส์',
        }
    ]
    
    # Check if bank_name is already a bank code
    for bank in bank_mapping:
        if bankCode == bank['bankCode']:
            return bank['bankNameTh']
    
    return None

def transfer_money(device=None, pin=None, acc_number=None, amount=None, bank_name=None, time_out=60):

    package = "com.kasikorn.retail.mbanking.wap"

    """
    Function to transfer money to another bank account using K+ mobile banking app
    
    Args:
        device: Device ID to connect to. If None, connects to default device
        pin: PIN for K+ app authentication
        acc_number: Recipient account number
        amount: Amount to transfer
        bank_name: Name of recipient's bank
        time_out: Maximum time to wait for each step
        
    Returns:
        Reference number if transfer successful, None otherwise
    """
    # Connect to the specified device if provided

    adb = uiautomator2.connect(device)

    if adb.info['currentPackageName'] == "com.android.systemui":
        adb.screen_on()
        adb.swipe_ext(Direction.FORWARD)
    # Make sure the app is running
    if adb.info['currentPackageName'] != package:
        adb.app_start(package)

    bank_name_en = filter_bank_shortCode(bank_name)
    bank_name_th = filter_bank_bankNameTh(bank_name)
    
    # Step 1: Wait and click quick banking menu
    step1_start = time.time()
    while True:
        if time.time() - step1_start >= time_out:
            print("Timeout reached for Step 1")
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        
        print("Step 1")


        try:
            textview_message_dialog = adb(resourceId="com.kasikorn.retail.mbanking.wap:id/textview_message_dialog").get_text(timeout=0.5)
            print("textview_message_dialog:", textview_message_dialog)
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_confirm").click(timeout=0.5)
        except:
            pass

        try:
            transfer_text = adb(text="โอนเงิน").get_text(timeout=0.5)
            print("transfer_text:", transfer_text)
            break
        except:
            pass

        
        try:
            layout_quickBankingMenuCircle = adb(resourceId="com.kasikorn.retail.mbanking.wap:id/layout_quickBankingMenuCircle").get_text(timeout=0.5)
            print("layout_quickBankingMenuCircle:", layout_quickBankingMenuCircle)
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/layout_quickBankingMenuCircle").click(timeout=0.5)
            break
        except:
            pass
        
        time.sleep(0.5)


    # Step 3: Wait and click other bank account button
    
    while True:

        if time.time() - step1_start >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        
        print("Step 3")

        try:
            if adb(text="กรุณาใส่รหัสผ่าน").exists:
                print("กรุณาใส่รหัสผ่าน")
                for p in pin:
                    print(f"Entering PIN: {p}")
                    adb(resourceId=f"com.kasikorn.retail.mbanking.wap:id/linear_layout_button_activity_{p}").click()
                    time.sleep(0.5)
        except:
            pass

        try:
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/layout_quickBankingMenuCircle").click(timeout=0.1)
        except:
            pass

        try:
            adb(text="โอนเงิน").click(timeout=0.1)
        except:
            pass

        try:
            # bank_other = adb(text="บัญชีธนาคารอื่น").get_text(timeout=0.5)
            # print("bank_other:", bank_other)
            adb(text="บัญชีธนาคารอื่น").click(timeout=0.5)
            break
        except:
            pass

    

    # Step 4: Wait for search box and enter bank name
    
    while True:
        if time.time() - step1_start >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        print("Step 4")

        try:
            time.sleep(2)
            print("bank_name:", bank_name_en)
            adb.xpath('//*[@resource-id="com.kasikorn.retail.mbanking.wap:id/search_edit_text"]').click()
            time.sleep(1)
            # Using set_text instead of send_keys as the error shows send_keys is not a valid attribute
            element = adb.xpath('//*[@resource-id="com.kasikorn.retail.mbanking.wap:id/search_edit_text"]')
            element.set_text(bank_name_en)
            break
        except:
            pass
        

    
    
    while True:
        if time.time() - step1_start >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        
        print("Step 5")
        try:
            
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/merchant_name", text=bank_name_th).click()
            break
        except:
            pass

    # Step 6: Wait for account number input field and enter text
    
    while True:
        if time.time() - step1_start >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        try:
            if adb(text="กรอกเลขบัญชี").exists:
                adb(text="กรอกเลขบัญชี").set_text(acc_number)
                time.sleep(1)
                adb(description="ตกลง ").click()
                break
        except:
            pass

    # Step 7: Wait for amount input field and enter text
    
    while True:
        if time.time() - step1_start >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        try:
            if adb(text="กรอกจำนวนเงิน").exists:
                adb(text="กรอกจำนวนเงิน").set_text(amount)
                time.sleep(1)
                adb(description="ตกลง ").click()
                break
        except:
            pass
    # Step 8: Click next button
    
    while True:
        if time.time() - step1_start >= time_out:
            print("Timeout reached for Step 8")
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        
        try:
            # Add a small delay to prevent excessive CPU usage
            time.sleep(0.5)
            
            if adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_navigation_next").exists:
                adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_navigation_next").click()
                time.sleep(1)  # Give time for the app to respond
                break
        except Exception as e:
            print(f"Error in Step 8: {e}")
            time.sleep(1)  # Add delay on exception

    # Step 9: Click next button again to confirm
    
    while True:
        if time.time() - step1_start >= time_out:
            print("Timeout reached for Step 9")
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        
        try:
            # First try to click confirm button if it exists
            if adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_confirm").exists:
                adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_confirm").click()
                time.sleep(1)  # Give time for the app to respond
        except Exception as e:
            print(f"Error with confirm button: {e}")
            time.sleep(0.5)

        try:
            # Then try to click next button
            if adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_navigation_next").exists:
                adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_navigation_next").click()
                time.sleep(1)  # Give time for the app to respond
                break
        except Exception as e:
            print(f"Error with next button: {e}")
            time.sleep(1)  # Add delay on exception

    # Check for successful transfer message
    
    while True:
        if time.time() - step1_start >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        try:
            if adb(text="โอนเงินสำเร็จ").exists:
                ref = adb(resourceId="com.kasikorn.retail.mbanking.wap:id/textView_finance_number").get_text()
                print("ref:", ref)
                print("โอนเงินสำเร็จ")
                adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageView_bottom_menu_home").click()

                data_json = {
                    "from":"",
                    "to":acc_number,
                    "amount":amount,
                    "fee":"0.00",
                    "number":ref,
                }
                return {"status":True,"msg":data_json}
        except:
            pass
    


def transfer_money_loop(transfer_list=None, device=None, pin="000009", time_out=60):
    """
    Function to transfer money to multiple bank accounts using K+ mobile banking app
    
    Args:
        transfer_list: List of dictionaries containing transfer details
                      [{"acc_number": "1234567890", "amount": "10", "bank_name": "กรุงไทย"}, ...]
        device: Device ID to connect to. If None, connects to default device
        pin: PIN for K+ app authentication
        time_out: Maximum time to wait for each step
        
    Returns:
        Dictionary with account numbers as keys and reference numbers as values
        If transfer fails, the value will be None
    """
    if transfer_list is None or len(transfer_list) == 0:
        print("No transfers specified")
        return {}
    
    results = {}
    
    for transfer in transfer_list:
        acc_number = transfer.get("acc_number")
        amount = transfer.get("amount")
        bank_name = transfer.get("bank_name")
        if bank_name:
            bank_name_th = filter_bank_shortCode(bank_name)
            if bank_name_th:
                bank_name = bank_name_th
        
        if not all([acc_number, amount, bank_name]):
            print(f"Skipping incomplete transfer: {transfer}")
            continue
            
        print(f"Transferring {amount} to {acc_number} ({bank_name})")
        ref = transfer_money(
            device=device,
            pin=pin,
            acc_number=acc_number,
            amount=amount,
            bank_name=bank_name,
            time_out=time_out
        )
        
        results[acc_number] = ref
        
        if ref:
            print(f"Transfer to {acc_number} successful, reference: {ref}")
        else:
            print(f"Transfer to {acc_number} failed")
        
    
    return results




def close_all_apps(d):
    """
    Closes all apps in the recent apps screen except for those in the excluded_apps list.
    
    :param excluded_apps: A list of apps (package names) to exclude from being closed.
                          If None, defaults to ['com.termux'].
    """


    # Connect to the device (replace 'your_device_ip' with your device's IP address if necessary)
    # Go to the home screen
    d.press('home')
    # Press the "Recent Apps" button to show all running apps
    d.press('recent')
    # Give some time for the recent apps to load
    time.sleep(1)
    d(resourceId=f"com.miui.home:id/clearAnimView").click()

def get_ui_elements_info(device):
    # Dump the UI hierarchy (XML format)
    ui_hierarchy = device.dump_hierarchy()
    # Convert the XML hierarchy to a Python dictionary using xmltodict
    ui_dict = xmltodict.parse(ui_hierarchy)
    # Convert the dictionary to JSON (you can also keep it as dict if you don't need JSON specifically)
    # ui_json = json.dumps(ui_dict, indent=4, ensure_ascii=False)
    return ui_dict  # Return JSON formatted UI data



@app.route("/infoapp", methods=["GET", "POST"])
def infoapp():
    data = request.args
    device_id = data.get("device")  # Get the device ID from the request

    device_id = request.args.get("device")
    if not device_id:
        devices = get_devices_all()
        device_id = devices[0]

    # Connect to the Android device using the provided device ID
    try:
        adb = uiautomator2.connect(device_id)
    except Exception as e:
        return {"status": False, "msg": f"Failed to connect to the device: {str(e)}"}

    # Get UI element details, including XPath and other properties
    try:
        data = get_ui_elements_info(adb)
    except Exception as e:
        return {"status": False, "msg": f"Failed to get UI elements info: {str(e)}"}

    return {"status": True, "msg": data}
# package = "com.kasikorn.retail.mbanking.wap"
# name_adb = "WWTWDQ4XX48XIBTO"
# url = ""
# adb = uiautomator2.connect(name_adb)
# adb.open_url(url)
#http://192.168.0.63:56485?device=WWTWDQ4XX48XIBTO&token=KMBCYB000000000CBDCC53FC8E84BFF82D0A21FFFCC529A
#https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/KMBCYB000000000CBDCC53FC8E84BFF82D0A21FFFCC529A
@app.route("/devices",methods=["GET"])
def get_devices_all():
    main_adb = LibAdb()
    data_adb = main_adb.list_adb()
    return  data_adb

@app.route("/unlock",methods=["GET","POST"])
def unlock():
    device = request.args.get("device")
    if not device:
        devices = get_devices_all()
        device = devices[0]
    adb = uiautomator2.connect(device)
    adb.screen_on()
    adb.swipe_ext(Direction.FORWARD)
    return  {"status":True,"msg":'ปลดล็อก สำเร็จ'}

@app.route("/lock",methods=["GET","POST"])
def lock():
    device = request.args.get("device")
    if not device:
        devices = get_devices_all()
        device = devices[0]
    adb = uiautomator2.connect(device)
    adb.screen_off()
    return  {"status":True,"msg":'ล็อก สำเร็จ'}

@app.route("/clearall",methods=["GET","POST"])
def clearall():
    device = request.args.get("device")
    if not device:
        devices = get_devices_all()
        device = devices[0]
    adb = uiautomator2.connect(device)
    close_all_apps(adb)
    return  {"status":True,"msg":'clear สำเร็จ'}

@app.route("/clear",methods=["GET","POST"])
def clearone():
    device = request.args.get("device")
    if not device:
        devices = get_devices_all()
        device = devices[0]
    adb = uiautomator2.connect(device)
    close_unwanted_apps(adb)
    return  {"status":True,"msg":'clear สำเร็จ'}


@app.route("/info",methods=["GET","POST"])
def info():
    try:
        device = request.args.get("device")
        if not device:
            devices = get_devices_all()
            device = devices[0]
        adb = uiautomator2.connect(device)
        return  {"status":True,"msg":adb.info}
    except:
        return  {"status":False,"msg":"ไม่สามารถทำงานได้"}

@app.route("/verifyphone",methods=["GET"])
def verifyphone():
    start_time = time.time()
    time_out = 60
    device = request.args.get("device")
    if not device:
        devices = get_devices_all()
        device = devices[0]
    package = "com.kasikorn.retail.mbanking.wap"
    adb = uiautomator2.connect(device)
    adb.app_start(package)
    while True:
        
        if time.time() - start_time >= time_out:
            adb.app_stop(package)
            return {"status":False,"msg":"time_out"}
        
        try:
            footer_bank_textview = adb(text="ธุรกรรม").get_text(timeout=0.1)
            print(footer_bank_textview)
            adb.app_stop(package)
            return  {"status":True,"msg":'อัพเดทสำเร็จ'}
        except:
            pass

        try:
            complete_back_button = adb(text="อัปเดตเบอร์มือถือ").get_text(timeout=0.1)
            print(complete_back_button)
            break
        except:
            pass
    time.sleep(1)
    adb(resourceId=f"com.kasikorn.retail.mbanking.wap:id/complete_back_button").click()
    adb.app_stop(package)
    return  {"status":True,"msg":'อัพเดทสำเร็จ'}

@app.route("/transfer",methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        data = request.json
    else:
        data = request.args
    device = data.get("device")
    pin = data.get("pin")
    acc_to = data.get("acc_to")
    amount = data.get("amount")
    bank_name = data.get("bankcode")


    if not device:
        devices = get_devices_all()
        device = devices[0]


    return transfer_money(device=device, pin=pin, acc_number=acc_to, amount=amount, bank_name=bank_name)

    



@app.route("/",methods=["GET", "POST"])
def index():
    global data_adb
    try:
        start_time = time.time()
        time_out = 60
        data = request.args

        device = request.args.get("device")
        if not device:
            devices = get_devices_all()
            device = devices[0]
        token = data["token"]
        link = f"https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/{token}"
        pin = "112233"
        if device not in data_adb:
            return {"status":False,"msg":"check name device"}
        package = "com.kasikorn.retail.mbanking.wap"
        adb = uiautomator2.connect(device)
        print(adb.info)
        if adb.info['currentPackageName'] == "com.android.systemui":
            adb.screen_on()
            adb.swipe_ext(Direction.FORWARD)
            # run_adb_command("input keyevent KEYCODE_WAKEUP")  # Turn on the screen
            # run_adb_command("input swipe 300 1000 300 500")  # Swipe up (for swipe unlock)
        close_unwanted_apps(adb)
        adb.app_stop(package)
        adb.open_url(link)
        while True:
            if time.time() - start_time >= time_out:
                adb.app_stop(package)
                return {"status":False,"msg":"time_out"}

            try:
                adb(text="ขออภัย").get_text(timeout=0.1)
                adb.app_stop(package)
                return {"status":False,"msg":"check token"}
            except:
                pass

            try:
                adb.xpath('//*[@resource-id="com.kasikorn.retail.mbanking.wap:id/imageview_navigation_next"]').click()
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
                return {"status":False,"msg":"time_out"}
            try:
                adb(text="ยืนยันรายการ").get_text(timeout=0.1)
                data_info = adb(className="android.widget.TextView")
                print(data_info.count)
                data_json = {
                    "from":data_info[-5].get_text(),
                    "to":data_info[-4].get_text(),
                    "amount":data_info[-3].get_text(),
                    "fee":data_info[-2].get_text(),
                    "number":data_info[-1].get_text(),
                }
                break
            except:
                pass

        while True:
            if time.time() - start_time >= time_out:
                adb.app_stop(package)
                return {"status":False,"msg":"time_out"}
            try:
                adb(text="ยืนยัน").click(timeout=0.5)
            except:
                pass
            try:
                adb(text="ดำเนินการเสร็จสิ้น").get_text(timeout=0.1)
                time.sleep(1)
                adb.app_stop(package)
                return {"status":True,"msg":data_json}
            except:
                pass
    except Exception as e:
        return {"status":False,"msg":f"error : {e}"}







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=56485)

# {'errorCode': '00', 'qrBase64': 'data:image/png;base64,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', 'tokenId': 'KMBCYB0000000001F8AC5280A2D44C2BE4F7F8F100DB6A8', 'link': 'https://kplus.kasikornbank.com/authenwithkplus/?tokenId=KMBCYB0000000001F8AC5280A2D44C2BE4F7F8F100DB6A8&nextAction=authenwithkplus', 'expQr': '6', 'transType': 'FTOT', 'transferType': 'Online', 'bulk': 'N', 'fromAccountNo': '1178114472', 'fromAccountNoMasking': 'xxx-x-x1447-x', 'fromAccountName': 'นาย สรศักดิ์ ธุระหาย', 'beneficiaryNo': '1761711527', 'beneficiaryNoMasking': '176-1-71152-7', 'beneficiaryName': 'MRS. NOUTHIP VONGVANE', 'amount': '3', 'feeAmount': '0', 'totalAmount': '3', 'transStatus': 'S', 'effectiveDate': '2024-07-26 15:20:18.178', 'lang': 'th', 'memo': '', 'memoTypeId': '12', 'notiEmailNote': '', 'errorMsg': 'Success', 'reqRefNo': 'TRBS240726964088208', 'scheduleFlag': 'N', 'rqUID': '069_20240726_8FE3D9FE3CAB4183B9732524E98B74EA', 'attachFileName': '', 'smsLang': 'th', 'createDate': '2024-07-26 15:20:18.178', 'beneficiaryNoMaskingSms': 'xxx-x-x1152-x', 'bankCode': '004'}
# https://kpaymentgateway-services.kasikornbank.com/KPGW-Redirect-Webapi/Appswitch/KMBCYB0000000001F8AC5280A2D44C2BE4F7F8F100DB6A8
