"""
Use `import pdb; pdb.set_trace()` to pause and inspect the runfiles directory
"""

import os
import shutil
import subprocess

from python.runfiles import Runfiles

runfiles = Runfiles.Create()

# http_file location
ZSTD_CLI = runfiles.Rlocation("zstd_cli/file/downloaded")

# http_archive location
YQ_CLI = runfiles.Rlocation("yq_cli/yq_linux_amd64")

# local workspace file location (already in a Bazel package)
sources_txt = runfiles.Rlocation("_main/src/sources.txt")

# local workspace file location (not in a Bazel package)
data_json = runfiles.Rlocation("_main/adhoc/data.json")

# the actual output file name is `libhelpers.so` for the shared `cc_library`
# where `helpers` is the name of the target; the output file name might vary
# depending on the type of the rule
helpers_so = runfiles.Rlocation("_main/src/libhelpers.so")

pairs = [
    ("zstd", ZSTD_CLI),
    ("yq", YQ_CLI),
    ("Data file tracked by Bazel", sources_txt),
    ("Data file not tracked by Bazel", data_json),
    ("Data file produced by Bazel from a build target", helpers_so),
]
for pair in pairs:
    print(pair)

print("Pretty print of JSON with yq:")
_ = subprocess.run(
    args=[YQ_CLI, data_json],
    check=True,
    text=True,
)

print(f"Zstd compression level from env var: {os.getenv('ZSTD_COMPRESSION_LEVEL')}")
_ = subprocess.run(
    args=[
        ZSTD_CLI,
        sources_txt,
        "-o",
        "archive.zst",
        "--force",
    ],
    check=True,
    text=True,
)

# need to copy the archive from `/home/%username%/.cache/bazel/_bazel_%username%/checksum/execroot/_main/bazel-out/k8-fastbuild/bin/tools/archiver.runfiles/_main`
shutil.copyfile(
    "archive.zst",
    f"{os.getenv('BUILD_WORKSPACE_DIRECTORY')}/archive.zst",
)
