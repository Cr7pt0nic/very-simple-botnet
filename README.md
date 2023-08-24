# very-simple-botnet
stupidly simple botnet for demonstration purposes on DDoS botnets and how they work.

## About The Project
I was basically bored off my mind and lately there has been a lot of people within the community that I'm in that was interested in learning a lot more about how botnets worked and in general how people make botnets in general. There's lots of great tools out there for very simple Dos (Denial of Service) attacks out there for demonstration but not a lot of great resources for knowing how real botnets function, how they're created, and a lot of source codes out there either don't work, they're outdated, or overall completely shit (Like mine). So I made a very simple, minimalistic, and easily transportable botnet framework which essentially works at all times but with the slowest language (Python). This isn't meant to be used for any real engagements and really this is just for learning. Sure it can be used and applied for different use cases but please don't rip off the project like a skid and claim it's your source. This is only for educational purposes only and I am not responsible for how you use this program in any way shape or form.

### Prerequisites

Python 3.11.2 - 3.11.4 (As long as you have the latest version)

```pip install multithreading```

## Usage

Modify "client.py" on line 104 and 105

python
```py
    server_ip = "CHANGE THIS" # Change C2 IP Address here
    server_port = 4242 # This is where you put the C2 (Command & Control server) port here
```

Modify "server.py" on line 98 and 99
```py
    server_ip = "CHANGE THIS" # change this to the C2 IP Address
    server_port = 4242 # Change this to the C2 Port
```

Run the "server.py" on your VPS server or your test environment
```sh
python3 server.py
```

Run the "client.py" on your client device or system
```sh
python3 client.py
```

You also have the option to compile the client.py script as well using pyinstaller

```sh
pip3 install pyinstaller
pyinstaller --onefile client.py --noconsole
```

