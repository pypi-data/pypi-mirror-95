class Mixin:

    def private_get_account_summary(self, currency, extended='false'):
        """
        Retrieves user account summary.
        :param currency: BTC or ETH.
        :param extended: Include additional fields
        :return: user account summary
        """
        endpoint = '/private/get_account_summary'
        params = f'currency={currency}&extended={extended}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_positions(self, currency, kind):
        """
        Retrieve user positions.
        :param currency: BTC or ETH.
        :param kind: future or option
        :return: positions
        """
        endpoint = '/private/get_positions'
        params = f'currency={currency}&kind={kind}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)
