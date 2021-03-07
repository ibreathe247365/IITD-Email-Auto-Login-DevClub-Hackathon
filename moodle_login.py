
def moodle_login(driver):
    user = "mt1200852"
    passward = "836ef764"
    driver.get("https://moodle.iitd.ac.in/login/index.php")
    username = driver.find_element_by_id("username")
    username.send_keys(user)
    password = driver.find_element_by_id("password")
    password.send_keys(passward)
    captcha = driver.find_element_by_id("login")
    lst = captcha.get_attribute("innerText").split("\n")
    var = lst[3]
    print(var)
    val = 0
    if "add" in var:
        var = var.split(" ")
        val = int(var[2]) + int(var[4])
    elif "subtract" in var:
        var = var.split(" ")
        val = int(var[2]) - int(var[4])
    elif "first" in var:
        var = var.split(" ")
        val = int(var[4])
    elif "second" in var:
        var = var.split(" ")
        val = int(var[6])
    print(val)
    value = driver.find_element_by_id("valuepkg3")
    value.send_keys(str(val))
    driver.find_element_by_id("loginbtn").click()


if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome("chromedriver.exe")
    moodle_login(driver)
