class EmptyJWKSRemoteURIError(Exception):
    def __init__(self):
        message = ("The public JWK Set URI is empty. It can be due to a misconfiguration on your server. Did you "
                   "export PBL_JWKS_REMOTE_URI environment variable on your system or on your .env file ?")
        print("ERROR: " + message)
        super().__init__(message)


class EmptyJWKSError(Exception):
    def __init__(self):
        message = "Public keys set is empty. jwks.json file might be corrupted, empty or not exist."
        super().__init__(message)


class NotFoundJWKError(Exception):
    def __init__(self, kid: str):
        message = "JWK key was not found for this kid (" + kid + ")"
        super().__init__(message)


class NoAlgorithmProvidedError(Exception):
    def __init__(self, kid: str):
        message = "No algorithm is provided for this JWK (" + kid + ("). It might be cause by a badly encoded of the "
                                                                     "public Json Web Key (JWK).")
        super().__init__(message)
