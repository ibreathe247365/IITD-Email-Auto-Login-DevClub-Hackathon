# IITD-Email-Auto-Login-DevClub-Hackathon
This repo is made by Shreyansh Jain and is a submission for Hackathon CampusHack 2021
(If you just want to know what to do to run it, just read form line 10)

This project was in my mind for quiet a few time but I was not having enough motivation to start working upon it. But CampusHack came out to be a great game changer.
When DevClub IITD gave a assignment to make moodle auto login bot, I was pretty excited to make one for IITD email as well. Hearing of CampusHack I worked really long this weekend and made a bot that can read what is given in image captcha(almost accurate).

In my email bot I used image processing using opencv and neural networks using tensorflow to make a bot to extract the right characters from given captcha. The model is pretty accurate but it may take a few tries before decoding the correct captcha sequence.

First of all, installing all python pre-requisite for this(hoping you have python installed)
Step 1: You just have to double-click the installer.bat file and it will do all installation work for you(please make sure you have active internet connection and pip correctly installed)
Step 2: Nothing you are done, to run moodle bot, just double click moodle_login.bat file and for IITD_Email bot run Mail_bot.bat file and watch the magic happen

(Here you need to enter your details in the terminal but can change it in code by commenting and uncommenting lines in code so that you don't have to enter them again and again, for it just comment lines 1, 2, 42 and 45 in IIT-Email_BOT.py and uncomment lines 41 and 44 and write your credentials as shown there and just opposite for reverse.)
