import random
import string


def generate_email() -> str:
    """
    A generator that creates a random email for trianz.com.

    """
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    email = f"{random_string}@trianz.com"
    return email
