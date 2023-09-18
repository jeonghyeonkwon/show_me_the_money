class UserResponse:
    userId: str
    hashedPwd: bytes

    def __init__(self, userId, hashedPwd):
        self.userId = userId
        self.hashedPwd = hashedPwd


class LoginResponse:
    userId: str
    token: str

    def __init__(self, userId: str, token):
        self.userId = userId
        self.token = token
