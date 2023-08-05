# Data loading methods
import json
from typing import Any, List, Mapping, Optional, Sequence, Set

from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.models.ksdk_workload_deployment import WorkloadTemplateData
from kelvin.sdk.lib.common.models.types import WorkloadFileType
from kelvin.sdk.lib.common.utils.general_utils import flatten, guess_delimiter, inflate

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore


def load_workload_data(
    file: KPath, file_type: WorkloadFileType, field_map: Optional[Mapping[str, Any]] = None
) -> Sequence[Mapping[str, Any]]:
    data: Sequence = []
    if file_type == WorkloadFileType.CSV:
        data = _load_csv_workload_data(file, field_map=field_map)
    elif file_type in {WorkloadFileType.YAML, WorkloadFileType.JSON}:
        try:
            data = _load_yaml_workload_data(file)
        except Exception as e:
            raise ValueError(f"Unable to read workload data: {e}")

    if not data:
        raise ValueError("No workloads found.")

    return data


def _load_csv_workload_data(file: KPath, field_map: Optional[Mapping[str, Any]] = None) -> Sequence[Mapping[str, Any]]:
    """
    Load workload data from CSV.

    :param file: CSV data file.
    :param field_map: Optional mapping of field names.

    :return: sequence of mapping entries corresponding to individual deployments.
    """
    import csv

    if field_map is None:
        field_map = {}

    with file.open("rt") as f:
        header = f.readline().rstrip("\n")
        delimiter = guess_delimiter(header)
        fieldnames = [field_map.get(x, x) for x in header.split(delimiter)]

        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=delimiter)

        return [inflate(x) for x in reader]


def _load_yaml_workload_data(file: KPath) -> Sequence[Mapping[str, Any]]:
    """
    Load workload data from YAML/JSON.

    :param file: YAML/JSON data file.

    :return: sequence of mapping entries corresponding to individual deployments.
    """

    import yaml

    with file.open("rt") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, List):
        raise ValueError("Workload data must be a list")

    bad = [(i, x) for i, x in enumerate(data) if not isinstance(x, Mapping)]
    if bad:
        bad_entries = "\n".join(f"  - {i + 1}: {type(x).__name__}" for i, x in bad)
        raise ValueError(f"All entries in workload data must be mappings:\n{bad_entries}")

    return data


# Persistence methods
def save_workload_data(
    file: KPath, filename: str, file_type: WorkloadFileType, output_filename: Optional[str], results: Sequence[Mapping]
) -> bool:
    if output_filename is None:
        head, tail = filename.rsplit(".", 1)
        output_filename = f"{head}_result.{tail}"

    output_file = KPath(output_filename).expanduser().resolve()
    if file_type == WorkloadFileType.CSV:
        with file.open("rt") as f:
            delimiter = guess_delimiter(f.readline().rstrip("\n"))
        return _save_csv_workload_data(output_file, results, delimiter=delimiter)
    elif file_type in {WorkloadFileType.YAML, WorkloadFileType.JSON}:
        return _save_yaml_workload_data(output_file, results)
    return False


def _save_csv_workload_data(file: KPath, data: Sequence[Mapping[str, Any]], delimiter: str = ",") -> bool:
    """
    Save workload data to CSV.

    :param file: CSV data file.
    :param data: Workload data.
    :param delimiter: Optional delimiter.

    :return: a boolean indicating the csv data was successfully saved.
    """

    import csv

    if not data:
        return False

    flattened_data: List[Mapping[str, Any]] = []
    fields: Set[str] = {*()}

    for x in data:
        v = dict(flatten(x))
        flattened_data += [v]
        fields |= {*v}

    fieldnames = [*WorkloadTemplateData.__fields__]
    fieldnames += sorted(fields - {*fieldnames})

    with file.open("wt") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(flattened_data)

    return True


def _save_yaml_workload_data(file: KPath, data: Sequence[Mapping[str, Any]]) -> bool:
    """
    Save workload data to YAML/JSON.

    :param file: YAML/JSON data file.
    :param data: Workload data.

    :return: a boolean indicating the yaml data was successfully saved.
    """

    import yaml

    if not data:
        return False

    with file.open("wt") as f:
        if file.suffix == ".json":
            json.dump(data, f)
        else:
            yaml.dump(data, f)

    return True
