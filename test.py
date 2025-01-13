import uiautomator2 as u2
import subprocess
import time
import xmltodict
#Connect to the device
d = u2.connect()




d.xpath('//*[@resource-id="com.kasikorn.retail.mbanking.wap:id/imageview_navigation_next"]').click()


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

