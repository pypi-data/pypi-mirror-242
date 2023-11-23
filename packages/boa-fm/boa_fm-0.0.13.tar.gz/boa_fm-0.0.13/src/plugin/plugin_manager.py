import importlib


class PluginManager:
    # this dictionary holds the plugins loaded (aka imported)
    # key is plug_point
    loaded_plugin_dict = {}

    loaded_plugin_class_dict = {}

    core_plug_point_configuration = {}

    plugin_initialized = False

    @classmethod
    def override_plugins(cls, override_plugin_dict):
        """
        infrastructure modules are recommended to use this method to override the plugins
        provided by core.
        see plugin/plug_point_config.py for the list of plug points declared by the module.
        :param override_plugin_dict:
        :return:
        """
        for plug_point, override_plugin_dict in override_plugin_dict.items():
            if plug_point in cls.core_plug_point_configuration:
                cls.core_plug_point_configuration[plug_point]["plugin_module"] = override_plugin_dict["plugin_module"]
                cls.core_plug_point_configuration[plug_point]["plugin_class"] = override_plugin_dict["plugin_class"]
            else:
                raise ValueError(f'There is no plug_point with name {plug_point} defined in core')
        cls._import_plugins(cls.core_plug_point_configuration)

    @classmethod
    def get_plugin(cls, persistence_interface_module_name):
        module = cls.loaded_plugin_dict.get(persistence_interface_module_name)
        if module is None:
            if cls.plugin_initialized is False:
                msg = 'PluginManager has not been initialized. ' \
                      'Did you forget to call PluginManager.setup_plugins?' \
                      'Or was there an error calling it?'
            else:
                msg = f'there is no module for {persistence_interface_module_name=}. ' \
                      f'Have you defined the right name for the plugin? '
            print(msg)
            raise BaseException(msg)

        # return module.get_implementation()
        return cls.loaded_plugin_class_dict.get(persistence_interface_module_name)

    @classmethod
    def setup_core_plugins(cls, module_plug_point_configuration_dict):
        """
        this method is invoked only by core modules.
        infrastructure module are recommended to use override_plugins method.
        :return:
        """
        # for now just update i.e. the new plug point will override whatever is
        # already setup.
        # it will be nice to detect one core module overriding another core module
        # because that should never happen - and it is good to catch that.
        cls.core_plug_point_configuration.update(module_plug_point_configuration_dict)
        cls._import_plugins(cls.core_plug_point_configuration)

    @classmethod
    def _import_plugins(cls, plug_point_configuration):
        """
        this method is invoked only by core modules.
        infrastructure module are recommended to use override_plugins method.
        :param plug_point_configuration:
        :return:
        """
        # this method imports plugin modules and associates the module to the
        # plug point
        for plug_point, plug_point_dict in plug_point_configuration.items():
            if "plugin_module" in plug_point_dict:
                # TODO if importing an already imported identical plugin is an error then gracefully skip it.

                print(
                    f'setting up {plug_point=}. we expect a python module of with name {plug_point_dict["plugin_module"]}')
                module = importlib.import_module(plug_point_dict["plugin_module"])
                cls.loaded_plugin_dict[plug_point] = module

                # we want a plugin to be instantiated only once.
                # we could have implemented singleton. but that requires every plugin class to handle that
                # behavior of singleton.
                # there are patterns for it (https://python-patterns.guide/gang-of-four/singleton/)
                # to keep this simple, plugin manager is making sure the plugin class is instantiated exactly once
                class_ = getattr(module, plug_point_dict["plugin_class"])
                plugin_instance = class_()
                cls.loaded_plugin_class_dict[plug_point] = plugin_instance

                # ok, finally mark the plugin is instantiated
                cls.plugin_initialized = True
            else:
                raise ValueError(f'plugin is not defined for {plug_point=}')
