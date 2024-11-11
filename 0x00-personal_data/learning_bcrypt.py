#!/usr/bin/env python3
"""
Author: Gadoskey
Description: Just playing around with bycrypt looooolll
"""


import bcrypt

# Password to hash
password = "reecejames"

# Generate the salt and hash the password
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode(), salt)

# Save the hashed password to a file
with open("hashed_password.txt", "wb") as f:
    f.write(hashed_password)

print("Password has been hashed and stored in 'hashed_password.txt'.")

is_correct = bcrypt.checkpw(password.encode(), hashed_password)
print("Checking if password is correct:", is_correct)
