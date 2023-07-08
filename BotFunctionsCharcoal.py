from pyautogui import *
import pyautogui
import time
import win32api, win32con, win32gui
from random import randint
import pytesseract
from PIL import ImageGrab
import cv2
import numpy as nm

#812, 216, 980, 250 - Check name Full HD
#1695, 694, 1850, 800 - Check 'locked in' and 'confirmed' Full HD
#962, 165, 1403, 984 - items Full HD
#1498, 521, 1887, 617 - buttons Full HD
#1444, 322 - coordinates for putting items Full HD
#1238, 23, 1765, 216 - step Full HD

#for text recognition
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#delete old history write today's date + all nicknames
def date(server, x1, x2, x3, x4):

      #if today's date and names of the server already in file, return none
      with open('Transaction_history.txt', 'r') as f:
            data = f.readlines()
            today = datetime.datetime.today()
            date = today.strftime("%b-%d-%Y")
            try:
                  if (data.index(server + '\n') and
                      data.index(date + '\n')):
                        return None
            except:
                  pass
                                              
      #write today's date    
      with open('Transaction_history.txt', 'a+') as f:
            today = datetime.datetime.today()
            d = today.strftime("%b-%d-%Y")
            f.seek(0)
            f.write('\n' + '-' * 10 + "Last session" +\
                    '-' * 10 + '\n' + d + '\n' + str(server) +\
                    '\n' + '-' * 10 + '\n')
            f.close()

      #delete what's before first apperance of today's date     
      with open('Transaction_history.txt') as f:
          data = list(f.readlines())
          date = today.strftime("%b-%d-%Y")
          count = data.index(date+'\n')
          del data[0:count - 1]
          with open('Transaction_history.txt', 'w') as f:
              for i in data:
                  f.write(i)
          f.close()

      #write names of the server
      with open('Transaction_history.txt', 'a') as f:
            names = x1 + x2 + x3 + x4
            f.seek(0)
            for i in names:
                  f.write(i+'\n')
            f.close()
                  

#all nicknames
def list_of_nicknames(list):
      return    list 

#function for click into found item
def click(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(.1)
    pyautogui.click()
    
#function for double click
def double_click(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(.1)
    pyautogui.click()
    pyautogui.click()

    
#1250, 280, 2000, 1400 - items
#2007, 722, 2500, 800 - buttons
#1650, 0, 2500, 400 - step
#2184, 934, 2500, 1100 - for accept trade check of 'locked in' and 'confirmed'
#function for check if the item is on the screen
def check(item , x, y, w, h):
 a = 0
 test =[]
 while a < 1:
    test = pyautogui.locateOnScreen(item, region=(x, y, w, h),
                                    grayscale=True, confidence=0.9) 
    if test is not None:
       a = a + 1     
       return test
    

#function to avoid disconnect
def step(item , x, y, w, h):
    if pyautogui.locateOnScreen(item, region=(x, y, w, h), grayscale=True,
                                confidence=0.9) !=None:
       pyautogui.press('w')
       

# Brazenhem algo
def draw_line(x1=0, y1=0, x2=0, y2=0):

    coordinates = []

    dx = x2 - x1
    dy = y2 - y1

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x1, y1

    error, t = el / 2, 0

    coordinates.append([x, y])

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        coordinates.append([x, y])

    return coordinates

# Smooth move mouse from current pos to xy
def smooth_move(x, y):
    flags, hcursor, (startX, startY) = win32gui.GetCursorInfo()
    coordinates = draw_line(startX, startY, x, y)
    x = 0
    for dot in coordinates:
        x += 1
        if x % 2 == 0 and x % 3 == 0:
            time.sleep(0.01)
        win32api.SetCursorPos((dot[0], dot[1]))   

#X: 2035 Y:  440 - position of the place to put an item
#function to put item in trade
def put_item_in_trade(x,y,item):
    pyautogui.press(str(x))
    pyautogui.press(str(y))
    active_item = check(item, 962, 165, 1403, 984)
    #we need to adjust x position
    win32api.SetCursorPos((active_item[0] + 50, active_item[1]))
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.2)
    smooth_move(1444, 322)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#function for charcoal + flux
def put_item_in_trade_flux_and_charcoal(x,y,z,item):
    pyautogui.press(str(x))
    pyautogui.press(str(y))
    pyautogui.press(str(z))
    active_item = check(item, 962, 165, 1403, 984)
    #we need to adjust x position
    win32api.SetCursorPos((active_item[0] + 50, active_item[1]))
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.2)
    smooth_move(1444, 322)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    
