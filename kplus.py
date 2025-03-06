import uiautomator2 as u2
import subprocess
import time
from uiautomator2 import Direction


adb = u2.connect()
print(adb.info)
if adb.info['currentPackageName'] == "com.android.systemui":
    adb.screen_on()
    adb.swipe_ext(Direction.FORWARD)

package = "com.kasikorn.retail.mbanking.wap"
adb.app_start(package)


def filter_bank_shortCode(shortCode):
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
        if shortCode == bank['shortCode']:
            return bank['bankNameTh']
    
    # Check if bank_name matches any Thai or English name or short code
    for bank in bank_mapping:
        if (shortCode.lower() in bank['bankNameTh'].lower() or 
            shortCode.lower() in bank['bankNameEn'].lower() or 
            shortCode.upper() == bank['shortCode']):
            return bank['bankNameTh']
    
    # If no match found
    return None

def transfer_money(device=None, pin="000009", acc_number="0000000000", amount="10", bank_name="กรุงไทย", time_out=60):
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
    global adb
    if device:
        adb = u2.connect(device)
    
    # Make sure the app is running
    if adb.info['currentPackageName'] != package:
        adb.app_start(package)

    if bank_name:
        bank_name_th = filter_bank_shortCode(bank_name)
        if bank_name_th:
            bank_name = bank_name_th
        
    
    # Step 1: Wait and click quick banking menu
    step1_start = time.time()
    while True:
        if time.time() - step1_start >= time_out:
            print("Timeout reached for Step 1")
            adb.app_stop(package)
            return None
        
        print("Step 1")


        try:
            textview_message_dialog = adb(resourceId="com.kasikorn.retail.mbanking.wap:id/textview_message_dialog").get_text(timeout=0.5)
            print("textview_message_dialog:", textview_message_dialog)
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageview_confirm").click(timeout=0.5)
        except:
            pass


        
        try:
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/layout_quickBankingMenuCircle").click(timeout=0.5)
            break
        except:
            pass

        try:
            transfer_text = adb(text="โอนเงิน").get_text(timeout=0.5)
            print("transfer_text:", transfer_text)
            adb(text="โอนเงิน").click(timeout=0.5)
            break
        except:
            pass

        time.sleep(0.1)

      
       

    # Step 3: Wait and click other bank account button
    step3_start = time.time()
    while True:
        if time.time() - step3_start >= time_out:
            adb.app_stop(package)
            return None
        try:
            pin_get = adb(text="กรุณาใส่รหัสผ่าน").get_text(0.5)
            print("pin_get:", pin_get)
            print("Entering PIN")
            for p in pin:
                time.sleep(0.1)
                print(f"Entering PIN: {p}")
                adb(resourceId=f"com.kasikorn.retail.mbanking.wap:id/linear_layout_button_activity_{p}").click()
                time.sleep(0.1)
        except:
            pass

        try:
            bank_other = adb(text="บัญชีธนาคารอื่น").get_text(timeout=0.5)
            print("bank_other:", bank_other)
            adb(text="บัญชีธนาคารอื่น").click(timeout=0.5)
        except:
            pass

        try:
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/search_edit_text").click(timeout=1)
            break
        except:
            pass

    # Step 4: Wait for search box and enter bank name
    step4_start = time.time()
    while True:
        if time.time() - step4_start >= time_out:
            adb.app_stop(package)
            return None
        try:
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/search_edit_text").set_text(bank_name)
            break
        except:
            pass

    # Step 5: Wait and click bank option
    step5_start = time.time()
    while True:
        if time.time() - step5_start >= time_out:
            adb.app_stop(package)
            return None
        try:
            adb(resourceId="com.kasikorn.retail.mbanking.wap:id/merchant_name", text=bank_name).click()
            break
        except:
            pass

    # Step 6: Wait for account number input field and enter text
    step6_start = time.time()
    while True:
        if time.time() - step6_start >= time_out:
            adb.app_stop(package)
            return None
        try:
            if adb(text="กรอกเลขบัญชี").exists:
                adb(text="กรอกเลขบัญชี").set_text(acc_number)
                time.sleep(1)
                adb(description="ตกลง ").click()
                break
        except:
            pass

    # Step 7: Wait for amount input field and enter text
    step7_start = time.time()
    while True:
        if time.time() - step7_start >= time_out:
            adb.app_stop(package)
            return None
        try:
            if adb(text="กรอกจำนวนเงิน").exists:
                adb(text="กรอกจำนวนเงิน").set_text(amount)
                time.sleep(1)
                adb(description="ตกลง ").click()
                break
        except:
            pass
    # Step 8: Click next button
    step8_start = time.time()
    while True:
        if time.time() - step8_start >= time_out:
            print("Timeout reached for Step 8")
            adb.app_stop(package)
            return None
        
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
    step9_start = time.time()
    while True:
        if time.time() - step9_start >= time_out:
            print("Timeout reached for Step 9")
            adb.app_stop(package)
            return None
        
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
    step10_start = time.time()
    while True:
        if time.time() - step10_start >= time_out:
            adb.app_stop(package)
            return None
        try:
            if adb(text="โอนเงินสำเร็จ").exists:
                ref = adb(resourceId="com.kasikorn.retail.mbanking.wap:id/textView_finance_number").get_text()
                print("ref:", ref)
                print("โอนเงินสำเร็จ")
                adb(resourceId="com.kasikorn.retail.mbanking.wap:id/imageView_bottom_menu_home").click()
                return ref
        except:
            pass
    
    return None

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



# Example usage
if __name__ == "__main__":


    transfer_money(device=None, pin="251899", acc_number="1941694183", amount="1.3", bank_name="KBANK")
    # transfer_list = [
    #     # {"acc_number": "1941694183", "amount": "2", "bank_name": "KBANK"},
    #     # {"acc_number": "4096530952", "amount": "1.2", "bank_name": "SCB"},
    #     # {"acc_number": "1941694183", "amount": "2.1", "bank_name": "KBANK"},
    #     # {"acc_number": "4096530952", "amount": "2.3", "bank_name": "SCB"},
    #     # {"acc_number": "1941694183", "amount": "2.4", "bank_name": "KBANK"},
    #     {"acc_number": "0377431218", "amount": "1.3", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "1.2", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "1.5", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "1.6", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "1.7", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "1.8", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "1.9", "bank_name": "BBL"},
    #     {"acc_number": "0377431218", "amount": "2", "bank_name": "BBL"},
    # ]

    # results = transfer_money_loop(transfer_list)
    # print("Transfer results:", results)
    
    # # Keep the script running to prevent immediate exit
    # try:
    #     print("Script completed. Press Ctrl+C to exit.")
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("Script terminated by user")
