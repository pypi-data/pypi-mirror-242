"""
@File       build_warning_diff_report.py
@Brief      Build warning diff report based on analyzing current warnings against known issues.
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""
from utils import utils
from xcwarnings.build_warning import BuildWarning
from xcwarnings.build_warning_diff import BuildWarningDiff


class BuildWarningDiffReport:
    """Contains a diff result between known warnings and current warnings observed in log file"""

    # pylint: disable = too-many-arguments
    def __init__(
        self,
        diff_warning_got_worse: list[BuildWarningDiff],
        diff_new_warning: list[BuildWarningDiff],
        diff_warning_fixed: list[BuildWarningDiff],
        diff_warning_improved: list[BuildWarningDiff],
        all_warnings: set[BuildWarning],
    ) -> None:
        self.diff_warning_got_worse = diff_warning_got_worse
        self.diff_new_warning = diff_new_warning
        self.diff_warning_fixed = diff_warning_fixed
        self.diff_warning_improved = diff_warning_improved
        self.all_warnings = all_warnings

    # pylint: enable = too-many-arguments

    def success(self) -> bool:
        """Returns whether the warnings quality gate has passed, i.e no new regressions and
        known build warnings file is up to date.

        Returns:
            bool: True if warnings quality gate passed; otherwise False.
        """
        return (
            len(self.diff_warning_got_worse)
            + len(self.diff_new_warning)
            + len(self.diff_warning_fixed)
            + len(self.diff_warning_improved)
            == 0
        )

    def __repr__(self) -> str:
        return (
            f"(worse: {self.diff_warning_got_worse}, new: {self.diff_new_warning}, "
            + f"fixed: {self.diff_warning_fixed}, improved: {self.diff_warning_improved}"
        )

    @staticmethod
    def calculate_diff_report(
        known_issues: dict[BuildWarning, int],
        current_issues: dict[BuildWarning, int],
        all_warnings: set[BuildWarning],
    ) -> "__class__":
        """Generates a report of diff'ed warnings between known issues and current issues found.
        PARAMS:
        - known_issues: Known issues dictionary, where keys are BuildWarning, and value is integer,
                        which is count.
        - current_issues: Current issues dictionary, where keys are BuildWarning, and value is integer,
                        which is count.
        - all_warnings: All warnings encountered in the current build
        RETURNS:
        - An instance of BuildWarningDiffReport of warings that got worse, new warnings or warnings that
        seem to have been fixed or improved.
        """
        diff_warning_got_worse = []
        diff_new_warning = []
        diff_warning_fixed = []
        diff_warning_improved = []

        for current_issue_warning, current_count in current_issues.items():
            current_count = current_issues[current_issue_warning]
            if current_issue_warning in known_issues:
                known_count = known_issues[current_issue_warning]
                if current_count > known_count:
                    utils.print_error_message("Error: The following warning got worse.")
                    utils.print_error_message(
                        f"Known count = {known_count}, Current count = {current_count}."
                    )
                    utils.print_info_message(f"{current_issue_warning}\n")
                    diff_warning_got_worse.append(
                        BuildWarningDiff(
                            current_issue_warning, known_count, current_count
                        )
                    )
            else:
                utils.print_error_message(
                    "Error: Following issue is not a known issue."
                )
                utils.print_info_message(f"{current_issue_warning}\n")
                diff_new_warning.append(
                    BuildWarningDiff(current_issue_warning, 0, current_count)
                )

        for known_issue, known_count in known_issues.items():
            if known_issue not in current_issues:
                utils.print_error_message(
                    "Error: known issue below no longer shows up in the build."
                )
                utils.print_error_message("Please remove it from known issues.")
                utils.print_info_message(str(known_issue))
                diff_warning_fixed.append(BuildWarningDiff(known_issue, known_count, 0))
            else:
                current_count = current_issues[known_issue]
                if current_count < known_count:
                    utils.print_error_message(
                        "Error: Issue has higher count in config than in build."
                    )
                    utils.print_error_message("Please adjust count.")
                    utils.print_error_message(
                        f"Expected count from known issues file: {known_count}. \
                        Found count in the log: {current_count}."
                    )
                    utils.print_info_message(f"{known_issue }\n")
                    diff_warning_improved.append(
                        BuildWarningDiff(known_issue, known_count, current_count)
                    )

        return BuildWarningDiffReport(
            diff_warning_got_worse,
            diff_new_warning,
            diff_warning_fixed,
            diff_warning_improved,
            all_warnings,
        )
