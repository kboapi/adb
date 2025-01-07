import uiautomator2 as u2
import subprocess
import time

d = u2.connect()


# def transfer_money(pin,bank_name, account_number, amount):
#     d.app_start("com.kasikornbank.kbiz")
#     while True:

#         try:
#             d.xpath('//*[@content-desc="เข้าสู่ระบบ"]').click()
#         except:
#             pass


#         try:
#             for digit in pin:
#                 d.xpath(f'//*[@content-desc="{digit}"]').click()
#         except:
#             pass
       

#         try:
#             d.xpath('//*[starts-with(@content-desc,"ธุรกรรม")]').click()
#         except:
#             pass

#         try:
#             d.xpath('//*[@content-desc="โอนเงิน"]').click()
#             print("โอนเงิน")
#         except:
#             pass


#         try:
#             if d(textStartsWith=f"ธนาคารกสิกรไทย").exists:
#                 d(textStartsWith=f"ธนาคารกสิกรไทย").click()
#                 print("ธนาคารถูกต้อง")
#             else:
#                 d(textStartsWith=f" ธนาคารกสิกรไทย").click()
#             elements = d.xpath('//android.widget.EditText').all()

#             #พิมพ์ธนาคาร
#             elements[4].click()
#             d.send_keys(bank_name)


#             #พิมพ์เลขบัญชี
#             elements[0].click()
#             d.send_keys(account_number)


#             #พิมพ์จำนวนเงิน
#             elements[1].click()
#             d.send_keys(amount)


#             d.swipe(461, 1322,461, 524, 0.5)

#             d(text="ต่อไป").click()
#             time.sleep(2)
#             d.swipe(461, 1322,461, 524, 0.5)
#             d.swipe(461, 1322,461, 524, 0.5)
#             time.sleep(1)
#             d.click(521,1458)

#             time.sleep(2)
#         except:
#             pass


#         try:
#             d.xpath('//*[@content-desc="ยืนยัน"]').click()
#             print("ยืนยันสำเร็จ")

#             while(True):
#                 try:
#                     d(text="โอนเงินสำเร็จ").get_text(timeout=0.5)
#                     print("โอนเงินสำเร็จ")
#                     break
#                 except:
#                     pass
#             break
#         except:
#             pass

        

#     d.app_stop("com.kasikornbank.kbiz")
# # รายการบัญชีที่ต้องการโอน
# accounts = [
#     {"bank": "ไทยพาณิชย์", "account": "4096530952", "amount": 0.13},
#     {"bank": "กสิกรไทย", "account": "1941694183", "amount": 0.05}, 
#     {"bank": "กรุงศรี", "account": "0421751829", "amount": 0.05}
# ]
# # วนลูปโอนเงินทุกบัญชี
# for acc in accounts:
#     transfer_money("230419",acc["bank"], acc["account"], acc["amount"])
#     time.sleep(3) # รอระหว่างการโอนแต่ละรายการ




account_number = "1941694183"

bank_name = "ไทยพาณิชย์"

amount = "0.05"

Spinners = d.xpath('//android.widget.Spinner').all()
Spinners[1].click()
time.sleep(2)
elements = d.xpath('//android.widget.EditText').all()
# #พิมพ์ธนาคาร
elements[2].click()
d.send_keys(bank_name)
d.click(150,1024)

time.sleep(1)
elements[0].click()
d.send_keys(account_number)

time.sleep(1)
elements[1].click()
d.send_keys(amount)

