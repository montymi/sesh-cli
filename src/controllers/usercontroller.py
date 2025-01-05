class UserController:
    def __init__(self, user, view):
        self.user = user
        self.view = view

    def _handle_login(self):
        self.view.prompt_for_login()
        username = self.view.prompt_for_username()
        if self.verify_username(username):
            return username, True
        else: return "", False

    def _handle_register(self):
        username = self.view.prompt_for_register()
        result = self.user.create_user(username)
        if result == 0:
            self.view.post_response("User already exists. Please login.")
            return self._handle_login()
        elif result == 1:
            self.view.post_response("User created successfully.")
            return username
        elif result == -1:
            self.view.post_response("An error occurred. Please try again. Note usernames must be 6 characters case-insensitive.")
            return self._handle_register()
        
        return username

    def verify_username(self, username):
        return self.user.authenticate_user(username)