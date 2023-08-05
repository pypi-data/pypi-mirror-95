class Mixin:

    def private_user_order_history_by_currency(self, currency, kind, count=20, offset=0, include_old='true', include_unfilled='true'):
        """
        Retrieves history of orders that have been partially or fully filled.
        :param currency: BTC or ETH.
        :param kind: Instrument kind (option or future), if not provided instruments of all kinds are considered
        :param count: Number of requested items, default 20
        :param offset: The offset for pagination, default - 0
        :param include_old: Include trades older than a few recent days, default - false
        :param include_unfilled: Include in result fully unfilled closed orders, default - false
        :return: orders
        """
        endpoint = '/private/get_order_history_by_currency'
        params = f'currency={currency}&kind={kind}&count={count}&offset={offset}&include_old={include_old}&include_unfilled={include_unfilled}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_user_trades_by_currency(self, currency, kind, count=10, start_id=None, end_id=None, include_old='true', sorting='asc'):
        """
        Retrieve the latest user trades that have occurred for instruments in a specific currency symbol.
        :param currency: BTC or ETH.
        :param kind: Instrument kind (option or future), if not provided instruments of all kinds are considered
        :param count: Number of requested items, default 10
        :param start_id: The ID number of the first trade to be returned
        :param end_id: The ID number of the last trade to be returned
        :param include_old: Include trades older than a few recent days, default - false
        :param sorting: Direction of results sorting (default value means no sorting, results will be returned in order in which they left the database)
        :return: trades
        """
        endpoint = '/private/get_user_trades_by_currency'
        params = f'currency={currency}&kind={kind}&count={count}&include_old={include_old}&sorting={sorting}'
        if start_id is not None:
            params += f'&start_id={start_id}'
        if end_id is not None:
            params += f'&start_id={end_id}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_user_trades_by_order(self, order_id, sorting='asc'):
        """
        Retrieve the list of user trades that was created for given order
        :param order_id: The order id
        :param sorting: Direction of results sorting (default value means no sorting, results will be returned in order in which they left the database)
        :return: Given trade
        """
        endpoint = '/private/get_user_trades_by_order'
        params = f'order_id={order_id}&sorting={sorting}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_settlement_by_currency(self, currency, type, count=10):
        """
        Retrieves settlement, delivery and bankruptcy events that have affected your account.
        :param currency: BTC or ETH.
        :param type: Settlement type. settlement, delivery or bankruptcy
        :param count: Number of requested items, default 10
        :return: settlements
        """
        endpoint = '/private/get_settlement_history_by_currency'
        params = f'currency={currency}&type={type}&count={count}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

