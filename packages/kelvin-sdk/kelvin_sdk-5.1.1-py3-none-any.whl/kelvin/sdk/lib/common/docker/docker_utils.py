import json
from time import sleep
from typing import Any, Dict, Generator, List

from kelvin.sdk.lib.common.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.common.exceptions import DependencyNotRunning, KDockerException
from kelvin.sdk.lib.common.models.ksdk_docker import DockerBuildEntry, DockerProgressEntry
from kelvin.sdk.lib.common.utils.display_utils import error_colored_message
from kelvin.sdk.lib.common.utils.general_utils import check_if_dependency_is_installed


def display_docker_progress(stream: Generator) -> bool:
    """
    When provided with a docker stream generator, display the overall progress of all layer involved.

    :param stream: a docker stream generator that outputs every entry of the process

    :return: return a bool indicating all progress info has been successfully displayed.
    """
    from tqdm import tqdm

    # 1 - a dictionary to keep track of all layers
    all_layers: Dict[str, tqdm] = {}
    layer_index = 0
    for log_entry in stream:
        entries = process_docker_image_progress_entry(entry=log_entry)
        for item in entries:
            layer_id = item.id
            layer_status = item.status
            layer_progress = item.progress or ""
            if layer_id:
                if layer_id not in all_layers.keys():
                    layer_base_description = DockerConfigs.layer_base_description.format(layer_id=layer_id)
                    all_layers[layer_id] = tqdm(
                        total=100,
                        desc=layer_base_description,
                        position=layer_index,
                        bar_format=DockerConfigs.progress_bar_format,
                        leave=True,
                        dynamic_ncols=True,
                    )
                    layer_index += 1
                else:
                    tracker = all_layers.get(layer_id, None)
                    if tracker:
                        params = {"layer_id": layer_id, "status": layer_status, "progress": layer_progress}
                        description = DockerConfigs.layer_download_success_description.format_map(params)
                        tracker.set_description_str(description)
                        tracker.refresh()
                        sleep(0.01)

    for tracker in all_layers.values():
        tracker.close()
        tracker.clear()

    return True


def process_dockerfile_build_entry(entry: dict) -> str:
    """
    Print the dockerfile build entry from its rightful dict.

    :param entry: a dictionary containing the dockerfile build entry.

    :return: a string containing the result of the processed entry object.

    """
    try:
        dockerfile_build_entry = DockerBuildEntry(**entry).stream_content or ""
    except Exception:
        dockerfile_build_entry = ""

    return dockerfile_build_entry


def process_docker_image_progress_entry(entry: bytes) -> List[DockerProgressEntry]:
    """
    Print the docker image push progress entry from its rightful dict.

    :param entry: a dictionary containing the docker image progress entry.

    :return: a string containing the result of the processed entry object.

    """
    try:
        split_entry = str(entry, "utf-8").split("\n")
        clean_entries = [json.loads(entry) for entry in split_entry if entry]
        return [DockerProgressEntry(**loaded_entry) for loaded_entry in clean_entries]
    except Exception:
        dockerfile_progress_entry: List[DockerProgressEntry] = []

    return dockerfile_progress_entry


def process_docker_entry(entry: bytes) -> str:
    """
    Print the datamodel compilation entry from its raw string.

    :param entry: a byte string containing the datamodel compilation entry.

    :return: a string containing the result of the processed entry object.

    """
    try:
        dockerfile_build_entry = entry.decode("utf-8").replace("\n", "")
    except Exception:
        dockerfile_build_entry = ""

    return dockerfile_build_entry


def ensure_docker_is_running(function: Any) -> Any:
    def wrapper(self: Any, *args, **kwargs) -> Any:  # type: ignore
        docker_dependency = DockerConfigs.docker_dependency
        try:
            check_if_dependency_is_installed(dependency=docker_dependency)
            docker_is_running = self._docker_client.ping()
        except Exception as exc:
            docker_is_running = exc is None

        if not docker_is_running:
            raise DependencyNotRunning(message=docker_dependency)

        return function(self=self, *args, **kwargs)

    return wrapper


def assess_docker_connection_exception(exc: Exception) -> Exception:
    """
    Parse the provided exception and return a 'pretty' docker exception.

    :param exc: the exception to verify.

    :return: an exception with the adequate result.
    """

    docker_api_not_available: str = f"""\n
        Error accessing the local Docker instance.
        Please ensure Docker is running and its service is accessible.\n
        More information:
            > Using a system installation - https://docs.docker.com/config/daemon/
            > Using Docker Desktop - https://docs.docker.com/docker-for-windows/install/#start-docker-desktop

        Detailed error:
            {str(exc)}

    """
    return KDockerException(docker_api_not_available)


def handle_error_stack_trace(complete_stack: List[DockerBuildEntry]) -> None:
    """
    When provided the complete build stack, yield a KDockerException with all the logging 'juice' combined.

    Returns
    -------
    complete_stack: List[DockerBuildEntry]
        the entire build stack trace

    """
    complete_stack = complete_stack[-7:] if len(complete_stack) > 7 else complete_stack
    complete_stack_message: str = ""
    for entry in complete_stack:
        entry_content = entry.log_content
        if entry_content:
            complete_stack_message += f"\n{error_colored_message(entry_content)}"

    raise KDockerException(f"\n{complete_stack_message}")
