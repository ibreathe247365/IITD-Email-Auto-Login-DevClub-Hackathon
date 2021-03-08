user_id = input("Enter your user id\n")
user_pass = input("Enter your user passward\n")
from selenium import webdriver
import cv2
import numpy as np
from urllib.request import urlopen
import tensorflow as tf
import pyttsx3
from datetime import datetime

# selenium functions a bit
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://webmail.iitd.ac.in/roundcube/?_task=mail&_mbox=INBOX")
window_before = driver.window_handles[0]
title = driver.title
print(title)


# Making voice function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Predict Function
def predict_char(var):
    model = tf.keras.models.load_model("letter_recognition")
    pred = model.predict([var])
    predictions = []
    for i in range(len(pred)):
        print(f"{i + 1} prediction is: {np.argmax(pred[i])}")
        predictions.append(np.argmax(pred[i]))

    return predictions


# making it in function
def login():
    user = driver.find_element_by_id("rcmloginuser")
    # user.send_keys(    " your user id here"   )          # uncomment it and write your user id in "" if don;t want to type again and again
    user.send_keys(user_id)                                # comment it if you want to make it automated
    password = driver.find_element_by_id("rcmloginpwd")
    # password.send_keys(  "your user password here"  )      # uncomment it and write your user passward in "" if don;t want to type again and again
    password.send_keys(user_pass)                          # comment it if you want to make it automated
    captcha_image = driver.find_element_by_id("captcha_image")
    captcha_image_src = captcha_image.get_attribute("src")

    # getting image of captcha
    url = urlopen(captcha_image_src)
    img_arr = np.array(bytearray(url.read()), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)

    # defining variables for contours
    cnts = []
    cnts_new = []
    cnt_vals = []
    output = []

    # labels
    labels = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # getting useful characters form captcha
    frame = img
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 0, 0), (255, 255, 130))
    mask = cv2.bitwise_and(frame, frame, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # highlighting contours and getting contour data
    i = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 10:
            x, y, w, h = cv2.boundingRect(cnt)
            cnt_vals.append([x, y, w, h])
            cnts.append(np.zeros((60, 200)))
            cnts_new.append(np.zeros((42, 42)))
            cnts[i] = cv2.drawContours(cnts[i], contours, i, (255, 255, 255), 1)
            i += 1
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    # sorting contours
    passed = 0
    while passed != (len(cnts) - 1):
        passed = 0
        for i in range(len(cnts) - 1):
            x = cnt_vals[i][0]
            y = cnt_vals[i+1][0]
            if x > y:
                xc = cnt_vals[i]
                cnt_vals[i] = cnt_vals[i+1]
                cnt_vals[i+1] = xc
            else:
                passed += 1

    # getting each contour specifically
    for i in range(len(cnts)):
        x = cnt_vals[i][0]
        y = cnt_vals[i][1]
        w = cnt_vals[i][2]
        h = cnt_vals[i][3]
        cnt = mask[y:y+h, x:x+w]
        cnt = cv2.resize(cnt, (28, 28))
        cnts_new[i][7:35, 7:35] = cnt
        cnts_new[i] = cv2.resize(cnts_new[i], (28, 28))
        cnts_new[i] = cnts_new[i].tolist()
        output.append(cnts_new[i])

    output = np.array(output)
    output = tf.keras.utils.normalize(output, axis=1)

    ## Displaying all contours
    # cv2.imshow("mask", mask)
    # j = 0
    # for i in output:
    #     cv2.imshow(f"{j}", i)
    #     j += 1
    #
    # cv2.waitKey(100)
    # cv2.destroyAllWindows()
    # uncomment and increase time in milliseconds to see the images

    predictions = predict_char(output)

    # filling captcha
    captcha_input = driver.find_element_by_name("captcha_input")
    captcha_input_value = ""
    for i in range(len(predictions)):
        captcha_input_value += labels[predictions[i]]
    captcha_input.send_keys(captcha_input_value)
    print(captcha_input_value)
    driver.find_element_by_id("rcmloginsubmit").click()
    driver.implicitly_wait(3)
    if driver.title == title:
        login()
    else:
        unread = True
        i = 1
        while unread:
            mail = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr[" + f"{i}" + "]/td[2]/span[3]/span")
            unread = mail.get_attribute("title")
            if unread:
                title_mail = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr[" + f"{i}" + "]/td[2]/span[3]/a/span")
                text = title_mail.get_attribute("innerHTML")
                print(text)
                f = open("IITD_Email Notification.txt", "w", encoding="utf-8")
                to_write = f"{i}  unread mail says: " + text + "\non: " + str(datetime.now()) + "\n"
                to_speak = f"{i}       unread mail says: " + text + "\n"
                try:
                    speak(to_speak)
                except:
                    pass
                f.write(to_write)
                f.close()
            i += 1


login()

