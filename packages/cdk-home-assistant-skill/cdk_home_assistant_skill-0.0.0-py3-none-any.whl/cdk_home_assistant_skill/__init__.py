'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *


class HomeAssistantSkill(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-home-assistant-skill.HomeAssistantSkill",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])


__all__ = [
    "HomeAssistantSkill",
]

publication.publish()