#1250, 280, 2000, 1400 - items
#2007, 722, 2500, 800 - buttons
#function to put all items                 
def put_all_items_asmo():
    print('start putting items')
    #put tolvium
    flux = check('C:\Python\Bot\Screens\TolviumFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')
    
    #put flux in trade
    #flux = check('fluxFullHD.png', 962, 165, 1403, 984)
    #time.sleep(.1)
    #click(flux[0], flux[1])
    #time.sleep(.1)
    #Split = check('SplitFullHD.png', 962, 165, 1403, 984)
    #time.sleep(.1)
    #click(Split[0], Split[1])
    #time.sleep(.1)
    #inTrade = check('inTradeFullHD.png', 962, 165, 1403, 984)
    #time.sleep(.1)
    #double_click(inTrade[0], inTrade[1])
    #time.sleep(.1)
    #put_item_in_trade_flux_and_charcoal(1, 5, 0,'ReadyForTradeFullHD.png')

    #put cinnabar
    flux = check('C:\Python\Bot\Screens\CinnabarFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,r'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')

    #put charcoal
    flux = check(r'C:\Python\Bot\Screens\CharcoalFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check(r'C:\Python\Bot\Screens\SplitFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check(r'C:\Python\Bot\Screens\inTradeFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade_flux_and_charcoal(3, 0, 0, r'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')

    #put ingot
    flux = check('C:\Python\Bot\Screens\IngotFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


#1250, 280, 2000, 1400 - items
#2007, 722, 2500, 800 - buttons
#function to put all items                 
def put_all_items_asmo_plus_runic():
    print('start putting items')
    #put tolvium
    flux = check('C:\Python\Bot\Screens\TolviumFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')
    

    #put cinnabar
    flux = check('C:\Python\Bot\Screens\CinnabarFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put ingot
    flux = check('C:\Python\Bot\Screens\IngotFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put scarhide
    flux = check('C:\Python\Bot\Screens\scarhide_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put smolderhide
    flux = check('C:\Python\Bot\Screens\smolderhide_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put infused leather
    flux = check('C:\Python\Bot\Screens\infused_leather_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')

        #put charcoal
    flux = check(r'C:\Python\Bot\Screens\CharcoalFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check(r'C:\Python\Bot\Screens\SplitFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check(r'C:\Python\Bot\Screens\inTradeFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade_flux_and_charcoal(3, 0, 0, r'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


def put_all_items_asmo_plus_runic_plus_phoenix():
    print('start putting items')
    #put tolvium
    flux = check('C:\Python\Bot\Screens\TolviumFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')
    

    #put cinnabar
    flux = check('C:\Python\Bot\Screens\CinnabarFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put ingot
    flux = check('C:\Python\Bot\Screens\IngotFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put scarhide
    flux = check('C:\Python\Bot\Screens\scarhide_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put smolderhide
    flux = check('C:\Python\Bot\Screens\smolderhide_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put infused leather
    flux = check('C:\Python\Bot\Screens\infused_leather_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put blisterweave
    flux = check('C:\Python\Bot\Screens\listerweave_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put scalecloth
    flux = check('C:\Python\Bot\Screens\scalecloth_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put unfused silk
    flux = check('C:\Python\Bot\Screens\infused_silk_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')

        #put charcoal
    flux = check(r'C:\Python\Bot\Screens\CharcoalFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check(r'C:\Python\Bot\Screens\SplitFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check(r'C:\Python\Bot\Screens\inTradeFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade_flux_and_charcoal(3, 0, 0, r'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')
    

def put_all_items_asmo_plus_phoenix():
    print('start putting items')
    #put tolvium
    flux = check('C:\Python\Bot\Screens\TolviumFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')
    

    #put cinnabar
    flux = check('C:\Python\Bot\Screens\CinnabarFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put ingot
    flux = check('C:\Python\Bot\Screens\IngotFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put blisterweave
    flux = check('C:\Python\Bot\Screens\listerweave_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put scalecloth
    flux = check('C:\Python\Bot\Screens\scalecloth_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(1,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')


    #put unfused silk
    flux = check('C:\Python\Bot\Screens\infused_silk_full_hd.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check('C:\Python\Bot\Screens\SplitFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check('C:\Python\Bot\Screens\inTradeFullHD.png', 962, 74, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade(5,0,'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')

        #put charcoal
    flux = check(r'C:\Python\Bot\Screens\CharcoalFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(flux[0], flux[1])
    time.sleep(.1)
    Split = check(r'C:\Python\Bot\Screens\SplitFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    click(Split[0], Split[1])
    time.sleep(.1)
    inTrade = check(r'C:\Python\Bot\Screens\inTradeFullHD.png', 962, 165, 1403, 984)
    time.sleep(.1)
    double_click(inTrade[0], inTrade[1])
    time.sleep(.1)
    put_item_in_trade_flux_and_charcoal(3, 0, 0, r'C:\Python\Bot\Screens\ReadyForTradeFullHD.png')
    
#function to check if name is true than press 'f1'
#and return list with last trade nickname included
#1080, 290, 1300, 330 - 2k resolution
def check_name(names1, names2, names3, names4):
    im = ImageGrab.grab(bbox=(812, 216, 980, 250))
    im_for_check = pytesseract.image_to_string(cv2.cvtColor(nm.array(im), cv2.COLOR_BGR2GRAY),lang ='eng')
    list_for_check = im_for_check.split()
    x = 0
    while x < 1:
        check = any(item in list_of_nicknames(names1) for item in list_for_check)
        check1 = any(item in list_of_nicknames(names2) for item in list_for_check)
        check2 = any(item in list_of_nicknames(names3) for item in list_for_check)
        check3 = any(item in list_of_nicknames(names4) for item in list_for_check)
        
        if check is True:
            x += 1
            time.sleep(.1)
            pyautogui.press('f1')
            common_name = set(list_of_nicknames(names1)).intersection(list_for_check)
            return common_name, 1
        elif check1 is True:
            x += 1
            time.sleep(.1)
            pyautogui.press('f1')
            common_name = set(list_of_nicknames(names2)).intersection(list_for_check)
            return common_name, 2
        elif check2 is True:
            x += 1
            time.sleep(.1)
            pyautogui.press('f1')
            common_name = set(list_of_nicknames(names3)).intersection(list_for_check)
            return common_name, 3
        elif check3 is True:
            x += 1
            time.sleep(.1)
            pyautogui.press('f1')
            common_name = set(list_of_nicknames(names4)).intersection(list_for_check)
            return common_name, 4
      
        else:
            im = ImageGrab.grab(bbox=(812, 216, 980, 250))
            im_for_check  = pytesseract.image_to_string(cv2.cvtColor(nm.array(im),
                                                                     cv2.COLOR_BGR2GRAY),lang ='eng')
            list_for_check = im_for_check.split()
            print('Right now I try to find name and I see: %r' % list_for_check)
            #print(list_for_check)
            



#function for accepting trade
#2184, 934, 2500, 1100 - for accept trade check of 'locked in' and 'confirmed'
def accept_trade():
    print("Now I should accept trade")
    check('C:\Python\Bot\Screens\LockedInFullHD.png', 1695, 694, 1850, 800)
    lockIn = check('C:\Python\Bot\Screens\LockinFullHD.png', 1498, 521, 1887, 617)
    click(lockIn[0], lockIn[1])
    check('C:\Python\Bot\Screens\ConfirmedFullHD.png', 1695, 694, 1850, 800)
    Trade = check('C:\Python\Bot\Screens\TradeFullHD.png', 1498, 521, 1887, 617)
    click(Trade[0], Trade[1])
    
    
#function to check 2 trades from 1 nickname
def second_trade_check(list1, list2):
    result = 0
    for x in list1:
        for y in list2:
            if x == y:
                result = result + 1
    return result

#update file with the history of today's trades
def file_update(name):
      name_str = str(name)
      name_str = name_str.replace("['", '')
      name_str = name_str.replace("']", '')
      # Open the file in append & read mode ('a+')
      with open("Transaction_history.txt", "r+") as f:
          data = list(f.readlines())
          try:
                count = data.index(name_str + '\n')
                if len(name_str) < 8:
                      data[count] = str(name_str + '\t\t' + name_str + '\n')
                else:
                      data[count] = str(name_str + '\t' + name_str + '\n')
                f.seek(0)
                for i in data:
                      f.write(i)
          except ValueError:
                f.readlines()
                f.write('\n' + name_str +\
                        '\t'+\
                        ' I traded with this nickname but'
                        ' for some reason I couldn\'t find'
                        ' it in the list' + '\n')
          f.close() 
                

           
#function of full rotation for asmo
def full_rotation(server, names_asmo, names_asmo_plus_runic, names_asmo_plus_runic_plus_phoenix, names_asmo_plus_phoenix):
    date(server, names_asmo, names_asmo_plus_runic, names_asmo_plus_runic_plus_phoenix, names_asmo_plus_phoenix)
    a = []
    z = []
    second_trade = []
    first_from_a = []
    first_from_a_in_one_element = []
    while 1:
        z, num = check_name(names_asmo, names_asmo_plus_runic, names_asmo_plus_runic_plus_phoenix, names_asmo_plus_phoenix)
        a = a + list(z)

        #asmo
        if num == 1 and second_trade_check(a, second_trade) == 1: 
           print('Second trade I should recieve all items')
           accept_trade()
           file_update(a)
           a = list(set(a) - set(z))
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)
        elif num == 1 and second_trade_check(list_of_nicknames(names_asmo), a) < 2:
           print(second_trade_check(list_of_nicknames(names_asmo), a))
           print('first trade I should give items for Asmodeum')
           put_all_items_asmo()
           accept_trade()
           second_trade.extend(a)
           a = []
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)

        #asmo + runic
        elif num == 2 and second_trade_check(a, second_trade) == 1: 
           print('Second trade I should recieve all items')
           accept_trade()
           file_update(a)
           a = list(set(a) - set(z))
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)
        elif num == 2 and second_trade_check(list_of_nicknames(names_asmo_plus_runic), a) < 2:
           print(second_trade_check(list_of_nicknames(names_asmo), a))
           print('first trade I should give items for Asmodeum and Runic Leather')
           put_all_items_asmo_plus_runic()
           accept_trade()
           second_trade.extend(a)
           a = []
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)

        #asmo + runic + silk
        elif num == 3 and second_trade_check(a, second_trade) == 1: 
           print('Second trade I should recieve all items')
           accept_trade()
           file_update(a)
           a = list(set(a) - set(z))
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)
        elif num == 3 and second_trade_check(list_of_nicknames(names_asmo_plus_runic_plus_phoenix), a) < 2:
           print(second_trade_check(list_of_nicknames(names_asmo), a))
           print('first trade I should give items for Asmodeum, Runic Leather and Phoenixweave')
           put_all_items_asmo_plus_runic_plus_phoenix()
           accept_trade()
           second_trade.extend(a)
           a = []
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)

        #asmo + silk
        elif num == 4 and second_trade_check(a, second_trade) == 1: 
           print('Second trade I should recieve all items')
           accept_trade()
           file_update(a)
           a = list(set(a) - set(z))
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)
        elif num == 4 and second_trade_check(list_of_nicknames(names_asmo_plus_phoenix), a) < 2:
           print(second_trade_check(list_of_nicknames(names_asmo), a))
           print('first trade I should give items for Asmodeum, Runic Leather and Phoenixweave')
           put_all_items_asmo_plus_phoenix()
           accept_trade()
           second_trade.extend(a)
           a = []
           step('C:\Python\Bot\Screens\stepFullHD.png', 1238, 23, 1765, 216)
           




