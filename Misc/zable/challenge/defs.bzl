def _get_env_impl(ctx):
    return [
        platform_common.TemplateVariableInfo({
            "NAME": ctx.configuration.default_shell_env.get("NAME", "hacker"),
        }),
    ]

get_env = rule(
    implementation = _get_env_impl,
    attrs = {},
)