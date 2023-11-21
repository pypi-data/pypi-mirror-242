import functools
import inspect
import typing
import networkx as nx
import warnings
from collections import defaultdict
from typing import Optional, Union, Callable, Iterable, Generator, Any


class Registry:
    def __init__(self):
        self.functions = {}
        self.wraps = defaultdict(list)
        self.loaded_plugins = set()
        self.cached_functions = {}

    def register_plugin(self, name):
        if name in self.loaded_plugins:
            raise ValueError(f"Plugin {name} is already registered.")
        self.loaded_plugins.add(name)
        return Plugin(name, self)

    def register_function(self, name, function, private_params, meta_wrapper):
        self.functions[name] = function
        return lambda *args, **kwargs: self._resolve_function(name, private_params, meta_wrapper)(*args, **kwargs)

    def unregister_function(self, name):
        del self.functions[name]
        if name in self.cached_functions:
            del self.cached_functions[name]

    def register_wrap(self, function_name, wrap, extension_name, after):
        self.wraps[function_name].append((wrap, extension_name, after))
        if function_name in self.cached_functions:
            del self.cached_functions[function_name]  # Invalidate cache

    def _resolve_function(self, function_name, private_params, meta_wrapper):
        if function_name not in self.functions:
            raise ValueError(f"Function {function_name} is not registered.")

        # Use cached function if available
        if function_name in self.cached_functions:
            function = self.cached_functions[function_name]
        else:
            # Resolve wrap order and apply wraps
            def private_function(private_kwargs):
                return functools.partial(self.functions[function_name], **private_kwargs)

            def private_meta_wrapper(private_kwargs, meta_wrapper=meta_wrapper):
                return functools.partial(meta_wrapper, **private_kwargs)

            wraps = self._resolve_wrap_order(function_name)
            for wrap in wraps:
                # Nest private functions
                def private_function(private_kwargs, wrap=wrap, private_function=private_function):
                    resolved_wrap = functools.partial(wrap, original_function=private_function(private_kwargs))
                    if meta_wrapper is None:
                        return resolved_wrap
                    return functools.partial(private_meta_wrapper(private_kwargs), original_function=resolved_wrap)

            def function(*args, **kwargs):
                private_kwargs = {k: kwargs[k] for k in private_params}
                kwargs = {k: v for k, v in kwargs.items() if k not in private_kwargs}
                return private_function(private_kwargs)(*args, **kwargs)

            self.cached_functions[function_name] = function  # Cache the wrapped function

        return function

    def _resolve_wrap_order(self, function_name):
        wraps = self.wraps.get(function_name, [])
        g = nx.DiGraph()

        # Add nodes
        for _, ext_name, _ in wraps:
            g.add_node(ext_name)

        # Add edges based on 'after' dependencies
        for _, ext_name, after in wraps:
            if after:
                for dep in after:
                    if dep in self.loaded_plugins:
                        g.add_edge(ext_name, dep)

        # Attempt to perform topological sort
        try:
            sorted_ext_names = list(nx.topological_sort(g))
        except nx.NetworkXUnfeasible:
            # Detect and break circular dependencies
            cycle = nx.find_cycle(g, orientation='original')
            g.remove_edge(*cycle[0][:2])  # Correctly handle the edge tuple
            cycle_plugins = " -> ".join([node for node, _, _ in cycle])
            warnings.warn(
                f"Circular dependency detected in function '{function_name}' between plugins: {cycle_plugins}. "
                f"To resolve the issue, the wrap from plugin {cycle[0][1]} is applied before the wrap from plugin {cycle[0][0]}.",
                UserWarning)
            sorted_ext_names = list(nx.topological_sort(g))

        # Filter wraps based on the sorted extension names, ensuring each wrap is applied only once
        sorted_wraps = []
        seen = set()
        for ext_name in sorted_ext_names:
            for wrap, wrap_ext_name, _ in wraps:
                if wrap_ext_name == ext_name and wrap not in seen:
                    sorted_wraps.append(wrap)
                    seen.add(wrap)

        return sorted_wraps


Input = typing.TypeVar("Input")
Output = typing.TypeVar("Output")
PluginWrapperFunc = Callable[[Input, "PluginWrapperFuncOnly"], Output]
PluginWrapper = Union[PluginWrapperFunc, Generator[Input, Output, Output]]
PluginFunction = Callable[[Input, ...], Output]


class Plugin:
    def __init__(self, name: str, registry: Registry):
        self.name = name
        self.registry = registry

    def function(
        self,
        func: Optional[PluginFunction] = None,
        *,
        name: Optional[str] = None,
        private_params: Optional[Iterable[str]] = None,
        meta_wrapper: Optional[PluginWrapper] = None,
    ):
        if func is None:
            return lambda f: self._function_with_args(f, name=name, private_params=private_params, meta_wrapper=meta_wrapper)
        return self._function_with_args(func, name=name, private_params=private_params, meta_wrapper=meta_wrapper)

    def _function_with_args(self, func, *, name, private_params, meta_wrapper):
        if name is None:
            name = func.__name__

        if private_params is None:
            private_params = set()

        return self.registry.register_function(name, func, private_params, self._wrap_generator_to_function(meta_wrapper))

    def remove_function(self, func: Union[str, Callable]):
        if not isinstance(func, str):
            func = func.__name__
        self.registry.unregister_function(func)

    def wrapper(self, func: Optional[Callable] = None, *, name: Optional[str] = None, after: Optional[Union[str, Iterable[str]]] = None):
        if func is None:
            return lambda f: self._wrapper_with_args(f, name=name, after=after)
        return self._wrapper_with_args(func, name=name, after=after)

    def _wrapper_with_args(self, func, *, name, after):
        if name is None:
            name = func.__name__

        if after is None:
            after = set()
        elif isinstance(after, str):
            after = {after}

        self.registry.register_wrap(name, self._wrap_generator_to_function(func), self.name, after)
        return func

    def _wrap_generator_to_function(self, wrapper):
        if not inspect.isgeneratorfunction(wrapper):
            return wrapper

        def function_wrapper(*args, original_function, **kwargs):
            gen = wrapper(*args, **kwargs)
            try:
                value = next(gen)
                while True:
                    res = original_function(value)
                    value = gen.send(res)
            except StopIteration as e:
                return e.value

        return function_wrapper

    def create_component_list(
        self,
        *,
        name: str,
        private_params: Optional[Iterable[str]] = None,
        meta_wrapper: Optional[PluginWrapper] = None,
    ):
        return self.function(lambda: [], name=name, private_params=private_params, meta_wrapper=meta_wrapper)

    def append_component(self, component: Optional[Any] = None, *, name: Optional[str] = None, after: Optional[Union[str, Iterable[str]]] = None):
        if component is None:
            return lambda c: self._append_component_with_args(c, name=name, after=after)
        return self._append_component_with_args(component, name=name, after=after)

    def _append_component_with_args(self, component, *, name, after):
        if name is None:
            name = component.__name__

        self.wrapper(lambda original_function: (*original_function(), component), name=name, after=after)
        return component
