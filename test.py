import uiautomator2 as u2
import subprocess
import time
import xmltodict
#Connect to the device
d = u2.connect()

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



print(filter_bank_shortCode("004"))
# element = adb.xpath('//*[@resource-id="com.kasikorn.retail.mbanking.wap:id/search_edit_text"]')
# element.set_text("กสิกรไทย")

# d.app_start("com.kasikornbank.kbiz")
# while True:
    
#     if d.xpath('//*[@content-desc="ใช่"]').exists:
#         d.xpath('//*[@content-desc="ใช่"]').click()
        
#     elif d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').exists:
#         d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').click()
        
#     elif d.xpath('//*[@content-desc="ใส่รหัส PIN"]').exists:
#         print("ใส่รหัส PIN")
#         break

# while True:
#     if d.xpath('//*[@content-desc="1"]').exists:
#         for digit in "080564":
#             d.xpath(f'//*[@content-desc="{digit}"]').click()
#             time.sleep(0.2)

#         break



# while True:
#     try:
#         d.xpath('//*[starts-with(@content-desc,"ธุรกรรม")]').click()
#         time.sleep(0.1)
#     except:
#         pass

#     try:
#         d.xpath('//*[@content-desc="โอนเงิน"]').click()
#         print("โอนเงิน")
#         break
#     except:
#         pass



# while True:
#     try:
#         d.xpath('//*[@content-desc="โอนเงิน"]').click()
#         print("เข้าหน้าโอนเงิน")
#         break
#     except:
#         pass
# time.sleep(2)

# d.click(156,1115)



# bank = "ไทยพาณิชย์"


# d.click(156,702)
# d.click(156,702)
# d.send_keys(f"{bank}")
# time.sleep(2)
# d.click(150,1024)
# time.sleep(2)
# d.click(112,1273)
# d.send_keys("4096530952")

# time.sleep(2)

# d.click(126,1032)
# time.sleep(2)
# d.send_keys("1.11")

# d.swipe(461, 1322,461, 524, 0.5)

# d(text="ต่อไป").click()

# time.sleep(2)
# d.swipe(461, 1322,461, 524, 0.5)
# d.swipe(461, 1322,461, 524, 0.5)


# d.click(521,1458)

# while True:
#     try:
#         d.xpath('//*[@content-desc="ยืนยัน"]').click()
#         print("ยืนยันสำเร็จ")
#         break
#     except:
#         pass


# while True:
#     try:
#         d(text="โอนเงินสำเร็จ").get_text(timeout=0.1)
#         print("โอนเงินสำเร็จ")
#     except:
#         pass

# d.app_stop("com.kasikornbank.kbiz")





def transfer_money(bank_name, account_number, amount):
    d.app_start("com.kasikornbank.kbiz")
    while True:
        
        if d.xpath('//*[@content-desc="ใช่"]').exists:
            d.xpath('//*[@content-desc="ใช่"]').click()
            
        elif d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').exists:
            d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').click()

        elif d.xpath('//*[@content-desc="ใส่รหัส PIN"]').exists:
            print("ใส่รหัส PIN")
            break

    while True:
        if d.xpath('//*[@content-desc="1"]').exists:
            for digit in "230419":
                d.xpath(f'//*[@content-desc="{digit}"]').click()
                time.sleep(0.2)

            break
    time.sleep(2)

    # if d.xpath('//*[@content-desc="ปิด"]').exists:
    #         d.xpath('//*[@content-desc="ปิด"]').click()
    #         print("ปิด")
    #         while True:
    #             if d.xpath('//*[@content-desc="ใช่"]').exists:
    #                 d.xpath('//*[@content-desc="ใช่"]').click()
                    
    #             elif d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').exists:
    #                 d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').click()

    #             elif d.xpath('//*[@content-desc="ใส่รหัส PIN"]').exists:
    #                 print("ใส่รหัส PIN")
    #                 break



    while True:
        try:
            d.xpath('//*[starts-with(@content-desc,"ธุรกรรม")]').click()
            time.sleep(0.1)
        except:
            pass

        try:
            d.xpath('//*[@content-desc="โอนเงิน"]').click()
            print("โอนเงิน")
            break
        except:
            pass



    while True:
        try:
            d.xpath('//*[@content-desc="โอนเงิน"]').click()
            print("เข้าหน้าโอนเงิน")
            break
        except:
            pass
    time.sleep(2)

    d.click(156,1115)

    d.click(156,702)
    d.click(156,702)
    d.send_keys(f"{bank_name}")
    time.sleep(2)
    d.click(150,1024)
    time.sleep(2)
    d.click(112,1273)
    d.send_keys(account_number)

    time.sleep(2)

    d.click(126,1032)
    time.sleep(2)
    d.send_keys(str(amount))

    d.swipe(461, 1322,461, 524, 0.5)

    d(text="ต่อไป").click()

    time.sleep(2)
    d.swipe(461, 1322,461, 524, 0.5)
    d.swipe(461, 1322,461, 524, 0.5)
    time.sleep(1)
    d.click(521,1458)

    time.sleep(2)
    while True:
        try:
            d.xpath('//*[@content-desc="ยืนยัน"]').click()
            print("ยืนยันสำเร็จ")
            break
        except:
            pass

    while True:
        try:
            d(text="โอนเงินสำเร็จ").get_text(timeout=0.1)
            print("โอนเงินสำเร็จ")
            break
        except:
            pass

# รายการบัญชีที่ต้องการโอน
accounts = [
    {"bank": "ไทยพาณิชย์", "account": "4096530952", "amount": 0.01},
    {"bank": "กสิกรไทย", "account": "1941694183", "amount": 0.02}, 
    {"bank": "กรุงศรี", "account": "0421751829", "amount": 0.03}
]

# วนลูปโอนเงินทุกบัญชี
for acc in accounts:
    transfer_money(acc["bank"], acc["account"], acc["amount"])
    
    d.app_stop("com.kasikornbank.kbiz")
    time.sleep(3) # รอระหว่างการโอนแต่ละรายการ

