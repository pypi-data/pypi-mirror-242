from guerrilla.device.router import Commands

class ShowMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._add_show_methods()

    @classmethod
    def _add_show_methods(cls):
        def create_show_method(command):
            """Return a dynamically created method."""

            def method(self):
                self._back_to_main()
                return self.run(command)

            return method

        # def process_enum(enum_obj, prefix=""):
        #     for cmd in enum_obj:
        #         method_suffix = cmd.name.lower()
        #         # If nested Enum, process it first
        #         if hasattr(cmd.value, "__members__"):
        #             new_prefix = f"{method_suffix}_"
        #             process_enum(cmd.value, new_prefix)
        #         elif isinstance(cmd.value, str):  # Direct command
        #             method_name = f"show_{prefix}{method_suffix}"
        #             setattr(cls, method_name, create_show_method(cmd.value))
        
        def process_enum(enum_obj, prefix=""):
            for cmd in enum_obj:
                method_suffix = cmd.name.lower()
                # If nested Enum, process it first
                if hasattr(cmd.value, "__members__"):
                    # Append current suffix to prefix, ensuring to pass the full path
                    new_prefix = f"{prefix}{method_suffix}_"
                    process_enum(cmd.value, new_prefix)
                elif isinstance(cmd.value, str):  # Direct command
                    # Use the current prefix and suffix to form the method name
                    method_name = f"show_{prefix}{method_suffix}"
                    setattr(cls, method_name, create_show_method(cmd.value))
        

        process_enum(Commands.SHOW)