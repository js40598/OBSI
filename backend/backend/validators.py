from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
import re
import logging
logger = logging.getLogger(__name__)


# checks if provided username is not in use already
class UniqueUsernameValidator:
    def __init__(self, value, klass=User, message=None):
        self.klass = klass
        self.value = value
        self.message = message if message else 'Provided username is already in use'
        self.is_valid = self.__validate()

    def __validate(self):
        try:
            self.klass.objects.get(username=self.value)
            return False
        except ObjectDoesNotExist:
            return True
        except MultipleObjectsReturned:
            logger.error(f'Userename: "{self.value}" occurs multiple times in "{self.klass}" table.')
            return False


# checks if length of provided value is correct
class LengthValidator:
    def __init__(self, value, min_length=6, max_length=50, message=None):
        self.value = value
        self.min_length = min_length
        self.max_length = max_length
        self.message = message if message else f'Username length must be between {min_length} and {max_length} digits'
        self.is_valid = self.__validate()

    def __validate(self):
        if len(self.value) < int(self.min_length) or len(self.value) > int(self.max_length):
            return False
        else:
            return True


# checks if provided email is not in use already
class UniqueEmailValidator:
    def __init__(self, value, klass=User, message=None):
        self.klass = klass
        self.value = value
        self.message = message if message else 'Provided email is already in use'
        self.is_valid = self.__validate()

    def __validate(self):
        try:
            self.klass.objects.get(email=self.value)
            return False
        except ObjectDoesNotExist:
            return True
        except MultipleObjectsReturned:
            logger.error(f'Email address: "{self.value}" occurs multiple times in "{self.klass}" table.')
            return False


# checks if provided value is not too long
class MaxLengthValidator:
    def __init__(self, value, field, max_length=50, message=None):
        self.value = value
        self.max_length = max_length
        self.message = message if message else f'{field} cannot be longer than {max_length} digits'
        self.is_valid = self.__validate()

    def __validate(self):
        if len(self.value) > int(self.max_length):
            return False
        else:
            return True


# checks if provided passwords matches each other
class PasswordsMatchValidator:
    def __init__(self, password1, password2, message=None):
        self.password1 = password1
        self.password2 = password2
        self.message = message if message else 'Provided passwords does not match'
        self.is_valid = self.__validate()

    def __validate(self):
        if self.password1 == self.password2:
            return True
        else:
            return False


# checks if password contains special character
class PasswordContainSpecialCharacterValidator:
    def __init__(self, value, message=None):
        self.value = value
        self.message = message if message else 'Password must contain special characters'
        self.is_valid = self.__validate()

    def __validate(self):
        for character in self.value:
            if not character.isdigit() and not character.isalpha():
                return True
        return False


# checks if password contains digit
class PasswordContainDigitValidator:
    def __init__(self, value, message=None):
        self.value = value
        self.message = message if message else 'Password must contain digit'
        self.is_valid = self.__validate()

    def __validate(self):
        for character in self.value:
            if character.isdigit():
                return True
        return False


# checks if password contains uppercase character
class PasswordContainUppercaseValidator:
    def __init__(self, value, message=None):
        self.value = value
        self.message = message if message else 'Password must contain uppercase characters'
        self.is_valid = self.__validate()

    def __validate(self):
        for character in self.value:
            if character.isupper():
                return True
        return False


# checks if password contains lowercase character
class PasswordContainLowercaseValidator:
    def __init__(self, value, message=None):
        self.value = value
        self.message = message if message else 'Password must contain lowercase characters'
        self.is_valid = self.__validate()

    def __validate(self):
        for character in self.value:
            if character.islower():
                return True
        return False
