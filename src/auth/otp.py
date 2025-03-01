import pyotp
from dotenv import load_dotenv
load_dotenv()

def generate_otp(secret_key):
    """
    Generates a one-time password (OTP) based on the given secret key.
    :param secret_key: The shared secret key used for generating the OTP.
    :return: The generated OTP as a string.
    """
    totp = pyotp.TOTP(secret_key)
    return totp.now()

