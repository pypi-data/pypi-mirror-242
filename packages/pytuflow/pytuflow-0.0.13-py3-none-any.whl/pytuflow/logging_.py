class Logging_:
    """Compatibility class so routines can be copied from qgis tuflow plugin code."""

    def info(self, msg):
        """Prints a message to the console."""
        print(msg)

    def warning(self, msg):
        """Prints a warning message to the console."""
        print(msg)

    def error(self, msg, additional_info=None):
        """Prints an error message to the console."""
        print(msg)
        if additional_info:
            print(additional_info)


Logging = Logging_()