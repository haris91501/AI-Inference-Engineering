def validate_token_limit(token_limit: int ) -> int:
    if token_limit <=   0:
     raise ValueError("Token limit must be a positive integer.")
    
    return token_limit

limit=validate_token_limit(-5)
print(limit)
