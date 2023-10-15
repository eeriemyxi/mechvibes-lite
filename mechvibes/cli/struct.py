from click import ParamType


class ConfigDefinition(ParamType):
    def convert(self, value, param, ctx):
        return [x.strip() for x in value.split("=")]
