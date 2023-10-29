from click import Context, Parameter, ParamType


class ConfigDefinition(ParamType):
    def convert(
        self, value: str, param: Parameter | None, ctx: Context | None
    ) -> tuple[str, str]:
        option, option_value = value.split("=")
        return (option, option_value)
