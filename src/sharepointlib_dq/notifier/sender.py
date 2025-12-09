"""
Send emails using Microsoft Graph API.

This module provides functionality to send emails using Microsoft Graph API with OAuth2 authentication. It supports
sending HTML-formatted emails with optional file attachments.

Classes
-------
EmailNotifier
    A class to handle email sending operations via Microsoft Graph API.

Notes
-----
The module requires proper Microsoft Azure AD application registration with the following configurations:
- Registered application with client credentials
- Required API permissions for Microsoft Graph
- Mail.Send permissions granted to the application
"""

import base64
import os
from typing import Optional
import requests


class EmailNotifier:
    """
    Send email using Microsoft Graph API.

    A class for sending emails through Microsoft Graph API with OAuth2 authentication.
    Supports HTML content and file attachments.

    Parameters
    ----------
    client_id : str
        The client ID (application ID) from Azure AD app registration
    client_secret : str
        The client secret from Azure AD app registration
    tenant_id : str
        The Azure AD tenant ID
    sender_email : str
        The email address of the sender

    Attributes
    ----------
    _client_id : str
        Stores the client ID for authentication
    _client_secret : str
        Stores the client secret for authentication
    _tenant_id : str
        Stores the tenant ID for authentication
    _sender_email : str
        Stores the sender's email address
    _token : str
        Stores the OAuth access token

    Methods
    -------
    renew_token()
        Force re-authentication to obtain a new access token
    send_email(recipients, subject, message, attachments=None)
        Send an email to specified recipients with optional attachments

    Notes
    -----
    The class automatically handles OAuth2 authentication on initialization and provides methods to send emails and
    manage authentication tokens.
    """

    def __init__(self, client_id: str, client_secret: str, tenant_id: str, sender_email: str) -> None:
        """
        Initialize a notification sender with Microsoft Graph authentication.

        Parameters
        ----------
        client_id : str
            The Azure application (client) ID for authentication.
        client_secret : str
            The Azure client secret key for authentication.
        tenant_id : str
            The Azure directory (tenant) ID for authentication.
        sender_email : str
            The email address that will be used to send notifications.

        Returns
        -------
        None

        Notes
        -----
        The initialization process includes authentication through Microsoft Graph API using the provided credentials.
        The obtained authentication token is stored internally for subsequent API calls.
        """

        self._client_id = client_id
        self._client_secret = client_secret
        self._tenant_id = tenant_id
        self._sender_email = sender_email
        self._token = self._authenticate()

    def _authenticate(self) -> str:
        """
        Authenticate against Microsoft Azure Active Directory and obtain an access token.
        This method performs OAuth2 authentication using client credentials flow to obtain an access token for
        accessing Microsoft Graph API.

        Returns
        -------
        str
            The access token obtained from Azure AD that can be used to authenticate requests to Microsoft Graph API.

        Notes
        -----
        The method uses the following instance attributes that should be set during initialization:
            - self._tenant_id: The Azure AD tenant ID
            - self._client_id: The application (client) ID
            - self._client_secret: The client secret for authentication
        The obtained token is stored in self._token for future use.

        Raises
        ------
        requests.exceptions.RequestException
            If the authentication request fails
        """

        # Authenticate and get access token
        url = f"https://login.microsoftonline.com/{self._tenant_id}/oauth2/v2.0/token"

        # Headers for the token request
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Data for the token request
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "scope": "https://graph.microsoft.com/.default",
        }

        # Make the token request
        response = requests.post(url=url, headers=headers, data=data)
        # response.raise_for_status()

        # Extract the access token from the response
        self._token = response.json()["access_token"]

        return self._token

    def renew_token(self) -> None:
        """
        Force re-authentication to obtain a new access token.

        This method triggers a fresh authentication process and updates the internal token state.

        Returns
        -------
        None
            The new token is stored in the internal _token attribute.

        See Also
        --------
        _authenticate : Method that performs the actual authentication process.

        Notes
        -----
        This method overwrites any existing token value with the newly obtained one.
        """
        self._token = self._authenticate()

    def send_email(self, recipients: list, subject: str, message: str, attachments: Optional[list] = None) -> int:
        """
        Send an email using Microsoft Graph API.

        Parameters
        ----------
        recipients : list
            List of recipient email addresses.
        subject : str
            Subject line of the email.
        message : str
            HTML content of the email body.
        attachments : None or list, optional
            List of file paths to attach to the email. Default is None.

        Returns
        -------
        int
            HTTP status code returned by the API call.

        Notes
        -----
        - The function uses Microsoft Graph API to send emails.
        - The email is sent from the address specified in
        - self._sender_email using the authentication token stored in self._token.
        - Attachments are encoded in base64 format.
        - The function saves the sent email to the Sent Items folder and supports HTML content in the message body.

        Raises
        ------
        requests.exceptions.RequestException
            If the API request fails.
        IOError
            If there are issues reading attachment files.
        """
        # Endpoint
        url = f"https://graph.microsoft.com/v1.0/users/{self._sender_email}/sendMail"

        # Headers
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

        # Email message payload
        payload = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [{"emailAddress": {"address": r}} for r in recipients],
            },
            "saveToSentItems": "true",
        }

        # Handle attachments if provided
        if attachments:
            payload["message"]["attachments"] = []

            for file_path in attachments:
                # Read and encode the file content
                with open(file=file_path, mode="rb") as f:
                    content_bytes = base64.b64encode(s=f.read()).decode(encoding="utf-8")

                # Append attachment to the message
                payload["message"]["attachments"].append(
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": os.path.basename(file_path),
                        "contentBytes": content_bytes,
                    }
                )

        # Send request (email sent: 202 Accepted)
        response = requests.post(url=url, headers=headers, json=payload, verify=True)
        # response.raise_for_status()

        return response.status_code


# eof
