
"""
EmailTemplates class provides a collection of static methods for generating email templates used in various situations
related to error handling and notifications.

Methods
-------
technical_error(recipient_name: str, error_message: str) -> str
    Generates a template for notifying a recipient about a technical error.
informational_alert(recipient_name: str, error_message: str) -> str
    Generates a template for sending an informational alert to a recipient.
validation_followup(recipient_name: str, error_message: str) -> str
    Generates a template for following up with a recipient after validation checks.
"""


class EmailTemplates:
    """
    EmailTemplates class.

    This class provides a collection of static methods for generating email templates for various situations. Each
    template is designed to accept a recipient's name and an error message as input, and returns a formatted email
    string.

    Methods
    -------
    technical_error(recipient_name: str, error_message: str) -> str
        Generates a technical error email template.
    informational_alert(recipient_name: str, error_message: str) -> str
        Generates an informational alert email template.
    validation_followup(recipient_name: str, error_message: str) -> str
        Generates a validation follow-up email template.
    """
    @staticmethod
    def technical_error(recipient_name: str, error_message: str) -> str:
        return (
            f"Dear {recipient_name},<br><br>"
            f"We encountered a technical issue during processing:<br>"
            f"{error_message}<br><br>"
            f"Our team is investigating the matter and will follow up shortly.<br><br>"
            f"Best regards,<br>"
            f"Support Team"
        )

    @staticmethod
    def informational_alert(recipient_name: str, error_message: str) -> str:
        return (
            f"Dear {recipient_name},<br><br>"
            f"Please note the following alert:<br>"
            f"{error_message}<br><br>"
            f"This is for your information only and no action is required at this time.<br><br>"
            f"Best regards,<br>"
            f"Operations Team"
        )

    @staticmethod
    def validation_followup(recipient_name: str, error_message: str) -> str:
        return (
            f"Dear {recipient_name},<br><br>"
            f"Following our recent validation checks, we found:<br>"
            f"{error_message}<br><br>"
            f"Please review and confirm how you wish to proceed.<br><br>"
            f"Best regards,<br>"
            f"Data Quality Team"
        )


# eof
