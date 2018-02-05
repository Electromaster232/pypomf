import secrets

print("Copyright 2018 DJ-Electro.me. This software is part of the Flask-powered dj-electro.me file hosting site.")
print("How many bits to generate? IMPORTANT: 32-bit minimum for security.")
bits = input()
bitsint = int(bits)
key = secrets.token_hex(bitsint)
print("Here is your key, ensure you add it to the database!")
print(key)
