class InvalidModelNameError(Exception):
    """Exception raised for invalid model names in settings.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, model_name, message="Invalid model name in settings"):
        self.model_name = model_name
        self.message = f"{message}: {model_name}"
        super().__init__(self.message)