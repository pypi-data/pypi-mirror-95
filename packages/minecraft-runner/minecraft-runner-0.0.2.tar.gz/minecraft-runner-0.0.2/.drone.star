def main(ctx):
    envlist = {
        "lint": True,
        "security": True,
        "clean": ctx.build.event != "pull_request",
        "test": ctx.build.event != "pull_request",
        "report": (ctx.build.event != "pull_request" and
                   ctx.build.branch == "main"),
    }

    tox_steps = [tox(env) for env, case in envlist.items() if case]
    if ctx.build.event == "tag":
        tox_steps.append(release)

    return pipeline(tox_steps)


def pipeline(steps):
    return {
        "kind": "pipeline",
        "type": "exec",
        "name": "minecraft-runner",
        "steps": setup + steps + check_release
    }


def tox(env):
    return {
        "name": env,
        "commands": ["$$HOME/.local/bin/tox -e %s" % env]
    }


release = {
    "name": "release",
    "commands": [
        "$$HOME/.local/bin/tox -e build,release"
    ],
    "environment": {
        "TWINE_PASSWORD": {
            "from_secret": "TWINE_PASSWORD"
        }
    }
}


setup = [{
    "name": "setup prereqs",
    "commands": [
        "pip install --upgrade --user pip tox",
        "git fetch" # without tags setuptools_scm will fail
    ]
}]


check_release = [{
    "name": "check-release",
    "commands": [
        "echo Latest release:",
        "curl -sL https://pypi.org/pypi/minecraft-runner/json | jq -r '.info.release_url'"
    ]
}]
