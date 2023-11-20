class MappyError(Exception):
    pass

class InvalidTypeError(MappyError):
    def __init__(self, received_value, expected_value):
        self.expected_value = expected_value
        self.received_type = type(received_value).__name__
        self.received_value = received_value
        self.message = (
            f"\n\n:: Mappy Error ::\n"
            f"\nInvalid Type Received:\n"
            f"- 🚫 Received: {received_value} (type: {self.received_type})\n"
            f"- ✅ Expected: {expected_value}\n"
            f"\nTo fix this error:\n"
            f"  Ensure the input matches the expected format.\n"
        )
        super().__init__(self.message)

class InvalidValueError(MappyError):
    def __init__(self, received_value):
        self.received_value = received_value
        self.message = (
            f"\n\n:: Mappy Error ::\n"
            f"\nInvalid Value Received:\n"
            f"- 🚫 Received: {received_value}\n"
            f"- ✅ Expected: Correct address\n"
            f"\nTo fix this error:\n"
            f"  Ensure the input value is one of the expected values.\n"
        )
        super().__init__(self.message)

class APIConnectionError(MappyError):
    def __init__(self, url):
        self.url = url
        self.message = (
            f"\n\n:: Mappy Error ::\n"
            f"\nAPI Connection Error:\n"
            f"- 🔌 Failed to connect to: {url}\n"
            f"\nTo fix this error:\n"
            f"  Check your internet connection and the API URL.\n"
        )
        super().__init__(self.message)

class APITimeoutError(MappyError):
    def __init__(self, after_seconds):
        self.after_seconds = after_seconds
        self.message = (
            f"\n\n:: Mappy Error ::\n"
            f"\nAPI Timeout Error:\n"
            f"- ⏰ Timeout after: {after_seconds} seconds\n"
            f"\nTo fix this error:\n"
            f"  Check your internet connection and consider increasing the timeout limit.\n"
        )
        super().__init__(self.message)

class ResponseError(MappyError):
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason
        self.message = (
            f"\n\n:: Mappy Error ::\n"
            f"\nInvalid API Response:\n"
            f"- 🚫 Status Code: {status_code}\n"
            f"- 🚫 Reason: {reason}\n"
            f"\nTo fix this error:\n"
            f"  Check the status code and reason for the error and retry the request if appropriate.\n"
        )
        super().__init__(self.message)