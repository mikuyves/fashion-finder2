import asyncio
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from gmail import GMail, Message

from secret import BASEPATH, GMAIL_ACCOUNT, GMAIL_PASSWD, MAIL_TO


def check_path():
    '''Return: paths::List of <Path>'''
    paths = [p for p in BASEPATH.iterdir() if (p / 'ready_to_send.gml').exists()]
    return paths


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
                      to=MAIL_TO,
                      text=self.text,
                      attachments=self.attachments
                      )
        gmail.send(msg)
        gmail.close()
        print('Ok. Sent {}'.format(self.title))

    def done(self):
        (self.path / 'ready_to_send.gml').rename(self.path / 'sent.gml')


def load_emails():
    '''Load all the file that ready to send.'''
    emails = []
    paths = check_path()
    for path in paths:
        try:
            title = list(path.glob('*.gml'))[0].read_text()
        except IndexError as e:
            print('.gml file not found. Error: %s' % e)
            title = 'No title'

        try:
            text = list(path.glob('*.txt'))[0].read_text()
        except IndexError as e:
            print('.txt file not found. Error: %s' % e)
            text = 'No content.'

        attachments = [str(f) for f in path.iterdir() if f.is_file()]

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
    blocking_tasks = [loop.run_in_executor(executor, email.send) for email in emails]
    await asyncio.wait(blocking_tasks)
    [email.done() for email in emails]

if __name__ == '__main__':
    executor = ThreadPoolExecutor(3)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks(executor))
    print('DONE!')
