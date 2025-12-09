# sharepointlib_dq

- [Description](#package-description)
- [Usage](#usage)
- [Installation](#installation)
- [Docstring](#docstring)
- [License](#license)

## Package Description

Library that provides data quality control for the SharePointLib library. This
package is designed to be used within the Databricks platform, where PySpark
is already available and does not need to be installed as an additional
dependency.

## Usage

### Lakehouse DQ Logs

From a SQL script:

```sql
-- Create the Delta lakehouse table for tracking SharePoint file uploads
-- Includes metadata such as file details, user info, and processing status
-- Table (example): workspace.default.sharepoint_uploader_monitoring_logs
DROP TABLE IF EXISTS workspace.default.sharepoint_uploader_monitoring_logs;
CREATE TABLE workspace.default.sharepoint_uploader_monitoring_logs (
  target STRING,
  key STRING,
  input_file_name STRING,
  file_name STRING,
  user_name STRING,
  user_email STRING,
  modify_date STRING,     -- Should be timestamp
  file_size STRING,       -- Should be INT
  file_row_count STRING,  -- Should be INT
  status STRING,
  rejection_reason STRING,
  file_web_url STRING
)
USING DELTA;
```

From a Python script:

```python
# Error code descriptions
from sharepointlib_dq.core import DQStatusCode

print(DQStatusCode.get_description("SchemaMismatch"))  # DQ FAIL: SCHEMA MISMATCH
print(DQStatusCode.get_description("UnknownCode"))     # UNKNOWN STATUS CODE
```

Status Code Table

| Code                       | Description                             |
| -------------------------- | --------------------------------------- |
| NA                         | NOT APPLICABLE                          |
| EmptyFile                  | DQ FAIL: EMPTY FILE                     |
| SchemaMismatch             | DQ FAIL: SCHEMA MISMATCH                |
| SchemaMismatchAndEmptyFile | DQ FAIL: SCHEMA MISMATCH AND EMPTY FILE |
| InvalidNumericFormat       | DQ FAIL: INVALID NUMERIC FORMAT         |
| InvalidDateFormat          | DQ FAIL: INVALID DATE FORMAT            |

```python
# Metadata and DQ Writer
from sharepointlib_dq.core import SPFileMetadata
from sharepointlib_dq.core import DQWriter

# Simulated SharePoint metadata for a Customer report
meta_dict = {
    "alias": "Customer_Report.xlsx",
    "name": "Customer_Report.xlsx",
    "size": 204800,
    "path": "/SharePoint/Customers",
    "web_url": "https://contoso.sharepoint.com/sites/customers/Customer_Report.xlsx",
    "last_modified_date_time": "2025-11-24T10:30:00Z",
    "last_modified_by_name": "Peter Parker",
    "last_modified_by_email": "peter.parker@contoso.com",
    "id": "file_987"
}

# Init metadata object
metadata = SPFileMetadata(alias="My_File.xlsx", sheet="Customers")

# Build the metadata object (meta_dict -> metadata)
metadata.from_dict(d=meta_dict)

# Add the row_count (number of rows in the file)
metadata.row_count = 1500

# Initialise the writer with the existing STRING-only Delta table
dq_writer = DQWriter(table_name="workspace.default.sharepoint_uploader_monitoring_logs")

# Success case (no rejection reason -> status = SUCCESS)
dq_writer.write_metadata(metadata=metadata)

# Failure case (rejection reason provided -> status = FAIL)
dq_writer.write_metadata(metadata=metadata, reason="DQ FAIL: EMPTY FILE")
```

### Email Notifications

```python
from sharepointlib_dq.notifier import EmailNotifier

# Init email notifications
notifier = EmailNotifier(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id,
    sender_email="sender@example.com"
)

# Send email notification
status_code = notifier.send_email(
    recipients=["peter.parker@example.com"],
    subject="Notification X",
    message="This is<br>a test...",
    attachments=None
)
if status_code in (200, 202):
    print("Email sent")
```

```python
# Using pre-defined templates
from sharepointlib_dq.notifier import EmailTemplates

# Parameters
recipient_name = "Peter Parker"
error_message = "The web is crashing."

# Generate an email using the technical template
message = EmailTemplates.technical_error(
    recipient_name,
    error_message
)

# Print result
print(message)  # Dear Peter Parker...
```

## Installation

Install python and pip if you have not already.

Then run:

```bash
pip install pip --upgrade
```

For production:

```bash
pip install sharepointlib_dq
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:

```bash
git clone https://github.com/aghuttun/sharepointlib_dq.git
cd sharepointlib_dq
pip install -e ".[dev]"
```

## Docstring

The script's docstrings follow the numpydoc style.

## License

BSD License (see license file)

[top](#sharepointlib_dq)
