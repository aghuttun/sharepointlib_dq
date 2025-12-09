"""
SharePoint File Metadata Structure

This module defines a dataclass for encapsulating file metadata, including
SharePoint attributes, sheet information, and optional row count. It supports
logging, auditing, and persistence of file-related events.

Classes
-------
SPFileMetadata
    Represents metadata for files, including additional attributes such as
    sheet name and number of rows.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import json


@dataclass
class SPFileMetadata:
    """
    Metadata for report files.

    This dataclass stores file-related metadata, including attributes retrieved
    from SharePoint and additional fields required for processing.

    Attributes
    ----------
    alias : str
        Alias or expected filename for the file. Defaults to "Unknown".

    id : str, optional
        Unique identifier of the file.
    name : str, optional
        Actual name of the file.
    extension : str, optional
        File extension (e.g., 'xlsx').
    size : int, optional
        Size of the file in bytes.
    path : str, optional
        Path or folder where the file is located.
    web_url : str, optional
        SharePoint web URL for accessing the file.
    created_date_time : str, optional
        Creation timestamp of the file.
    last_modified_date_time : str, optional
        Last modification timestamp of the file.
    last_modified_by_name : str, optional
        Name of the user who last modified the file.
    last_modified_by_email : str, optional
        Email of the user who last modified the file.

    sheet : str
        Name of the sheet in the Excel file. Defaults to "Sheet1".
    row_count : int, optional
        Number of rows in the file, if known.
    """

    # Main fields
    alias: str = "Unknown"

    # Dictionary fields
    id: Optional[str] = None
    name: Optional[str] = None
    extension: Optional[str] = None
    size: Optional[int] = None
    path: Optional[str] = None
    web_url: Optional[str] = None
    created_date_time: Optional[str] = None
    last_modified_date_time: Optional[str] = None
    last_modified_by_name: Optional[str] = None
    last_modified_by_email: Optional[str] = None

    # Additional fields
    sheet: str = "Sheet1"
    row_count: Optional[int] = None

    def from_dict(self, d: Dict[str, Any]) -> None:
        """
        Update the current SPFileMetadata instance with values from a dictionary.

        This method iterates through the provided dictionary and updates the
        attributes of the instance if they exist in the dataclass. Attributes
        not present in the dictionary will retain their current values.

        Parameters
        ----------
        d : dict
            Dictionary containing metadata fields to update.

        Notes
        -----
        - Only attributes that already exist in the dataclass are updated.
        - Existing values are preserved if the corresponding key is not in the
        dictionary.
        - This method does not return a new object; it modifies the current
        instance in place.
        """
        for key, value in d.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_json(self) -> str:
        """
        Convert the FileMetadata instance to a JSON-formatted string.

        Serializes all attributes into a human-readable JSON string for logging,
        transmission, or storage.

        Returns
        -------
        str
            JSON representation of the FileMetadata instance.
        """
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


# eof
