import g4f
from g4f.Provider.selenium import Phind

g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # Check version
print(g4f.Provider.Ails.params)  # Supported args

# Set with provider
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    provider=Phind,
    messages=[{"role": "user", "content": "Find relevant introductory books about computer science covering operating "
                                          "systems, networking, programming and other misc topics"}],
    stream=False,
    # auth=True,
    # cookies={"__Secure-next-auth.session-token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..bTV6-ok8A9soBBXl.jyaW3rBvzkcabYUAoPsVnY6iVqB8IAyhSe1uiPFU7h4WrfANl6hJVpuJKWHppgdxHZ0KAxH_0xOwREnj5q-bQLEE7RVX2-5TY0mlXyNdTX90OORBuUKTNiITiIHZYZrv6Mv9uMWg73PsDXtlcf5LyDL9h8hujYzr3rqXfMe7qD5L7PWsJ4IZ8kxnkdDPNWWCxGWGguhLRpHl-L110L9H8CFLJMmPkOmqClHLtelCxDu2Z5qVJdrY-t7MQawz-uOPNLhwkw.tjU8EYqxKQTO_X8zR46vew"}
    # stream=True,
)

res = ''.join(response)

print(res)

# for message in response:
#     print(message)