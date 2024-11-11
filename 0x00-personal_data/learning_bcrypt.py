#!/usr/bin/env python3
"""
Author: Gadoskey
Description: Just playing around with bycrypt looooolll
"""


import bcrypt

#The Password to hash and printing it out
password = "reecejames"
print(password)

# Generate the salt, hash the passworda and print it out as well
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password.encode(), salt)
print(hash_password)


# Save the hashed password to hashed_password.txt
with open("hashed_password.txt", "wb") as f:
    f.write(hashed_password)

print("Password has been hashed and stored in 'hashed_password.txt'.")

is_correct = bcrypt.checkpw(password.encode(), hashed_password)
print("Checking if password is correct:", is_correct)
