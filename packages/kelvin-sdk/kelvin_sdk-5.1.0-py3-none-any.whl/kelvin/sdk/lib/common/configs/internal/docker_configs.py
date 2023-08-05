"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""


class DockerConfigs:
    docker_client_timeout: int = 120
    docker_dependency: str = "docker"
    latest_docker_image_version: str = "latest"
    # defaults
    default_ksdk_network: str = "ksdk"
    default_ksdk_network_driver: str = "bridge"
    # base construction variables
    ksdk_base_identification_label: dict = {"source": "ksdk"}
    ksdk_base_identification_filters: dict = {"label": "source=ksdk"}
    ksdk_app_identification_label: dict = {"source": "ksdk", "name": ""}
    # app storage configs
    app_container_app_dir_path: str = "/opt/kelvin/app"
    app_bundle_dir_path: str = "/opt/kelvin/bundle"
    app_datamodel_dir_path: str = "/opt/kelvin/datamodel"
    app_container_shared_dir_path: str = "/opt/kelvin/app/shared"
    app_container_shared_dir_bind: str = "{shared_dir_path}:/opt/kelvin/app/shared:Z"
    default_dockerfile_content_with_entrypoint = "FROM {base_image}\nENTRYPOINT {clean_entrypoint}"
    default_dockerfile_content_base = "FROM {base_image}"
    # default app dir
    app_container_app_dir: str = "app"
    layer_base_description: str = "[Layer: {layer_id}] [Pending..]"
    layer_download_success_description: str = "[Layer: {layer_id}] - [{status}] {progress}"
    progress_bar_format: str = " [elapsed: {elapsed}] - {desc} {bar} "
