class Mixin:

    def public_get_book_summary_by_instrument(self, instrument_name: str):
        """
        Retrieves the summary information such as open interest, 24h volume, etc. for a specific instrument.
        :param instrument: The name of the option or future
        :return: book summary info
        """
        endpoint = '/public/get_book_summary_by_instrument'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_historical_volatility(self, currency: str):
        """
        Provides information about historical volatility for given cryptocurrency.
        :param currency: BTC or ETH.
        :return: Volatility data
        """
        endpoint = '/public/get_historical_volatility'
        params = f'currency={currency}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_instrument(self, instrument_name: str):
        """
        Retrieves information about instrument
        :param instrument_name: BTC or ETH.
        :return: Instrument data
        """
        endpoint = '/public/get_instrument'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_instruments(self, currency: str, kind: str, expired: str):
        """
        Retrieves available trading instruments. This method can be used to see which instruments are available for trading,
        or which instruments have existed historically.
        :param currency: BTC or ETH.
        :param kind: future or option
        :param expired: true or false. Means if the future or option is still open or not
        :return: Instrument data
        """
        endpoint = '/public/get_instruments'
        params = f'currency={currency}&kind={kind}&expired={expired}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_last_trades(self, instrument_name: str):
        """
        Retrieve the latest trades that have occurred for a specific instrument.
        :param instrument_name: currency: BTC or ETH.
        :return: latest data with trades of a instrument
        """
        endpoint = '/public/get_last_trades_by_instrument'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_tradingview_chart_data(self, instrument_name: str, start_timestamp: int, end_timestamp: int, resolution: str):
        """
        Publicly available market data used to generate a TradingView candle chart.
        :param instrument_name: Instrument name
        :param start_timestamp: The earliest timestamp to return result for
        :param end_timestamp: The most recent timestamp to return result for
        :param resolution: Chart bars resolution given in full minutes or keyword 1D (only some specific resolutions are supported)
        :return: json with candles
        """
        endpoint = '/public/get_tradingview_chart_data'
        params = f'instrument_name={instrument_name}&start_timestamp={start_timestamp}&end_timestamp={end_timestamp}&resolution={resolution}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_ticker(self, instrument_name: str):
        """
        Get ticker for an instrument.
        :param instrument_name: The name of the option or future
        :return: a response with all information about the questioned instrument
        """
        endpoint = '/public/ticker'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)