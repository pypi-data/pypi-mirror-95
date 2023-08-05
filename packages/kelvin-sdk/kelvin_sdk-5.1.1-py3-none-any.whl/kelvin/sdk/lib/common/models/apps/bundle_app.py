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
from typing import Any, Dict, List, Optional

from pydantic import Field

from kelvin.sdk.lib.common.models.apps.common import DockerImageName, Version
from kelvin.sdk.lib.common.models.apps.kelvin_app import Core, Images, KelvinAppType
from kelvin.sdk.lib.common.models.generic import KSDKModel


class Pipeline(KSDKModel):
    name: DockerImageName = Field(..., description="Application name.", title="Application Name")
    version: Version = Field(..., description="Application version.", title="Application Version")
    kelvin: Optional[KelvinAppType] = None
    configuration: Optional[Dict[str, Any]] = Field(
        None, description="Extra configuration.", title="Extra Configuration"
    )


class BundleAppType(KSDKModel):
    core: Optional[Core] = None
    images: Optional[Images] = None
    pipelines: List[Pipeline] = []
