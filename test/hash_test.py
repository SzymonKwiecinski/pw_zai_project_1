from passlib.hash import argon2, pbkdf2_sha256
from passlib.context import CryptContext
import passlib
import secrets


# salt = secrets.token_bytes(32)
# print(salt)
haslo = "test"

alg = pbkdf2_sha256
# alg.



hash_pass1 = alg.hash(haslo, salt_size=32)
print(len(hash_pass1))
print(hash_pass1)
for k in hash_pass1.split("$"):
    if k:
        print(f"{k}<>{len(k)}")
xd2 = hash_pass1.split("$")[-1]
print(xd2)
print(len(xd2))
print(len(xd2.encode()))

xd = hash_pass1.split("$", 2)[2]
alg_type ='pbkdf2-sha256'
print(xd)
hash_pass2 = alg.verify(haslo, f"${alg_type}${xd}")
hash_pass3 = alg.hash(haslo)

print(hash_pass1)
print(hash_pass2)
print(hash_pass3)


# print(a2.verify(haslo, hash_pass))