
# IoT Security Monitoring System

A network monitoring and security alert system designed to run on a Raspberry Pi. The system monitors network activity, detects selected abnormal network conditions, sends monitoring data to ThingSpeak, and can send security notifications through CallMeBot.

## Project Structure

Place all project files in the same directory:

```text
IoT-Security-Monitoring/
├── main.py
├── config.py
├── requirements.txt
├── monitor.py
├── security.py
├── thingspeak.py
└── README.md
```

### File Description

- `main.py` — Main program that continuously runs the monitoring system.
- `monitor.py` — Collects network statistics using `psutil`.
- `security.py` — Checks network statistics and detects security alerts.
- `thingspeak.py` — Sends monitoring data to ThingSpeak and security messages through CallMeBot.
- `config.py` — Contains ThingSpeak settings and the update interval.

## Requirements

### Hardware

- Raspberry Pi Zero or a compatible Raspberry Pi.
- Internet connection.
- A network to monitor.

### Software

- Raspberry Pi OS / Linux.
- Python 3.
- pip.

## 1. Update the System

Open a Terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

Check the Python version:

```bash
python3 --version
```

Check pip:

```bash
python3 -m pip --version
```

If pip is not installed:

```bash
sudo apt install python3-pip -y
```

## 2. Install the Required Libraries

The project uses:

- `psutil` — for collecting network statistics.
- `requests` — for sending data to external services.

Install them with:

```bash
python3 -m pip install -r requirements.txt 
```

If your operating system does not allow direct installation, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure ThingSpeak

Create a Channel in ThingSpeak and add 8 fields.

The project uses the fields as follows:

| Field | Data |
|---|---|
| Field 1 | Download |
| Field 2 | Upload |
| Field 3 | Connections |
| Field 4 | TCP |
| Field 5 | UDP |
| Field 6 | Network Interfaces |
| Field 7 | Security Alert |
| Field 8 | Packets/s |

After creating the Channel, obtain the **Write API Key**.

Open:

```text
config.py
```

Set the API key:

```python
THINGSPEAK_WRITE_API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"
```

The ThingSpeak API endpoint used by the project is:

```python
THINGSPEAK_URL = "https://api.thingspeak.com/update"
```

## 4. Configure the Update Interval

In `config.py`:

```python
UPDATE_INTERVAL = 20
```

This means the system waits **20 seconds** between updates.

For example, to update every 60 seconds:

```python
UPDATE_INTERVAL = 60
```

## 5. Configure CallMeBot Notifications

The `thingspeak.py` file contains a function for sending messages through CallMeBot.

The current project contains the following user value:

```python
"user": "just_nobody8"
```

If you use a different CallMeBot configuration, change the required values in `send_tel_message()` according to your account and service configuration.

> **Security:** Never publish API keys, tokens, passwords, or other private credentials in a public GitHub repository.

## 6. Run the Project

Open the project directory:

```bash
cd IoT-Security-Monitoring
```

Run the program:

```bash
python3 main.py
```

When the program starts, it displays:

```text
==================================================
IoT Security Monitoring System
Raspberry Pi Zero + ThingSpeak
==================================================
```

The system then starts collecting network statistics continuously.

## 7. Network Data Monitored

The `monitor.py` module collects:

- Download traffic.
- Upload traffic.
- Number of active network connections.
- Number of TCP connections.
- Number of UDP connections.
- Number of active network interfaces.
- Packets per second.

Download and upload traffic are calculated during a short measurement interval, and the results are then returned to the main program.

## 8. Security Alert Detection

The `security.py` module compares network statistics against predefined thresholds.

For example:

```python
if stats["connections"] > 10:
```

If the number of connections exceeds 10, a security alert is activated.

The program also checks TCP connections:

```python
if stats["tcp"] > 80:
```

Download traffic:

```python
if stats["download"] > 5000:
```

Upload traffic:

```python
if stats["upload"] > 2000:
```

When one of these thresholds is exceeded, a Security Alert is generated and the reason is added to the alert message.

## 9. Send Data to ThingSpeak

The project sends the monitoring data using an HTTP POST request.

The following values are sent:

```text
field1 = Download
field2 = Upload
field3 = Connections
field4 = TCP
field5 = UDP
field6 = Interfaces
field7 = Security Alert
field8 = Packets/s
```

The data can then be viewed through the ThingSpeak Channel dashboard and its graphs.

## 10. Stop the Program

To stop the program while it is running:

```text
Ctrl + C
```

The program will display:

```text
Program stopped.
```

## 11. Run the Program in the Background

You can run the program in the background using:

```bash
nohup python3 main.py > monitor.log 2>&1 &
```

View the log:

```bash
tail -f monitor.log
```

Find the running process:

```bash
ps aux | grep main.py
```

Then stop it using:

```bash
kill PID
```

Replace `PID` with the process ID.

## 12. Start Automatically After Raspberry Pi Boots

You can use `systemd` to start the monitoring system automatically.

Create the service file:

```bash
sudo nano /etc/systemd/system/iot-monitor.service
```

Add:

```ini
[Unit]
Description=IoT Security Monitoring System
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/IoT-Security-Monitoring
ExecStart=/usr/bin/python3 /home/pi/IoT-Security-Monitoring/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

If your username or project directory is different, change:

```ini
User=pi
WorkingDirectory=/home/pi/IoT-Security-Monitoring
ExecStart=/usr/bin/python3 /home/pi/IoT-Security-Monitoring/main.py
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service:

```bash
sudo systemctl enable iot-monitor.service
```

Start the service:

```bash
sudo systemctl start iot-monitor.service
```

Check the service status:

```bash
sudo systemctl status iot-monitor.service
```

View the program logs:

```bash
journalctl -u iot-monitor.service -f
```

## 13. Troubleshooting

### `ModuleNotFoundError`

For example:

```text
ModuleNotFoundError: No module named 'psutil'
```

Install the missing library:

```bash
python3 -m pip install psutil
```

For `requests`:

```bash
python3 -m pip install requests
```

### ThingSpeak Is Not Receiving Data

Check:

1. The Raspberry Pi has an Internet connection.
2. The `THINGSPEAK_WRITE_API_KEY` is correct.
3. The ThingSpeak Channel and fields are configured correctly.
4. There is no network connection problem preventing access to ThingSpeak.

### Security Notifications Are Not Received

Check the CallMeBot configuration in:

```text
thingspeak.py
```

Make sure the CallMeBot service and account configuration are correct.

## 14. Program Workflow

After running:

```bash
python3 main.py
```

the system repeatedly performs the following process:

```text
Collect Network Statistics
          ↓
Analyze Network Activity
          ↓
Detect Security Alert
          ↓
Send Data to ThingSpeak
          ↓
Send Notification When Required
          ↓
Wait According to UPDATE_INTERVAL
          ↓
Repeat
```

## 15. Security Recommendations

Do not upload `config.py` to GitHub if it contains real API keys.

It is recommended to add the following to `.gitignore`:

```gitignore
config.py
__pycache__/
*.pyc
venv/
```

For a production project, consider storing secrets in environment variables instead of keeping them directly in source code.

## 16. Quick Start

For a quick installation and first run:

```bash
sudo apt update
sudo apt install python3 python3-pip -y

python3 -m pip install psutil requests

python3 main.py
```

Before running the program, make sure the correct **ThingSpeak Write API Key** is configured in `config.py`.

## License

Add the appropriate license here if the project will be published on GitHub.
