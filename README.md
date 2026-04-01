# Greeter Telegram Bot

A Telegram group management bot that welcomes new members and bids farewell when they leave.

## Features
- Auto welcome message when someone joins
- Farewell message when someone leaves
- Member count in welcome message
- `/setwelcome <message>` — Set custom welcome message (admins only)
- `/clearwelcome` — Reset to default message (admins only)
- `/help` — Show commands and placeholders

## Placeholders
Use these in your custom welcome message:
- `{name}` — Member's first name
- `{group}` — Group name  
- `{count}` — Current member count

**Example:**
```
/setwelcome Welcome {name} to {group}! You're member #{count} 🎉
```

## Setup

1. Clone the repo
```bash
git clone https://github.com/aditya4w/Greeter-Telegram-Bot
```

2. Install dependencies
```bash
pip install python-telegram-bot
```

3. Configure
```bash
cp config.example.py config.py
```

4. Add your credentials in `config.py`
```python
TOKEN = 'your-bot-token'
BOT_USERNAME = '@your-bot-username'
```

5. Add bot to your group and make it **admin**

6. Run
```bash
python main.py
```

## Built With
- Python
- python-telegram-bot v22
- SQLite
