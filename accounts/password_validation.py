from django.core.exceptions import ValidationError
import requests
import hashlib


class LeakedPasswordValidator:
    def __init__(self):
        pass

    def _request_api_data(self, query_char):
        url = 'https://api.pwnedpasswords.com/range/' + query_char
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error fetching: {res.status_code}')
        return res

    def _get_password_leaks_count(self, hashes, hashed):
        hashes = {line.split(':')[0]: line.split(':')[1]
                  for line in hashes.text.splitlines()}
        if hashed in hashes.keys():
            return hashes[hashed]
        return 0

    def _pwned_api_check(self, password):
        sha1password = hashlib.sha1(
            password.encode('utf-8')).hexdigest().upper()
        first5_char, tail = sha1password[:5], sha1password[5:]
        response = self._request_api_data(first5_char)
        return self._get_password_leaks_count(response, tail)

    def validate(self, password, user=None):
        leaks_count = self._pwned_api_check(password)
        if leaks_count:
            raise ValidationError(
                f"Oh no! This password has been leaked {leaks_count} times. You should change it",
                code='password_has_been_pwned'
            )

    def get_help_text(self):
        return "Password will be checked against a list of previously leaked ones to avoid using such an insecure password."
