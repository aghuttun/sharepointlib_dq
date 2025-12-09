"""
Provide utilities for handling data quality status codes.

Define the DQStatusCode class to map status codes to human-readable descriptions
for use in data validation workflows.

Classes
-------
DQStatusCode
    Represent data quality status codes and retrieve their descriptions.

Examples
--------
Get a description for a status code:

    desc = DQStatusCode.get_description("SchemaMismatch")
    # Returns: "DQ FAIL: SCHEMA MISMATCH"
"""


class DQStatusCode:
    """
    Represent data quality status codes and their descriptions.

    Use this class to retrieve human-readable descriptions for
    specific data quality status codes encountered during data
    validation processes.

    Attributes
    ----------
    _codes : dict
        Mapping of status code strings to their descriptions.

    Methods
    -------
    get_description(code)
        Return the description for a given status code.
    """

    _codes = {
        "NA": "NOT APPLICABLE",
        "EmptyFile": "DQ FAIL: EMPTY FILE",
        "SchemaMismatch": "DQ FAIL: SCHEMA MISMATCH",
        "SchemaMismatchAndEmptyFile": "DQ FAIL: SCHEMA MISMATCH AND EMPTY FILE",
        "InvalidNumericFormat": "DQ FAIL: INVALID NUMERIC FORMAT",
        "InvalidDateFormat": "DQ FAIL: INVALID DATE FORMAT",
    }

    @classmethod
    def get_description(cls, code):
        """
        Return the description for a given data quality status code.

        Parameters
        ----------
        code : str
            Data quality status code to look up.

        Returns
        -------
        str
            Human-readable description of the status code. If the code is not found,
            return "UNKNOWN STATUS CODE".
        """
        return cls._codes.get(code, "UNKNOWN STATUS CODE")


# eof
