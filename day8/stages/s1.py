def get_user(email:str) -> str:
    db = {"sam@gmail.com" : "user999"}
    return db.get(email.lower(), "not found")


print(get_user("sam@gmail.com"))