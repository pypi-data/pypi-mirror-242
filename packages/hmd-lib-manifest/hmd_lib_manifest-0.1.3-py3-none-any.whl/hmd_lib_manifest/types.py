import json
from typing import Any, Dict
import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

MANIFEST_EXTENSION_ENTRY_POINT = "hmd_lib_manifest.manifest"


class ManifestConfigMap(dict):
    """Wrapper class representing a dictionary configuration property in a Manifest."""

    def __init__(self, *args, **kw):
        super(ManifestConfigMap, self).__init__(*args, **kw)

    def __getattr__(self, __name: str):
        prop = self.get(__name)

        if isinstance(prop, dict):
            return ManifestConfigMap(prop)

        return prop

    def __getitem__(self, __key: Any) -> Any:
        prop = self.get(__key)

        if isinstance(prop, dict):
            return ManifestConfigMap(prop)

        return prop

    def __setitem__(self, key, value):
        super(ManifestConfigMap, self).__setitem__(key, value)

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(__name, __value)

    @classmethod
    def from_config(cls, config):
        """Allows creating from existing config object. Used primarily in extension subclasses to provide additional functionality.

        Args:
            config (Union[Dict, ManifestConfigMap]): existing configuration map or dictionary

        Returns:
            ManifestConfigMap: ManifestConfigMap or subclass instance
        """
        return cls(config)

    def merge(self, config):
        """Merges two configurations together.

        Lists and Dictionaries will be merged together, not overwritten.
        Raw values in ``config`` will overwrite values in this ManifestConfigMap instance with the same key.
        Any nested property with a key of ``commands`` will be deduped as best as possible.
        For example, given existing build commands of ``[["python"], ["docker"]]`` merging with ``[["python"], ["cdktf"]]`` will result in ``[["python"],["docker"], ["cdktf"]]``.
        However, the dedup only takes into account single item tool command lists, i.e. ["python"]. If extra arguments are given, then it is not considered for deduplication.
        For example, ``[["python"], ["docker"]]`` merging with ``[["python", "release", {"arg": "value"}]]`` will result in  ``[["python"], ["docker"],["python", "release", {"arg": "value"}]``

        Args:
            config (ManifestConfigMap): the ManifestConfigMap to merge into this one

        Raises:
            Exception: Invalid merge operation
            Exception: Invalid merge operation

        Returns:
            ManifestConfigMap: merged ManifestConfigMap
        """
        for k, v in config.items():
            if isinstance(v, dict):
                orig_value = self.get(k, ManifestConfigMap({}))
                if isinstance(orig_value, dict):
                    orig_value = ManifestConfigMap(orig_value)
                if not isinstance(orig_value, ManifestConfigMap):
                    raise Exception(f"Invalid merge operation for key: {k}")
                self[k] = orig_value.merge(v)
            elif isinstance(v, list):
                orig_value = self.get(k, [])
                if not isinstance(orig_value, list):
                    raise Exception(f"Invalid merge operation for key: {k}")
                # Build and Deploy commands are handled as special case and deduped
                if k == "commands":
                    tools = set()
                    commands = []

                    for t in [*orig_value, *v]:
                        if len(t) == 1:
                            if t[0] not in tools:
                                commands.append(t)
                            tools.add(t[0])
                        else:
                            commands.append(t)
                    self[k] = commands
                else:
                    self[k] = [*orig_value, *v]
            else:
                self[k] = v

        return self


class Manifest:
    """Python class representation of a NeuronSphere Project Manifest"""

    def __init__(self, data: Dict) -> None:
        self.__config = ManifestConfigMap(data)

        self.__extensions = {}

        for entrypoint in entry_points(group=MANIFEST_EXTENSION_ENTRY_POINT):
            self.__extensions[entrypoint.name] = entrypoint.load()

    def __get_config(self, __name: str) -> Any:
        if __name in self.__extensions:
            klass = self.__extensions[__name]

            if not issubclass(klass, ManifestConfigMap):
                raise Exception(f"Invalid manifest extension class: {klass.__name__}")

            return klass.from_config(self.__config[__name])
        return self.__config[__name]

    def __getattr__(self, __name: str) -> Any:
        return self.__get_config(__name)

    def __getitem__(self, __name: str) -> Any:
        return self.__get_config(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        # Handling special attributes to avoid infinite recursion
        if __name.endswith("__config") or __name.endswith("__extensions"):
            super().__setattr__(__name, __value)
        else:
            self.__config[__name] = (
                __value if not isinstance(__value, dict) else ManifestConfigMap(__value)
            )

    def __setitem__(self, __key: str, __value: str) -> None:
        self.__setattr__(__key, __value)

    def add_config(self, name: str, value: Any) -> None:
        """Adds new configuration property to Manifest

        Args:
            name (str): configuration property key
            value (Any): configuration property value
        """
        if isinstance(value, dict):
            value = ManifestConfigMap(value)
        self.__config[name] = value

    def merge(self, config):
        """Merge two Manifests together

        Args:
            config (Manifest): Manifest to merge into this one
        """
        self.__config = self.__config.merge(config)

    def items(self):
        """Returns iterable list of configuration properties

        Returns:
            dict_items: Manifest configuration properties
        """
        return self.__config.items()

    def to_json(self, fd=None) -> Dict:
        """Prints JSON representation of Manifest to file or string

        Args:
            fd (SupportsWrite[str], optional): file descriptor to write JSON to, opened with ``open``. Defaults to None.

        Returns:
            Dict: JSON representation of Manifest
        """
        if fd is None:
            return json.dumps(self.__config)
        return json.dump(self.__config, fd, indent=2)
