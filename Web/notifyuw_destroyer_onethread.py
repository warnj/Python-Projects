import imaplib2, time, email, email.header, datetime, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# to make executable execute command: pyinstaller.exe --onefile NotifyUW_Destroyer.py
# TODO: Make a GUI interface and a nice stop button that logs out of email and such
# sometimes will add an sln randomly(?) if the last email in gmail account is from notify uw - dont know what triggers the event in the email thread
# add a way to delete the last 2 emails after registering

# run this from a cmd terminal with:
#   python ./Documents/programming/python/notifyUW_destroyer.py
#   to close gracefully with ctrl+c

try:
    data = json.loads(open('../personal_data.json').read())
    # M = imaplib2.IMAP4_SSL('imap-mail.outlook.com')# times out after about 3 minutes on hotmail account, gmail does not
    M = imaplib2.IMAP4_SSL('imap.gmail.com')
    M.login(data["gmail"], data["gmail_password"])
    M.select("INBOX")
    print("Checking for Emails....")
    print("Press ctrl + c to stop")
    slns = []

    while True:
        start = datetime.datetime.now()
        driver = webdriver.Firefox()  # open browser to wait for email
        driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")
        assert "NetID" in driver.title
        elem = driver.find_element_by_name("user")
        elem.send_keys(data["uw_username"])
        elem = driver.find_element_by_name("pass")
        elem.send_keys(data["uw_password"])
        elem.send_keys(Keys.RETURN)
        assert "Registration" in driver.title
        driver.maximize_window()  # user can minimize the window
        restart = False
        while restart == False:
            try:
                # repeatedly check first email

                html = ''
                result, data = M.search(None, "ALL")
                ids = data[0]
                id_list = ids.split()
                latest_email_id = id_list[-1]
                result, data = M.fetch(latest_email_id, "(RFC822)")
                msg = email.message_from_string(data[0][1])
                if msg.is_multipart():  # this multipart stuff may be unneeded
                    for payload in msg.get_payload():
                        html += payload.get_payload(decode=True)
                else:
                    html = msg.get_payload(decode=True)
                index = html.find("(SLN: ")
                if index != -1:  # got a notifyUW email
                    sln = html[index + 6: index + 11]
                    # straight up register here if no quiz/labs to worry about - comment out these if/elses

                    if len(
                            slns) > 0:  # we have already received a notify email recently - change 0 to a 1 if have 3 sections to register for simultaneously
                        elem = driver.find_element_by_name(
                            "sln6")  # sln6 corresponds to the sln box highest on the page
                        elem.send_keys(sln)
                        i = 7
                        for num in slns:  # loop here kind of overkill for just one quiz section to register for
                            elem = driver.find_element_by_name("sln" + str(i))
                            elem.send_keys(num)
                            i += 1

                        # to drop a course:
                        # elem = driver.find_element_by_name("action4") #action1 corresponds to the class highest on the page
                        # elem.click()

                        elem.send_keys(Keys.RETURN)

                        slns.append(sln)
                        print("registering for slns: ", slns)
                        print("registering at time %s" % time.ctime())

                        try:  # look for the failure image on the page
                            elem = driver.find_element_by_xpath(
                                "//img[contains(@src,'/sdb_library/images/warning.gif')]")
                            print("registration failed")
                            # return to blank registration page
                            driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")

                        except:
                            print("registration succeeded")

                        finally:
                            del slns[:]  # empty the list after registering

                    else:  # this is the first notify email, store sln and wait for second email
                        slns.append(sln)
                        print("slns: ", slns)
                        print("appended sln at time %s" % time.ctime())

                else:
                    print("checked email, but did not have an sln number at time %s" % time.ctime())

                time.sleep(1)  # check email every second
                now = datetime.datetime.now()
                if (now - start).total_seconds() > (3600 * 7):  # relogin to myUW every 7 hrs
                    driver.close()
            except KeyboardInterrupt:
                print('\nExiting Browser.')
                driver.close()
                exit(0)

finally:
    print("Cleaning up Idler and Email")
    M.close()
    M.logout()  # This is important!
