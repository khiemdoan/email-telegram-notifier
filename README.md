# email-telegram-notifier

Small utility helps you quickly know when have a new email.

## Usage

Set environment variables or write to `.env` file (keep them secret only for you)

```text
IMAP_HOST =
IMAP_PORT =
IMAP_EMAIL =
IMAP_PASSWORD =

TELEGRAM_BOT_TOKEN =
TELEGRAM_CHAT_ID =
```

And run the script:

```sh
python src/main.py
```
