import os
import subprocess
import sys

import toml


def build(setup_kwargs):

    if sys.platform == "linux":

        plat = os.environ.get("PLAT", "")
        python_version = f"{sys.version_info.major}{sys.version_info.minor}"
        build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"build_{python_version}_{plat}")
        cmake_args = ["-DPYTHON_EXECUTABLE=" + sys.executable]
        if not os.path.exists(build_path):
            os.makedirs(build_path)

        subprocess.check_call(["cmake", ".."] + cmake_args, cwd=build_path)
        subprocess.check_call(["cmake", "--build", "."], cwd=build_path)

    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/cacheline/__init__.py")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyproject.toml")) as stream:
        data = toml.load(stream)
        version = data["tool"]["poetry"]["version"]

    with open(script, "a+") as f:
        git_hash = ""

        if os.environ.get("GIT_HASH", ""):
            git_hash = os.environ["GIT_HASH"]
        else:
            git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()

        f.write(f"\n__version__ = '{version}+{git_hash}'\n")


if __name__ == "__main__":
    build({})
