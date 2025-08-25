
# BlackLAN Messenger

> Message from Dev

- This Project made by a 19-year-old developer who loves to code for no reaone hope anyone help me upgrade this project with new features and ideas.
- Join my discord server for support and updates: [![NullStudio](https://img.shields.io/badge/nullstudio-join-blue.svg?logo=discord)](https://discord.gg/aFvUxKejw4) i'll apreciate your support and feedback!

## Table of Contents

- [About](#about)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technical Details](#technical-details)
- [Installation & Usage](#installation--usage)
- [Testing](#testing)
- [Notes](#notes)
- [Join the Community](#join-the-community)
- [💖 Support the Project](#💖-support-the-project)

## About

BlackLAN is a terminal-only LAN messenger for developers who still write their own sockets. It supports multi-user real-time chat, command handling, colored terminal logs, and that raw `[ OK ]` console vibe. Built for local networks. Built for control. This project was made by a 19-year-old developer.

This is a full-featured LAN messaging system using Python in the command line, inspired by penetration testing tools and hacker-style UIs.

## Project Structure

```

lan\_messenger/
│
├── client.py
├── server.py
├── config/
│   └── settings.json
│   └── settings.py
├── core/
│   ├── connection.py
│   ├── command\_handler.py
│   ├── message\_router.py
│   └── user\_session.py
│
├── utils/
│   ├── logger.py
│   ├── colors.py
│   ├── encryption.py
│   └── animation.py
│
├── chat\_logs/
│   └── server\_log.txt
│
├── README.md
└── requirements.txt

````

## Features

### Core Chat System

- Server handles multiple clients at once
- Usernames are entered at connection
- Broadcast messages in real-time with timestamp and username
- Message separation and formatting

### Admin & User Management

- Admin commands: `/kick`, `/ban`, `/mute`
- Server alerts on join/leave
- Temporary mute with timers

### User Commands

- `/users` — List all active users  
- `/msg <user>` — Send private message  
- `/nick <name>` — Change your username  
- `/ping <user>` — Simulate ping latency  
- `/status` — Set your current status (online/away/dnd)  
- `/clear` — Clear the terminal  
- `/exit` — Exit the client

### Terminal Experience

- `[ OK ]`, `[INFO]`, `[ERROR]` style messages using `colorama`
- Connecting animation / spinner
- Custom logger with timestamps

### Optional Features

- Basic **end-to-end encryption** using XOR with shared key (demo only)
- All settings are in `config/settings.json`

## Technical Details

- Built with Python 3.11+
- Multi-threaded server using `threading`
- Central command handler
- Error-resilient socket logic
- Easily configurable: host, port, buffer size, encryption key

## Installation & Usage

### Requirements

- Python 3.11+
- Install required packages:

```bash
  pip install -r requirements.txt
```

### Setup

1. **Clone or extract the project**

   ```bash
   unzip lan_messenger.zip
   cd lan_messenger
   ```

2. **Edit Configuration (Optional)**

   ```bash
   nano config/settings.json
   ```

3. **Run the Server**

   ```bash
   python3.11 server.py
   ```

4. **Run Clients**

   ```bash
   python3.11 client.py
   ```

Open multiple terminals to simulate multi-user chat.

## Testing

- Simulate many clients in different terminals
- Try all commands (`/msg`, `/nick`, `/ping`, `/status`, etc.)
- Use username `admin` to test admin-only commands (`/kick`, etc.)

## Notes

- The encryption method (XOR) is for **demo purposes only** — not secure.
- Admin authentication is **username-based only**. No password or real auth yet.
- This tool is meant for **local network testing** and learning socket programming.

## Join the Community

**Want to learn more, suggest features, or get support?**

[![Join Discord](https://img.shields.io/badge/Join%20Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/aFvUxKejw4)
[![Follow on GitHub](https://img.shields.io/badge/Follow%20on-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/NullStudio-dev)

## 💖 Support the Project

If you find this project useful and want to support its development, you can help through the following platforms:

>[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg?logo=paypal)](https://paypal.me/ayoubzel)  
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-333.svg?logo=github)](https://github.com/sponsors/RDXFGXY1)  
[![Patreon](https://img.shields.io/badge/Patreon-Support-orange.svg?logo=patreon)](https://patreon.com/NullStudio001)  
[![Open Collective](https://img.shields.io/badge/Open%20Collective-Contribute-9cf.svg?logo=open-collective)](https://opencollective.com/rdxfgxy1)  
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Donate-ff5f5f?logo=ko-fi)](https://ko-fi.com/kyrosdev)  
[![Liberapay](https://img.shields.io/badge/Liberapay-Donate-yellow.svg?logo=liberapay)](https://liberapay.com/kyros)  

- -_-

> Made With ❤️ by NullStudio