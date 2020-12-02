class ConnectorBase:
    """Interface class for Conncetor"""
    def connect(self, config: dict):
        raise NotImplementedError