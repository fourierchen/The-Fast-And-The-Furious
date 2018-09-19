from PIL import ImageGrab, ImageChops, Image
import numpy as np
import cv2
import win32gui
import pyautogui
import time
import sys
from datetime import datetime
pyautogui.FAILSAFE = True
hwnd = win32gui.FindWindow(None, '京彩 - Google Chrome')
try :
    left_x, left_y, right_x, right_y = win32gui.GetWindowRect(hwnd)
except :
    print("no catch!")

#找位置
'''
while True:
    x, y = pyautogui.position()
    print(x, y)
    time.sleep(2)
'''
#數字顏色
# 1 148 161 161
# 2 250 0 78
# 3 255 70 66
# 4 247 164 92
# 5 0 211 130
# 6 8 193 228
# 7 169 38 225
# 8 57 115 224
# 9 102 115 137
# 10 54 54 54
'''
while True:
    x, y = pyautogui.position()
    print(x, y)
    
    img = ImageGrab.grab(bbox = (left_x, left_y, right_x, right_y))
    img_np = np.array(img)
    color_want = img_np[263, 507, :]
    print(color_want)
    time.sleep(3)
    
    img_np[263,507,:] = 0
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    cv2.imshow("screen box", frame)
    cv2.waitKey(0)
    
'''
def correct_or_not(flag, open_result, i_vote, rate):
    print("correct or not")
    if open_result == i_vote:
        flag = True
        rate = 1
        print('correct!!!')
    else:
        flag = False
        rate *= 2
        print('fail!!!')

    return flag, rate

def update_result(color_map, open_result):
    print("update result")
   #img = ImageGrab.grab(bbox = (left_x, left_y, right_x, right_y))
    img = ImageGrab.grab(bbox = (0, 0, 2440, 1440))
    img_np = np.array(img)
    color_want = img_np[372, 768, :] # y , x
    color_want = color_want.tolist()
    print(color_want)
   # pyautogui.moveTo(768, 372)
    true_num = color_map.index(color_want) + 1
    print('open number :',true_num,'I will vote :', true_num % 2) # 1=單 2=雙   
    # get open_result 
    if true_num % 2 == 0:
        open_result = False
    else:
        open_result = True
    time.sleep(1)
    
    return open_result

def move_to_vote(flag, open_result, i_vote, rate):
    print('vote time!')
    if open_result == True: #單
        i_vote = open_result
        print('vote single')
        pyautogui.moveTo(918, 758) # 單
        pyautogui.click()
    else:
        i_vote = open_result
        print('vote double')
        pyautogui.moveTo(1124, 758) # 雙
        pyautogui.click()
    
    time.sleep(1)
    pyautogui.moveTo(2360, 365)
    pyautogui.click()
    pyautogui.press('backspace')
    time.sleep(1)
    pyautogui.typewrite(str(rate))
    print('vote :', rate*5)
    pyautogui.moveTo(2373, 571)  #下注
    time.sleep(1)
    pyautogui.click()
    pyautogui.moveTo(1101, 872)  #確認下注
    time.sleep(1)
    pyautogui.click()
    time.sleep(0.3)
    pyautogui.moveTo(1275, 836)  #知道了
    time.sleep(1.5)
    pyautogui.click()

    return i_vote

def refresh():
    pyautogui.moveTo(1220, 382)
    pyautogui.click()

    
# 整點開始下注，45秒時封盤
# 算時間
# main
# init 上一次的結果是單 下單數 一倍
flag = True
open_result = True # 單
i_vote = True # 單
rate = 1
yes_count = 0
no_count = 0
color_map = [[149, 161, 161], [238, 20, 83], [244, 74, 73], [240, 165, 96], [70, 210, 129], [70, 193, 227], [164, 44, 224], [71, 115, 223], [104, 115, 137], [54, 54, 54]]

# init
refresh()
time.sleep(2)
open_result = update_result(color_map, open_result)
i_vote = open_result
i_vote = move_to_vote(flag, open_result, i_vote, rate)

# start loop
time_flag = True
while time_flag:
    now = datetime.now()
    #print(now.second)
    if now.second == 5: # 五秒時開始下注
        print('-----------------------------------------------------')
        print('start bot!')
        refresh()
        time.sleep(2)
        open_result = update_result(color_map, open_result)
        flag, rate = correct_or_not(flag, open_result, i_vote, rate)

        # 統計有沒有中, 有中把fail歸零
        if flag == True:
            yes_count += 1
            print('success :', yes_count)
            no_count = 0
            if yes_count == 10:   #跑幾次後停止
                time_flag = False
                continue
        else:
            no_count += 1
            print('fail :', no_count)
            if no_count == 10:
                time_flag = False
                continue

        i_vote = move_to_vote(flag, open_result, i_vote, rate)

        
    else:
        time.sleep(0.5)
   
