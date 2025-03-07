from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return(
            str(user.pk) + str(timestamp) + str(user.is_active)
        )
    
class PasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return(
            str(user.pk) + str(timestamp) + str(user.is_active)
        )
    
account_activation_token = AccountActivationTokenGenerator()
password_reset_token = PasswordResetTokenGenerator()