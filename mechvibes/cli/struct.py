from click import ParamType, Context, Parameter


class ConfigDefinition(ParamType):
    def convert(self, value: str, param: Parameter | None, ctx: Context | None):
        return [x.strip() for x in value.split("=")]
