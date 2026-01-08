## Runfiles

[Bazel runfiles](https://bazel.build/extending/rules#runfiles) are a set of files used by a target at runtime (as opposed to build time). 
During the execution phase, Bazel creates a directory tree containing symlinks pointing to the runfiles. 
This stages the environment for the binary so it can access the runfiles during runtime.

How one can access runfiles from a Python script is documented at 
[bazel-runfiles library](https://github.com/bazel-contrib/rules_python/tree/main/python/runfiles),
however, declaring resources that are going to be accessed in a Python script can take some time to figure out
due to potentially confusing syntax.

This repository contains a working example of a Python script that is run with `bazel run` that accesses:

* [http_file](https://bazel.build/rules/lib/repo/http#http_file)
* [http_archive](https://bazel.build/rules/lib/repo/http#http_archive)
* a file that is part of a Bazel package (labeled `//path/from/root:filename.ext`)
* a standalone file that is **not** part of a Bazel package (a directory without `BUILD` file) (labeled `//:dirname/filename.ext`)

## `bazel run`

```shell
$ bazel run //tools:archiver
INFO: Analyzed target //tools:archiver (81 packages loaded, 3594 targets configured).
INFO: Found 1 target...
Target //tools:archiver up-to-date:
  bazel-bin/tools/archiver
INFO: Elapsed time: 0.956s, Critical Path: 0.15s
INFO: 5 processes: 5 internal.
INFO: Build completed successfully, 5 total actions
INFO: Running command line: bazel-bin/tools/archiver
('zstd', '/home/username/.cache/bazel/_bazel_username/254dc3e965daf05650054d94e27038ea/external/+_repo_rules2+zstd_cli/file/downloaded')
('yq', '/home/username/.cache/bazel/_bazel_username/254dc3e965daf05650054d94e27038ea/external/+_repo_rules+yq_cli/yq_linux_amd64')
('Data file tracked by Bazel', '/home/username/code/projects/bazel-runfiles-demo/src/sources.txt')
('Data file not tracked by Bazel', '/home/username/code/projects/bazel-runfiles-demo/adhoc/data.json')
Pretty print of JSON with yq:
{
  "a": "A",
  "b": "B"
}
Zstd compression level from env var: 10
/home/username/code/projects/bazel-runfiles-demo/src/sources.txt :136.11%   (    36 B =>     49 B, archive.zst)
```