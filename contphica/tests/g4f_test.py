import g4f

g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking
print(g4f.version)  # Check version
print(g4f.Provider.Ails.params)  # Supported args

#
# from g4f.Provider import (
#     Bard,
#     Bing,
#     You,
# )

# Set with provider
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    provider=g4f.Provider.Phind,
    messages=[{"role": "user", "content": "Find relevant introductory books about computer science covering operating "
                                          "systems, networking, programming and other misc topics"}],
    stream=False
    # stream=True,
)

res = ''.join(response)

print(res)

# for message in response:
#     print(message)