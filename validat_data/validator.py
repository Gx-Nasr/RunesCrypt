import json
from hash_sha_256.sha_256 import sha_256

def validate_password(password):
    if len(password) < 8:
        return "Password must contain at least 8 characters"
    if len(password) > 32:
        return "Password cannot exceed 32 characters"

    lowercase = set("abcdefghijklmnopqrstuvwxyz")
    uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = set("0123456789")
    special = set("!@#$&*-+=_")
    a_bool = u_bool = n_bool = s_bool = False

    for c in password:
        if c in lowercase:
            a_bool = True
        elif c in uppercase:
            u_bool = True
        elif c in numbers:
            n_bool = True
        elif c in special:
            s_bool = True
        else:
            return "Invalid characters"

    if not u_bool:
        return "Password must contain at least 1 uppercase letter"
    if not a_bool:
        return "Password must contain at least 1 lowercase letter"
    if not n_bool:
        return "Password must contain at least 1 number"
    if not s_bool:
        return "Password must contain 1 special char (!@#$&*-+=_)"

    return None


def validate_login(login):
    if len(login) < 4:
        return "Login must contain at least 4 characters"
    if len(login) > 12:
        return "Login cannot exceed 12 characters"

    for c in login:
        if not c.isalpha():
            if c not in '_-':
                return "invalid character"
            
    return None


def validat_password_login(login: str, password: str) -> bool | str:
    if len(login) > 12:
        return "Login cannot exceed 12 characters"
    if len(password) > 32:
        return "Password cannot exceed 32 characters"
    
    login = sha_256(login)
    password = sha_256(password)

    with open(".user.json", "r") as f:
        user_dict = json.load(f)
    if login != user_dict["login"] or password != user_dict["password"]:
        return "Login failed !"
    else:
        return None
