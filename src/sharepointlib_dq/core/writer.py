"""
Perform data quality metadata management for Delta tables.

This module provides the DQ class for writing data quality metadata to a
specified Delta table.
It defines a schema for metadata, converts metadata objects to Spark
DataFrames, and persists them.

Classes
-------
DQWriter
    Manage and write data quality metadata to a Delta table.

Notes
-----
- The metadata schema includes fields such as target, key, file information,
user details, and status.
- The write_metadata method append to existing data in the target Delta table.
"""

from .metadata import SPFileMetadata
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import Row
from typing import Optional


class DQWriter:
    """
    Manage and write data quality metadata to a Delta table.

    This class provides methods to persist data quality metadata in a specified
    Delta table.
    It defines a schema for the metadata, converts metadata objects to Spark
    DataFrames, and writes them to the table.

    Parameters
    ----------
    table_name : str
        Name of the Delta table where metadata will be stored.

    Methods
    -------
    write_metadata(metadata)
        Write the provided SPFileMetadata object to the Delta table, append to
        existing data.

    Notes
    -----
    The metadata schema includes fields such as target, key, file information,
    user details, and status.
    """

    def __init__(self, table_name: str):
        """
        Initialize the DQ class with the specified Delta table name.

        Parameters
        ----------
        table_name : str
            Specify the name of the Delta table where metadata will be stored.

        """
        self.table_name = table_name
        self.spark = SparkSession.builder.getOrCreate()

    def write_metadata(
        self, metadata: SPFileMetadata, reason: Optional[str] = None
    ) -> None:
        """
        Write data quality metadata to the table, append to existing data.

        Convert the provided SPFileMetadata object to a Spark DataFrame using
        the defined schema, and persist it to the specified Delta table.

        Parameters
        ----------
        metadata : SPFileMetadata
            File metadata object to be written to the Delta table.
        reason : str | None, optional
            Reason for rejection.

        Returns
        -------
        None

        Notes
        -----
        The metadata schema includes fields such as target, key, file
        information, user details, and status.
        """
        # Define schema
        # target: folder
        # key: filename + email
        # status: SUCCESS / FAIL
        # rejection_reason (DQStatusCode): NOT APPLICABLE, DQ FAIL: SCHEMA MISMATCH, ...
        schema = StructType(
            [
                StructField("target", StringType(), False),
                StructField("key", StringType(), False),
                StructField("input_file_name", StringType(), False),
                StructField("file_name", StringType(), False),
                StructField("user_name", StringType(), False),
                StructField("user_email", StringType(), False),
                StructField("modify_date", StringType(), False),
                StructField("file_size", StringType(), False),
                StructField("file_row_count", StringType(), False),
                StructField("status", StringType(), False),
                StructField("rejection_reason", StringType(), True),
                StructField("file_web_url", StringType(), True),
            ]
        )

        # Compose Key
        key = f"{metadata.name}_{metadata.last_modified_by_email or ''}".strip("_")

        # Status
        status = "FAIL" if reason else "SUCCESS"

        # Map dataclass fields to schema
        mapped_data = {
            "target": metadata.path or "",
            "key": key or "",
            "input_file_name": metadata.name or "",
            "file_name": metadata.alias or "",
            "user_name": metadata.last_modified_by_name or "",
            "user_email": metadata.last_modified_by_email or "",
            "modify_date": metadata.last_modified_date_time or "",
            "file_size": str(metadata.size or 0),
            "file_row_count": str(metadata.row_count or 0),
            "status": status,
            "rejection_reason": reason,  # reason mapped to rejection_reason
            "file_web_url": metadata.web_url or "",
        }

        # Convert metadata to Row
        # row = Row(**metadata.__dict__)
        row = Row(**mapped_data)

        # Create Spark DataFrame
        spark_df = self.spark.createDataFrame([row], schema=schema)

        # Write to Delta table
        # spark_df.write.format("delta").mode("append").saveAsTable(self.table_name)
        # spark_df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(self.table_name)
        spark_df.write.insertInto(self.table_name, overwrite=False)


# eof
