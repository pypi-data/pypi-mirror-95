"""
Provides various implementations of algorithms to generate an Access Token.
"""

import uuid

from twitcher.utils import expires_at
from twitcher import datatype


def tokengenerator_factory(request):
    return UuidTokenGenerator()


class TokenGenerator(object):
    """
    Base class for every token generator.
    """
    def create_access_token(self, valid_in_hours=1):
        """
        Creates an access token.

        TODO: check valid in hours
        TODO: maybe specify how often a token can be used
        """
        token = datatype.AccessToken(
            token=self.generate(),
            expires_at=expires_at(hours=valid_in_hours))
        return token

    def generate(self):
        raise NotImplementedError


class UuidTokenGenerator(TokenGenerator):
    """
    Generate a token using uuid4.
    """
    def generate(self):
        """
        :return: A new token
        """
        return uuid.uuid4().hex
