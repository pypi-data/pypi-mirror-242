from __future__ import annotations

from collections.abc import Callable
import pathlib
import types

import jinja2

from jinjarope import utils


class LoaderMixin:
    """Loader mixin which allows to OR loaders into a choice loader."""

    ID: str
    loader: jinja2.BaseLoader
    list_templates: Callable
    get_source: Callable

    def __or__(self, other: jinja2.BaseLoader):
        own = self.loaders if isinstance(self, jinja2.ChoiceLoader) else [self]  # type: ignore[list-item]
        others = other.loaders if isinstance(other, jinja2.ChoiceLoader) else [other]
        return ChoiceLoader([*own, *others])

    def __getitem__(self, val: str) -> str:
        return self.get_source(None, val)[0]

    def __contains__(self, path):
        return pathlib.Path(path).as_posix() in self.list_templates()

    def __rtruediv__(self, path):
        return self.prefixed_with(path)

    def prefixed_with(self, prefix: str):
        """Return loader wrapped in a PrefixLoader instance with given prefix.

        Arguments:
            prefix: The prefix to use
        """
        return PrefixLoader({prefix: self})  # type: ignore[dict-item]


class PrefixLoader(LoaderMixin, jinja2.PrefixLoader):
    """A loader for prefixing other loaders."""

    ID = "prefix"

    def __repr__(self):
        return utils.get_repr(self, self.mapping)

    def __eq__(self, other):
        return type(self) == type(other) and self.mapping == other.mapping

    def __hash__(self):
        return hash(tuple(sorted(self.mapping.items())))


class ModuleLoader(LoaderMixin, jinja2.ModuleLoader):
    """This loader loads templates from precompiled templates.

    Templates can be precompiled with :meth:`Environment.compile_templates`.
    """

    ID = "module"

    def __repr__(self):
        return utils.get_repr(self, path=self.module.__path__)

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.package_name == other.package_name
            and self.module == other.module
        )

    def __hash__(self):
        return hash(self.package_name) + hash(self.module)


class FunctionLoader(LoaderMixin, jinja2.FunctionLoader):
    """A loader for loading templates from a function.

    The function takes a template path as parameter and either returns
    a (text, None, uptodate_fn) tuple or just the text as str.
    """

    ID = "function"

    def __repr__(self):
        return utils.get_repr(self, self.load_func)

    def __eq__(self, other):
        return type(self) == type(other) and self.load_func == other.load_func

    def __hash__(self):
        return hash(self.load_func)


class PackageLoader(LoaderMixin, jinja2.PackageLoader):
    """A loader for loading templates from a package."""

    ID = "package"

    def __init__(
        self,
        package: str | types.ModuleType,
        package_path: str | None = None,
        encoding: str = "utf-8",
    ) -> None:
        """Instanciate a PackageLoader.

        Compared to the jinja2 equivalent, this loader also supports
        `ModuleType`s and dotted module paths for the `package` argument.

        Arguments:
            package: The python package to create a loader for
            package_path: If given, use the given path as the root.
            encoding: The encoding to use for loading templates
        """
        if isinstance(package, types.ModuleType):
            package = package.__name__
        parts = package.split(".")
        path = "/".join(parts[1:])
        if package_path:
            path = (pathlib.Path(path) / package_path).as_posix()
        super().__init__(parts[0], path, encoding)

    def __repr__(self):
        return utils.get_repr(
            self,
            package_name=self.package_name,
            package_path=self.package_path,
        )

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.package_name == other.package_name
            and self.package_path == other.package_path
        )

    def __hash__(self):
        return hash(self.package_name) + hash(self.package_path)


class FileSystemLoader(LoaderMixin, jinja2.FileSystemLoader):
    """A loader to load templates from the file system."""

    ID = "filesystem"

    def __repr__(self):
        return utils.get_repr(self, searchpath=self.searchpath)

    def __add__(self, other):
        if isinstance(other, jinja2.FileSystemLoader):
            paths = other.searchpath
        else:
            paths = [other]
        return FileSystemLoader([*self.searchpath, *paths])

    def __eq__(self, other):
        return type(self) == type(other) and self.searchpath == other.searchpath

    def __hash__(self):
        return hash(tuple(self.searchpath))


class ChoiceLoader(LoaderMixin, jinja2.ChoiceLoader):
    """A loader which combines multiple other loaders."""

    ID = "choice"

    def __repr__(self):
        return utils.get_repr(self, loaders=self.loaders, _shorten=False)

    def __eq__(self, other):
        return type(self) == type(other) and self.loaders == other.loaders

    def __hash__(self):
        return hash(tuple(self.loaders))


class DictLoader(LoaderMixin, jinja2.DictLoader):
    """A loader to load static content from a path->template-str mapping."""

    ID = "dict"

    def __repr__(self):
        return utils.get_repr(self, mapping=self.mapping)

    def __add__(self, other):
        if isinstance(other, jinja2.DictLoader):
            mapping = self.mapping | other.mapping
        elif isinstance(other, dict):
            mapping = self.mapping | other
        return DictLoader(mapping)

    def __eq__(self, other):
        return type(self) == type(other) and self.mapping == other.mapping

    def __hash__(self):
        return hash(tuple(sorted(self.mapping.items())))


def from_json(dct_or_list) -> jinja2.BaseLoader | None:
    from jinjarope import fsspecloaders

    if not dct_or_list:
        return None
    loaders = []
    ls = dct_or_list if isinstance(dct_or_list, list) else [dct_or_list]
    for item in ls:
        match item:
            case jinja2.BaseLoader():
                loaders.append(item)
            case str() if "://" in item:
                loaders.append(fsspecloaders.FsSpecFileSystemLoader(item))
            case str():
                loaders.append(FileSystemLoader(item))
            case types.ModuleType():
                loaders.append(PackageLoader(item))
            case dict():
                for kls in jinja2.BaseLoader.__subclasses__():
                    if not issubclass(kls, LoaderMixin):
                        continue
                    dct_copy = item.copy()
                    if dct_copy.pop("type") == kls.ID:  # type: ignore[attr-defined]
                        if kls.ID == "prefix":  # type: ignore[attr-defined]
                            mapping = dct_copy.pop("mapping")
                            mapping = {k: from_json(v) for k, v in mapping.items()}
                            instance = kls(mapping)  # type: ignore[call-arg]
                        else:
                            instance = kls(**dct_copy)

                        loaders.append(instance)
    match len(loaders):
        case 1:
            return loaders[0]
        case 0:
            return None
        case _:
            return ChoiceLoader(loaders)


if __name__ == "__main__":
    from jinjarope import Environment

    env = Environment()
    env.loader = FileSystemLoader("")
    text = env.render_template(".pre-commit-config.yaml")
    print(text)
