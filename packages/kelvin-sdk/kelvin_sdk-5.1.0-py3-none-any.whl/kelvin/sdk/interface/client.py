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

from typing import Sequence

from typeguard import typechecked


@typechecked
def client(args: Sequence[str]) -> None:
    """
    Launch an IPython client with a pre-loaded KelvinClient object.

    """
    from kelvin.sdk.lib.common.auth.auth_manager import launch_ipython_client as _launch_ipython_client

    _launch_ipython_client(args)
