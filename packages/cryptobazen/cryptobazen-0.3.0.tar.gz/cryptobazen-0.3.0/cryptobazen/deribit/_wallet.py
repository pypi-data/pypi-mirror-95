class Mixin:

    def private_get_deposits(self, currency, count=10, offset=0):
        """
        Retrieve the latest users deposits
        :param currency: BTC or ETH.
        :param count: Number of requested items, default 10
        :param offset: The offset for pagination, default 0
        :return: transfers
        """
        endpoint = '/private/get_deposits'
        params = f'currency={currency}&count={count}&offset={offset}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_transfers(self, currency, count=10, offset=0):
        """
        Adds new entry to address book of given type
        :param currency: BTC or ETH.
        :param count: Number of requested items, default 10
        :param offset: The offset for pagination, default 0
        :return: transfers
        """
        endpoint = '/private/get_transfers'
        params = f'currency={currency}&count={count}&offset={offset}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_withdrawals(self, currency, count=10, offset=0):
        """
        Retrieve the latest users deposits
        :param currency: BTC or ETH.
        :param count: Number of requested items, default 10
        :param offset: The offset for pagination, default 0
        :return: transfers
        """
        endpoint = '/private/get_withdrawals'
        params = f'currency={currency}&count={count}&offset={offset}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)
