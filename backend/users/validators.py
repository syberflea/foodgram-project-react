from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    flags = 0
