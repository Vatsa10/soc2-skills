AWS_KEY = "AKIAABCDEFGHIJKLMNOP"
def save(user):
    db.insert(email=user.email, date_of_birth=user.dob)
