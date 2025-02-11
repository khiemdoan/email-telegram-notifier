__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

from email.header import decode_header

from imapclient import IMAPClient
from imapclient.response_types import Address, Envelope
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

from telegram import Telegram
from templates import Render


class ImapSettings(BaseSettings):
    host: str
    port: str
    email: str
    password: str

    model_config = SettingsConfigDict(
        extra='ignore',
        env_prefix='IMAP_',
        env_file='.env',
        env_file_encoding='utf-8',
    )


def decode_subject(subject: bytes) -> str:
    subject = decode_header(subject.decode('utf-8'))
    subject = ', '.join(s[0].decode(s[1]) if isinstance(s[0], bytes) else s[0] for s in subject)
    return subject


def decode_address(addr: Address) -> str:
    mailbox = addr.mailbox.decode('utf-8')
    host = addr.host.decode('utf-8')

    if addr.name is None:
        return f'{mailbox}@{host}'

    name = decode_header(addr.name.decode('utf-8'))
    name = ', '.join(n[0].decode(n[1]) if isinstance(n[0], bytes) else n[0] for n in name)

    return f'{name} ({mailbox}@{host})'


def check_folder(client: IMAPClient, folder: str):
    emails = []

    client.select_folder(folder)
    message_ids = client.search('UNSEEN')
    messages = client.fetch(message_ids, ['ENVELOPE'])
    for _, data in messages.items():
        envelope: Envelope = data[b'ENVELOPE']
        email = {
            'subject': decode_subject(envelope.subject),
            'date': envelope.date,
            'folder': folder,
            'from': ', '.join(decode_address(addr) for addr in envelope.from_),
            'to': ', '.join(decode_address(addr) for addr in envelope.to),
        }
        if envelope.cc:
            email['cc'] = ', '.join(decode_address(addr) for addr in envelope.cc)
        if envelope.bcc:
            email['bcc'] = ', '.join(decode_address(addr) for addr in envelope.bcc)
        emails.append(email)

    if not emails:
        return

    context = {
        'folder': folder,
        'total': len(emails),
        'emails': emails,
    }
    render = Render()
    message = render('message.j2', context).strip()

    with Telegram() as tele:
        try:
            tele.send_message(message)
        except Exception as ex:
            logger.error(ex)


if __name__ == '__main__':
    imap = ImapSettings()
    with IMAPClient(host=imap.host, port=imap.port) as client:
        client.login(imap.email, imap.password)

        folders = client.list_folders()
        for folder in folders:
            check_folder(client, folder[-1])
