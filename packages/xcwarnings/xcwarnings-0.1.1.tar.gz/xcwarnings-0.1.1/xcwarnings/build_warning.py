"""
@File       build_warning.py
@Brief      An Xcode build warning
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""
from xcwarnings.build_warning_scope import BuildWarningScope


class BuildWarning:
    # pylint: disable = too-many-arguments
    """BuildWarning contains metadata about a warning in an xcode build output file"""

    def __init__(
        self,
        file_path: str | None,
        line_number: str | None,
        column: str | None,
        target: str | None,
        project: str | None,
        warning_statement: str,
    ) -> None:
        self.file_path = file_path
        self.line_number = line_number
        self.column = column
        self.target = target
        self.project = project
        self.warning_statement = warning_statement
        if self.file_path is not None:
            self.scope = BuildWarningScope.FILE
        else:
            self.scope = BuildWarningScope.TARGET

    # pylint: enable = too-many-arguments

    def __repr__(self) -> str:
        if self.scope == BuildWarningScope.FILE:
            return (
                f"Warning in file: {self.file_path}:{self.line_number}:{self.column}. "
                + f"Warning: {self.warning_statement}"
            )

        if self.scope == BuildWarningScope.TARGET:
            return f"Warning in target: {self.target}. Project: {self.project}. Warning: {self.warning_statement}"

        raise ValueError(f"Unexpected scope: {self.scope}")

    def __eq__(self, other: object):
        """Checks if currrent instance is eual to the other instance

        Args:
            other (object): object to compare to current instance for equality

        Returns:
            bool: True if objects are equal; otherwise, false.
        """
        if isinstance(other, BuildWarning):
            return (
                (self.file_path == other.file_path)
                and (self.warning_statement == other.warning_statement)
                and (self.project == other.project)
                and (self.target == other.target)
                and (self.line_number == other.line_number)
                and (self.column == other.column)
            )

        return False

    def __ne__(self, other: object) -> bool:
        """Checks if currrent instance is not equal to the other instance

        Args:
            other (object): object to compare to current instance for equality

        Returns:
            bool: True if objects are not equal; otherwise, true.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Returns hash of current instance

        Returns:
            str: Hash of BuildWarning instance
        """
        return hash(self.__repr__())

    def to_dict(self) -> dict[str, object]:
        """Serializes BuildWarning instance into a dictionary."""
        warning_dict: dict[str, object] = {}
        warning_dict["warning"] = self.warning_statement
        if self.scope == BuildWarningScope.FILE:
            warning_dict["file_path"] = self.file_path
            if self.line_number:
                warning_dict["line_number"] = self.line_number
            if self.column:
                warning_dict["column"] = self.column
        elif self.scope == BuildWarningScope.TARGET:
            warning_dict["target"] = self.target
            warning_dict["project"] = self.project
        else:
            raise ValueError(f"Unexpected scope: {self.scope}")
        return warning_dict

    @staticmethod
    def create_file_warning(
        file_path: str,
        line_number: int | None,
        column: int | None,
        warning_statement: str,
    ) -> "BuildWarning":
        """Creates a file level warning

        Args:
            file_path (str): Path to the file where the warning occurs, relative to the repo root.
            line_number (int): Line number where the warning occurs
            column (int): Column within the line where the warning occurs
            warning_statement (str): Warning statement

        Returns:
            BuildWarning: a file level warning
        """
        return BuildWarning(
            file_path, line_number, column, None, None, warning_statement
        )

    @staticmethod
    def create_target_warning(
        target: str, project: str, warning_statement: str
    ) -> "BuildWarning":
        """Creates a target level warning

        Args:
            target (str): Target where the warning occurs
            project (str): Project where the warning occurs
            warning_statement (str): Warning statement

        Returns:
            BuildWarning: a target level warning
        """
        return BuildWarning(None, None, None, target, project, warning_statement)

    @staticmethod
    def from_dict(input_dict: dict[str, object]) -> "BuildWarning":
        """Creates an instance of BuildWarning from given dictinoary.

        Args:
            input_dict: dictionary serialization of BuildWarning

        Returns:
            BuildWarning: An instance of build warning
        """
        return BuildWarning(
            input_dict.get("file_path"),
            input_dict.get("line_number"),
            input_dict.get("column"),
            input_dict.get("target"),
            input_dict.get("project"),
            input_dict["warning"],
        )
