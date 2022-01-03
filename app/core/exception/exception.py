class AuthFailedException(Exception):

    def __str__(self) -> str:
        return 'Auth failed'