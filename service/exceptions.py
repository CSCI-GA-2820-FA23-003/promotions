class ConfirmationRequiredError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Confirmation is required to delete the object."):
        self.message = message
        super().__init__(self.message)
