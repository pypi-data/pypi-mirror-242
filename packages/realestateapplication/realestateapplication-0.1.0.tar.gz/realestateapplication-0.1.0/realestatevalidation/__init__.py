import re

class Validation:
    def _init_(self, data):
        self.data = data

    def validate(self):
        errors = []
        errors += self.validate_username()
        errors += self.validate_password()
        errors += self.confirm_password()
        return errors

    def validate_username(self):
        errors = []
        username = self.data.get('username', [''])[0]
        if not username:
            errors.append("Username is required")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        elif not re.match("^[A-Za-z0-9]*$", username):
            errors.append("Username must not contain special characters")
        return errors

    def validate_password(self):
        errors = []
        password = self.data.get('password', [''])[0]
        if not password:
            errors.append("Password is required")
        elif len(password) <= 8:
            errors.append("Password must be more than 8 characters long")
        return errors

    def confirm_password(self):
        errors = []
        password = self.data.get('password', [''])[0]
        password2 = self.data.get('password2', [''])[0]
        if password != password2:
            errors.append("Passwords do not match")
        return errors