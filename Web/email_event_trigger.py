import imaplib2, time, email, email.header
from threading import *


# This is the threading object that does all the waiting on
class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()

    def start(self):
        self.thread.start()

    def stop(self):
        # This is a neat trick to make thread end.
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        while True:
            # This is part of the trick to make the loop stop 
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False

            # A callback method that gets called when a new
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()

            # Do the actual idle call. This returns immediately,
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is 
            # set by the callback, when the server 'answers' 
            # the idle call and the callback function gets 
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing 
            # anything if the stop() is called. Kinda neat 
            # solution.
            if self.needsync:
                self.event.clear()
                self.dosync()

    # The method that gets called when a new email arrives. 
    # gets the latest email and extract sln #
    def dosync(self):
        html = ''
        result, data = M.search(None, "ALL")
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = M.fetch(latest_email_id, "(RFC822)")
        msg = email.message_from_string(data[0][1])
        if msg.is_multipart():
            for payload in msg.get_payload():
                html += payload.get_payload(decode=True)
        else:
            html = msg.get_payload(decode=True)
        index = html.find("(SLN: ")
        if index != -1:
            sln = html[index + 6: index + 11]
            print(sln)


try:
    data = json.loads(open('../personal_data.json').read())
    # This program times out after about 3 minutes on hotmail account, gmail does not
    # M = imaplib2.IMAP4_SSL('imap-mail.outlook.com')
    M = imaplib2.IMAP4_SSL('imap.gmail.com')
    M.login(data["gmail"], data["gmail_password"])
    M.select("INBOX")
    print("Waiting for Emails....")
    idler = Idler(M)  # Start the Idler thread
    idler.start()
    while True:
        time.sleep(5 * 60)  # sleep forever in 5 min increments
finally:
    # Clean up.
    idler.stop()
    idler.join()
    M.close()
    M.logout()  # This is important!
