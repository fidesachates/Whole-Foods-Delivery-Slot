import bs4

from selenium import webdriver

import sys
import time
import os
import pyttsx3
import email_service

engine = pyttsx3.init()  # object creation


def sayIt(textToSay):
    engine.say(textToSay)
    engine.runAndWait()
    email_service.notify_slot_found(textToSay)


def getWFSlot(productUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    driver = webdriver.Chrome("C:\\Users\\eyy21\\Workspace\\Whole-Foods-Delivery-Slot\\chromedriver.exe")
    driver.get(productUrl)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    input("Hit enter to resume the script or just close it if you're done")
    should_continue = True

    while should_continue:
        driver.refresh()
        print("refreshed")
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        time.sleep(4)

        try:
            slot_opened_text = "Not available"
            all_dates = soup.findAll("div", {"class": "ufss-date-select-toggle-text-availability"})
            for each_date in all_dates:
                if slot_opened_text not in each_date.text:
                    print('SLOTS OPEN 2!')
                    sayIt('Slots for delivery opened!')
                    result = input("Hit enter to resume the script or type 'n' and hit enter to keep the loop going: ")
                    if result == "n":
                        should_continue = False
        except AttributeError:
            pass

        try:
            no_slot_pattern = 'No delivery windows available. New windows are released throughout the day.'
            if no_slot_pattern == soup.find('h4', class_='a-alert-heading').text:
                print("NO SLOTS!")
        except AttributeError:
            print('Banner is gone')
            sayIt('There might be slots open.')
            result = input("Hit enter to resume the script or type 'n' and hit enter to keep the loop going: ")
            if result == "n":
                should_continue = False

        slot_patterns = ['Next available', '1-hour delivery windows', '2-hour delivery windows']
        try:
            next_slot_text = str(
                [x.text for x in soup.findAll('h4', class_='ufss-slotgroup-heading-text a-text-normal')])
            if any(next_slot_text in slot_pattern for slot_pattern in slot_patterns):
                print('SLOTS OPEN!')
                sayIt('Slots for delivery opened!')
                result = input("Hit enter to resume the script or type 'n' and hit enter to keep the loop going: ")
                if result == "n":
                    should_continue = False

        except AttributeError:
            pass


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')
