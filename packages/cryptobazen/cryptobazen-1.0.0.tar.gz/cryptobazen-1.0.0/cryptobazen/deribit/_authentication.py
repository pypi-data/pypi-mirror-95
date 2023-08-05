class Mixin:

    def public_auth(self):
        """
        Retrieve an Oauth access token, to be used for authentication of 'private' requests.
        :return: Oauth access token
        """
        endpoint = '/public/auth'
        params = ''
        return self.api_query(method='GET', params=params, endpoint=endpoint)