import asyncio
import os
import re
from concurrent.futures import ThreadPoolExecutor

from gmail import GMail, Message

from secret import BASEPATH, GMAIL_ACCOUNT, GMAIL_PASSWD, MAIL_TO



mail_to = MAIL_TO


def checkfolder():
    folders = []
    for folder, sub, filenames in os.walk(BASEPATH):
        if u'ready_to_send.gml' in filenames:
            folders.append(folder)
    return folders


def get_content(path, filenames, suffix):
    target_file = [f for f in filenames if re.search(suffix, f)][0]
    with open(os.path.join(path, target_file)) as f:
        file_content = f.read()
    return file_content


async def sendmail(title, text, attachments):
    print('Sending {}'.format(title))
    gmail = GMail(GMAIL_ACCOUNT, GMAIL_PASSWD)
    msg = Message(title,
                    to=mail_to,
                    text=text,
                    attachments=attachments
    )
    await gmail.send(msg)
    gmail.close()
    print('Send.')


class Email():
    def __init__(self, path, title, text, attachments):
        self.path = path
        self.title = title
        self.text = text
        self.attachments = attachments

    def send(self):
        print('Sending {}'.format(self.title))
        gmail = GMail(GMAIL_ACCOUNT, GMAIL_PASSWD)
        msg = Message(self.title,
                      to=mail_to,
                      text=self.text,
                      attachments=self.attachments
                      )
        gmail.send(msg)
        gmail.close()
        print('Ok. Sent {}'.format(self.title))

    async def asend(self):
        print('Sending {}'.format(self.title))
        await self.send()
        print('Ok. Sent {}'.format(self.title))

    def done(self):
        os.rename(
            os.path.join(self.path, 'ready_to_send.gml'),
            os.path.join(self.path, 'sent.gml')
        )


def load_emails():
    emails = []
    folders = checkfolder()
    for folder in folders:
        for path, sub, filenames in os.walk(folder):
            try:
                title = get_content(path, filenames, 'gml$')
            except IndexError as e:
                print('.gml file not found. Error: %s' % e)

            try:
                text = get_content(path, filenames, 'txt$')
            except IndexError as e:
                print('.txt file not found. Error: %s' % e)

            attachments = []
            for filename in filenames:
                attachment = os.path.join(path, filename)
                attachments.append(attachment)

            email = Email(path, title, text, attachments)
            emails.append(email)

    return emails


async def main():
    emails = load_emails()
    coroutines = [email.asend() for email in emails]
    tasks = [asyncio.ensure_future(coro) for coro in coroutines]
    await asyncio.wait(tasks)

async def run_tasks(executor):
    loop = asyncio.get_event_loop()

    emails = load_emails()
    blocking_tasks = [loop.run_in_executor(executor, email.send)for email in emails]
    await asyncio.wait(blocking_tasks)


if __name__ == '__main__':
    executor = ThreadPoolExecutor(3)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks(executor))
    print('DONE!')
