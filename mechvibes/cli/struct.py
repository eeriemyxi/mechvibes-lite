from click import ParamType, Context, Parameter


class ConfigDefinition(ParamType):
    def convert(self, value: str, param: Parameter | None, ctx: Context | None):
        option, option_value = value.split("=")
        return (option, option_value)
