import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-home-assistant-skill",
    "version": "0.0.0",
    "description": "cdk-home-assistant-skill",
    "license": "Apache-2.0",
    "url": "https://github.com/t0bst4r/cdk-home-assistant-skill.git",
    "long_description_content_type": "text/markdown",
    "author": "t0bst4r<82281152+t0bst4r@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/t0bst4r/cdk-home-assistant-skill.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_home_assistant_skill",
        "cdk_home_assistant_skill._jsii"
    ],
    "package_data": {
        "cdk_home_assistant_skill._jsii": [
            "cdk-home-assistant-skill@0.0.0.jsii.tgz"
        ],
        "cdk_home_assistant_skill": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.88.0, <3.0.0",
        "cdk-skill-management>=1.0.28, <2.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.92.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
