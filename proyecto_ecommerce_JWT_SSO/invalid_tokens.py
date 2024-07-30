invalid_tokens = set()

def add_invalid_token(token):
    invalid_tokens.add(token)

def is_token_invalid(token):
    return token in invalid_tokens
