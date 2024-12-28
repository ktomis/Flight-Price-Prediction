import secrets

n = int(input("Input Total Token: "))

for i in range(n):
    print(secrets.token_hex(32))
