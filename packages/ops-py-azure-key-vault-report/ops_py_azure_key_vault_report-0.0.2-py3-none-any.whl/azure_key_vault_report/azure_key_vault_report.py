#!/usr/bin/env python

import logging
import json
import subprocess
from datetime import datetime


###############################################################################


def set_timestamp(s):
    """Returns a date object of a string in format %Y-%m-%d.

    The string has to be in the correct format, if not None is returned."""

    date_format = "%Y-%m-%d"
    try:
        ts = datetime.strptime(str(s), date_format)
    except ValueError:
        logging.error(f"Unable to convert provided argument '{str(s)}' to timestamp object")
        return

    return ts


class AzureKeyVaultReport(object):
    """
    Fetches the list of secrets in the specified key-vault

    The list is fetched by invoking the following shell command as subprocess:
    'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT'

    The values of 'updated', 'created' and 'expires' are converted to date object
    and the age (in days) is calculated.

    Then a table is generated and sorted by (from top to bottom):
    the oldest 'Expiration' date, then by
    the oldest 'Last Updated' date

    ...

    Attributes
    ----------
    vault_name : str
        The name of the vault
    result : json
        The raw result from the azure cli command
    items : list
        The list of items. After the age of each date element, for each item, is calculated.
    report : str
        The plain text generated table
    table_columns : tuple
        The table columns and width. Defaults to:
        'Secret Name'  : 50
        'Last Updated' : 18
        'Expiration'   : 18
        'Comment'      : 55

    Methods
    -------
    az_cmd()
        Execute the shell command
        'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT'
        and set the result to variable 'result'
    parse_results()
        Parse through the result from the azure cli keyvault output.

        For each item in the result;
        date objects are created from the 'updated', 'created' and 'expires' values and stored as values
        in new X_ts keys.

        The age (in days) is calculated from each of the date objects and stored as values in new X_age keys.

        For each item parsed, a new item is created and added to the items list.
    set_report_header()
        Set the header part of the report:
        At the top row with dashes, then
        left aligned columns with fixed width, separated by |
        then a new row with dashes
    plaintext_report()
        Creates and return the report.

        A 'Comment' column is also created.
        The value of the comment is generated according to the age of 'updated', 'created' and 'expires'.
        A comment if missing 'expires' is also created and added.
    """

    def __init__(self, vault_name):
        """
        Parameters
        ----------
        vault_name : str
            The name of the key vault
        """

        self.vault_name = vault_name
        self.result = {}
        self.items = []
        self.report = ""
        self.table_columns = (
            (50, "Secret Name"),
            (18, "Last Updated"),
            (18, "Expiration"),
            (55, "Comment")
        )

    def az_cmd(self, cmd=""):
        """invoke the 'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT' shell cmd

        Parameters
        ----------
        cmd : str
            The shell subprocess command invoked to fetch the secret list
            (default: 'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT')
        """

        if not cmd:
            cmd = f"az keyvault secret list --vault-name {self.vault_name}"

        az = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        az_stdout = az.stdout.decode("utf-8")
        self.result = json.loads(az_stdout)

    def parse_results(self):
        """parse through the result from the azure cli keyvault cmd output"""
        if not isinstance(self.result, list):
            return

        now = datetime.now()
        for r in self.result:
            item = {}
            if isinstance(r, dict):
                a = r.get("attributes")
                item["name"] = r.get("name")
                if isinstance(a, dict):
                    for k, v in a.items():
                        if "updated" in k or "created" in k or "expires" in k and v:
                            value = v.split("T")[0]
                            item[k] = value
                            ts = set_timestamp(value)
                            item[f"{k}_ts"] = ts
                            item[f"{k}_age"] = (now - ts).days

            self.items.append(item)

    def set_report_header(self):
        """set the header part of the report"""
        # Ensure the report variable is empty before heading is added to it
        self.report = ""

        # Create the dotted line part of the header. The length of the dotted row is each sum of chars from each column
        sep_line = ""
        for col in self.table_columns:
            sep_line += col[0] * "-"
        sep_line += "\n"

        # Parse through each part of the header row. Element 0 is column total width. Element 1 is the actual value.
        header_row = ""
        for col in self.table_columns:
            header_row += f"| {col[1]: <{col[0]}}"

        # Add one dotted line row, the header row and one more dotted line row to the report
        self.report += sep_line
        self.report += header_row.lstrip("|")
        self.report += "\n"
        self.report += sep_line

    def plaintext_report(self):
        """creates and return the report"""
        if not self.report:
            self.set_report_header()

        # Sort the items from top and down
        # First sort by the oldest 'Expiration' date
        # Then sort by the oldest 'Last Updated' date
        items = sorted(self.items, key=lambda x: (str(x.get('expires')), x.get('updated', ' ')), reverse=False)

        for item in items:
            row = ""

            # Get name of the secret. If no name, we skip to next item in the list
            name = item.get("name")
            if not name:
                continue

            # Get the expires and update values
            expires = item.get("expires")
            expires_age = item.get("expires_age")
            updated = item.get("updated")
            updated_age = item.get("updated_age")

            # Add columns to current row
            # The column width is specified by first item in each table_columns tuple

            # First column added is 'Name'. Second column is 'Last Updated'
            row += f" {name: <{self.table_columns[0][0]}}|"
            row += f" {updated: <{self.table_columns[1][0]}}|"

            # Third column added is 'Expiration'. If 'Expiration' value is empty, blank spaces are added instead.
            if expires:
                row += f" {expires: <{self.table_columns[2][0]}}|"
            else:
                row += self.table_columns[2][0] * " "
                row += " |"

            # The last column 'Comment' has to be created before added to the row.
            # The value of 'Comment' is dependent of the info from the expires and update values
            comment = ""
            if isinstance(expires_age, int):
                if expires_age <= 0:
                    comment += f"Will expire in {abs(expires_age)} days. "

                if expires_age > 0:
                    comment += f"Expired {expires_age} days ago. "

            if not expires:
                comment += f"Has no expiration date. "

            if isinstance(updated_age, int):
                comment += f"Updated {updated_age} days ago. "

            # Finally the 'Comment' column is added to the row, along with a linebreak for the row
            row += f" {comment}\n"

            # A little cosmetic touch to avoid plural where it should not be used
            self.report += row.replace(" 1 days", " 1 day")

        if self.report:
            logging.info(f"{self.vault_name} - secret list report generated.")
            return self.report
