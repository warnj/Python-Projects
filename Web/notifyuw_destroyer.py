import imaplib2, time, email, email.header, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from threading import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# to make executable execute command: pyinstaller.exe --onefile NotifyUW_Destroyer.py
# TODO: Make a GUI interface and a nice stop button that logs out of email and such
# sometimes will add an sln randomly(?) if the last email in gmail account is from notify uw - dont know what triggers the event in the email thread
# add a way to delete the last 2 emails after registering

# run this from a cmd terminal with:
#   python ./Documents/programming/python/notifyUW_destroyer.py
#   to close gracefully with ctrl+c

class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()

    def start(self):
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        while True:
            if self.event.isSet():
                return
            self.needsync = False

            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()

            self.M.idle(callback=callback)
            self.event.wait()
            if self.needsync:
                self.event.clear()
                self.dosync()

    # gets the latest email, extracts sln # and types into UW registration
    def dosync(self):
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
                elem = driver.find_element_by_name("sln6")  # sln6 corresponds to the sln box highest on the page
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
                    elem = driver.find_element_by_xpath("//img[contains(@src,'/sdb_library/images/warning.gif')]")
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


try:
    data = json.loads(open('../personal_data.json').read())
    # M = imaplib2.IMAP4_SSL('imap-mail.outlook.com')# times out after about 3 minutes on hotmail account, gmail does not
    M = imaplib2.IMAP4_SSL('imap.gmail.com')
    M.login(data["gmail"], data["gmail_password"])
    M.select("INBOX")
    # adds am email to the mailbox
    msg = MIMEMultipart()
    msg["From"] = data["email"]
    msg["Subject"] = "Appended Email"
    msg.set_payload("First Appended Email")
    M.append('INBOX', '', imaplib2.Time2Internaldate(time.time()), str(msg))
    print("Waiting for Emails....")
    print("Press ctrl + c to stop")
    idler = Idler(M)  # Start the Idler thread
    idler.start()
    slns = []
    while True:
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
        try:
            for i in range(0, 14):
                time.sleep(1800)  # sleep for 14 1/2hr increments so session is always logged in

                # adds am email to the mailbox
                msg = MIMEMultipart()
                msg["From"] = data["email"]
                msg["Subject"] = "Appended Email"
                msg.set_payload("Content of email")
                M.append('INBOX', '', imaplib2.Time2Internaldate(time.time()), str(msg))

                # deletes most recent email from mailbox
                result, data = M.search(None, "ALL")
                ids = data[0]
                id_list = ids.split()
                latest_email_id = id_list[-1]
                M.store(latest_email_id, '+FLAGS', '\\Deleted')
                M.expunge()

            driver.close()
        except KeyboardInterrupt:
            print('\nExiting Browser.')
            driver.close()
            exit(0)

finally:
    print("Cleaning up Idler and Email")
    idler.stop()
    idler.join()
    M.close()
    M.logout()  # This is important!
