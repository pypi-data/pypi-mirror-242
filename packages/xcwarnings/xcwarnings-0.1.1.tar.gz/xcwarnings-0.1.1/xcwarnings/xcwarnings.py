"""
@File       xcwarnings.py
@Brief      Module that detects new build warnings
@Author     rajaber
@Date       03-22-2021
@copyright  Microsoft Corporation. All rights reserved.
"""
import argparse
import json
import os
import re
import copy

from utils import utils
from xcwarnings.build_warning import BuildWarning
from xcwarnings.build_warning_diff_report import BuildWarningDiffReport

# AUTO_TRIAGGED_TAG = 'AutoTriagged'
# FAILED_AUTO_TRIAGGED_TAG = 'NoAutoTriagged'


def get_arguments():
    """Get arguments input from the script execution
    RETURNS:
    - Arguments to use in script
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "xcode_build_output_file_path", help="Path to the xcode output file"
    )
    parser.add_argument(
        "--known_build_warnings_file_path",
        nargs=1,
        help="Full path to a file with known build warnings",
    )
    parser.add_argument(
        "--source_root", required=True, help="File path for the root of the source code"
    )
    parser.add_argument(
        "--generate_baseline",
        action="store_true",
        default=False,
        help="Whether a new baseline of known issues should be generated.",
    )
    return parser.parse_args()


def read_known_issues(
    known_build_warnings_file_path: str | None,
) -> dict[BuildWarning, int]:
    """Reads known build issues per optional configuration file.
    PARAMS:
    - known_build_warnings_file_path: Path to build warnings file, or None if no such file exists.
    RETURNS:
    - Dictionary of known build issues where the keys are the warnings of type BuildWarning,
      and the values are the counts of how many such warnings are expected in their respective files
      or project targets.
      Note: Those BuildWarning instances are not expected to contain line and column numbers because
      those tend to change as new content is added/removed.
    """

    if known_build_warnings_file_path is None:
        utils.print_info_message(
            "known_build_warnings_file_path not specified. No known warnings."
        )
        return {}

    utils.print_info_message(
        f"known_build_warnings_file_path = {known_build_warnings_file_path}\n"
    )

    with open(known_build_warnings_file_path, encoding="utf-8") as file:
        data_file = file.read()

    known_issues_list = json.loads(data_file)
    return {
        BuildWarning.from_dict(known_issue): known_issue["count"]
        for known_issue in known_issues_list
    }


def scan_line_for_warning(line: str, source_root: str) -> BuildWarning | None:
    """Scans given line from build output for a warning.
    PARAMS:
    - line: Contents of a line of a build output file (as a string)
    - source_root: File path for the root of the source code
    RETURNS:
    - BuildWarning instance or None if no warning is found in this line.
    """

    file_scope_warning_pattern = r"^(.*):(\d+):(\d+): warning: (.*)$"
    target_scope_warning_pattern = (
        r"^warning: (.*) \(in target '(.*)' from project '(.*)'\)$"
    )

    file_scope_warning_search = re.search(file_scope_warning_pattern, line)
    if file_scope_warning_search:
        file_path = file_scope_warning_search.group(1)
        line_number = int(file_scope_warning_search.group(2))
        column = int(file_scope_warning_search.group(3))
        warning_statement = file_scope_warning_search.group(4)

        if not file_path.startswith(os.path.abspath(source_root) + os.sep):
            # Exclude files not under source root
            return None

        relative_file_path = os.path.relpath(file_path, source_root)
        build_warning = BuildWarning.create_file_warning(
            relative_file_path, line_number, column, warning_statement
        )
        return build_warning

    target_scope_warning_search = re.search(target_scope_warning_pattern, line)
    if target_scope_warning_search:
        warning_statement = target_scope_warning_search.group(1)
        target = target_scope_warning_search.group(2)
        project = target_scope_warning_search.group(3)
        build_warning = BuildWarning.create_target_warning(
            target, project, warning_statement
        )
        return build_warning

    return None


def scan_for_warnings(output_file_path: str, source_root: str) -> [BuildWarning]:
    """Scans the given file for all build warnings
    PARAMS:
    - output_file_path: Path to a file containing logs from xcode build command
    RETURNS:
    - source_root: File path for the root of the source code
    - An array of BuildWarning instances found. Empty array if none is found.
      Note: there may be duplicate build warnings if output file contains multiple lines refering to
      the same warning messages. They will show up as duplicate entries in the returned array.
    """
    with open(output_file_path, encoding="utf-8") as file:
        data_file = file.readlines()

    warnings: [BuildWarning] = []

    for line in data_file:
        warning = scan_line_for_warning(line, source_root)
        if warning:
            warnings.append(warning)

    return warnings


def get_warnings(output_file_path: str, source_root: str) -> set[BuildWarning]:
    """Gets all warnings found in given output file, deduped, and aggregated on the file level.
    PARAMS:
    - output_file_path: Path to a file containing logs from xcode build command
    - source_root: File path for the root of the source code
    RETURNS:
    - An array of BuildWarning instances found. Empty array if none is found.
      Note: Duplicate build warnings in the output file with multiple lines refering to
      the same warning messages are deduped and will count as one error.
    """
    utils.print_info_message(
        f"Extracting warnings from build output file: {output_file_path}"
    )

    warnings = scan_for_warnings(output_file_path, source_root)
    warnings_deduped = set(warnings)
    utils.print_info_message(
        f"Total number of warning instances found in build log file: {len(warnings_deduped)}."
    )

    return warnings_deduped


def get_aggregated_warnings(warnings: set[BuildWarning]) -> dict[BuildWarning, int]:
    """Aggregates warnings so that all warnings in one file or target, have one entry in the output dictionary
    along with a count of how many times it occured
    PARAMS:
    - warnings: Array of warnings found
    RETURNS:
    - A dictionary of BuildWarning instances found. Each entry corresponds to one file or project/target.
    """

    warnings_copy = copy.deepcopy(warnings)

    for warning in warnings_copy:
        # Clear line number and column so that we can aggregate at the file level
        warning.line_number = None
        warning.column = None

    warning_dict: dict[BuildWarning, int] = {}
    for warning in warnings_copy:
        warning_dict[warning] = warning_dict.get(warning, 0) + 1

    return warning_dict


def generate_baseline(
    output_file_path: str, output_known_issues_file: str, source_root
) -> None:
    """Gets baseline for all known issues identified in the output file path, and writes them
    to a known issues file at the given path.
    PARAMS:
    - output_file_path: Path to a file containing logs from xcode build command
    - output_known_issues_file: Path to a new file that this method will write, summarizing issues
    discovered in output file path.
    - source_root: File path for the root of the source code
    RETURNS:
    - Writes known issues in JSON format at output_known_issues_file. Does not return value.
    """
    utils.print_info_message("Generating baseline 📈")
    warnings = get_warnings(output_file_path, source_root)
    warnings_with_count = get_aggregated_warnings(warnings)
    supressions = []

    for unique_warning, count in warnings_with_count.items():
        supression_entry = unique_warning.to_dict()
        supression_entry["count"] = count
        supressions.append(supression_entry)

    known_issues_json = json.dumps(supressions, indent=4)

    with open(output_known_issues_file, "w", encoding="utf-8") as text_file:
        text_file.write(known_issues_json)

    utils.print_success_message(
        f"Baseline generated at file: {output_known_issues_file}"
    )


def analyze(
    xcode_build_output_file_path: str,
    known_build_warnings_file_path: str | None,
    source_root: str,
) -> BuildWarningDiffReport:
    """Compares warnings present in the given output file with known warnings in
       known_build_warnings_file_path.
    PARAMS:
    - xcode_build_output_file_path: Path to a file containing logs from xcode build command
    - output_known_issues_file: Path to file with known build issues, or None if no known issues.
    - source_root: File path for the root of the source code
    RETURNS:
    - An instance of BuildWarningDiffReport
    """
    known_issues = read_known_issues(known_build_warnings_file_path)
    current_warnings = get_warnings(xcode_build_output_file_path, source_root)
    aggregated_warnings = get_aggregated_warnings(current_warnings)
    return BuildWarningDiffReport.calculate_diff_report(
        known_issues, aggregated_warnings, current_warnings
    )


def main():
    """Parses xcode build output file, and confirms there are no new warning errors.
    When --generate_baseline argument is passed, a baseline is generated with warnings found
    in given output log.
    PARAMS:
    - xcode_build_output_file_path: Path to a file containing logs from xcode build command
    - output_known_issues_file: Path to file with known build issues, or None if no known issues.
    RETURNS:
    - An instance of BuildWarningDiffReport
    """

    args = get_arguments()

    utils.print_info_message("Hello. Staring Build Warnings Detector ⚠️ ")

    if args.generate_baseline:
        if not args.known_build_warnings_file_path:
            raise ValueError(
                "known_build_warnings_file_path is required if "
                "generate_baseline option is specified."
            )

        generate_baseline(
            output_file_path=args.xcode_build_output_file_path,
            output_known_issues_file=args.known_build_warnings_file_path[0],
            source_root=args.source_root,
        )
        return 0

    utils.print_info_message("Analyzing current warnings against known issues if any🔬.")
    diff_report = analyze(
        xcode_build_output_file_path=args.xcode_build_output_file_path,
        known_build_warnings_file_path=args.known_build_warnings_file_path[0],
        source_root=args.source_root,
    )
    utils.print_info_message("Build Warnings Gate finished running. 🔥")
    return 0 if diff_report.success() else 1


if __name__ == "__main__":
    main()
