from cryptography.fernet import Fernet
import secrets

# fernetKey
print(Fernet.generate_key().decode())
# webserverSecretKey
print(secrets.token_hex(16))