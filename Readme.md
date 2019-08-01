# EDK II Continuous Integration Project

* [Overview](#overview)
* [Maintainers](#maintainers)

# Overview

The majority of the content in the EDK II open source project uses a
[BSD-2-Clause Plus Patent License](License.txt).

The master branch of the edk2-ci repository contains the template for the files
required in a patchset branch that initiates a Continuous Integration (CI)
process.  Git repositories and Git branches may be used from TianoCore or public
forks of TianoCore.  The branch naming convention is:

    patchset/<github id>/BZ_<bz id>/V<patch set version>/<title>

For example:

    patchset/mdkinney/BZ_1234/V1/Add_My_New_Feature

The required files in a `patchset` branch are:

    Readme.txt            # Same as edk2-ci/master
    License.txt           # Same as edk2-ci/master
    Maintainers.txt       # Same as edk2-ci/master
    AzurePipelines        # Same as edk2-ci/master
    azure_pipelines.yml   # Customize as needed

There is no FW code in a patchset branch.  Instead, a patchset branch provides
an inventory of git repositories/branches to use for a CI build and the set of
build commands to run against those git repositories/branches.  When a branch
that follows the branch naming convention is pushed to `edk2-ci`, it starts a
CI build using the inventory of git repositories/branches and build commands.
A developer typically prepares a patchset in branch(s) in their personal fork of
the EDK II repositories.  The `azure_pipelines.yml` file in the patchset branch
is updated to point to these branch(s) in their personal fork of the EDK II
repositories.

Each CI environment must be initialized to be compatible with an EDK II build.
The following CI environments are supported:

* Azure Pipelines - azure_pipelines.yml

If the default environment provided is not compatible with the build commands,
then the YML file can be customized in the patchset branch.

Any contributions to this branch should be submitted via email to the
EDK II mailing list with a subject prefix of `[edk2-ci]`. See
[Laszlo's excellent guide](https://github.com/tianocore/tianocore.github.io/wiki/Laszlo's-unkempt-git-guide-for-edk2-contributors-and-maintainers)
for details on how to do this successfully.

## Azure Pipelines Configuration

When using Azure Pipelines, only the `azure_pipelines.yml` file should be
customized.  There are template files in the AzurePipelines directory that
contain the set of Host OS/Compiler/CPU Arch combinations that are supported,
the prerequisites that need to be installed for each Host OS, and the steps
required to download the EDK II sources and run a sequence of EDK II build
commands that produce log/report files and potentially FD/FV images.

The `azure_pipelines.yml` file provides a simple way to specify the EDK II
sources required to perform a build along with a sequence of packages/platforms
to build.  I also includes the ability to filter out some Host OS/Compiler/CPU
Arch combinations if a developer is working on a bug/feature for specific build
combination.

The following is the complete set of parameters to the Azure Pipelines template
in the file `AzurePipelines/DoEdk2Build.yml` along with the default values for
each parameter.

```
parameters:
  git_commands: |
    git clone --depth 1 https://github.com/tianocore/edk2.git
    cd edk2
    git submodule update --init
  x11_prerequisite: 'false'
  edk2_path: 'edk2'
  build_target_list:
  - 'DEBUG'
  packages_path_list:
  - 'edk2'
  tool_chain_tag_build_list:
  - 'VS2015x86'
  - 'VS2017'
  - 'GCC5'
  - 'XCODE5'
  arch_build_list:
  - 'IA32'
  - 'X64'
  - 'ARM'
  - 'AARCH64'
  packages_build_list:
  linux_packages_build_list:
  windows_packages_build_list:
```
* `git_commands` - Any sequence of `git` commands required to install the EDK II
  sources required for the package/platform builds.  Multiple repositories may
  be cloned into a single WORKSPACE and specific branches can be checked out.
  The default value clones the edk2 repository from Tianocore and updates all
  submodules.
* `x11_prerequisite` - Default is `'false'`.  If the `EmulatorPkg` is built for
  Linux or MacOS, then this parameter must be set to `'true'` to install the
  the extra required prerequisites.
* `edk2_path`: The WORKSPACE relative path to the main edk2 sources that are
  used to build `BaseTools` and execute `edksetup.bat` or `edk2setup.sh`.  The
  default value is `'edk2'` which means no setting is required if the main edk2
  sources are cloned into their default location in WORKSPACE.  An example where
  a different value is required is if multiple `edk2` branches are cloned into
  the same WORKSPACE and `BaseTools` and `edksetup` need to be used from a
  directory other than `edk2`.
* `build_target_list` - List of EDK II build targets to use to build the
  specified packages/platforms.  The default is the `'DEBUG'` target.  The
  `tools_def.txt` file specifies the available set of build targets.
* `packages_path_list` - List of WORKSPACE relative paths used to generate the
  PACKAGES_PATH environment variable.  The default is the `'edk2'` directory.
  If multiple repositories are cloned into WORKSPACE, then this list is expanded
  based on the PACKAGES_PATH setting required for the required packages/platforms
  builds.
* `tool_chain_tag_build_list` - List of tool chain tags to use to generate
  build commands for the specified packages/platforms builds.  The default is to
  build for all supported tool chain tags (VS2015x86, VS2017, GCC5, and XCODE5).
  A smaller set of tool chain tags can be specified to reduce the total number
  of builds.
* `arch_build_list` - List of CPU archs to use to generate build commands for
  the specified package builds.  The default is to build packages for all the
  supported CPU archs (IA32, X64, ARM, AARCH64).  If a tool chain tag does not
  support a specific CPU arch, then the build is skipped.  A smaller set of CPU
  archs can be specified to reduce the total number of builds.
* `packages_build_list` - List of package DSC files to build.  Additional `-D`
  flags can be optionally provided.  If one or more `-a` CPU architecture flags
  are specified, then the build is assumed to be a platform build and only the
  specified CPU archs are used.
* `linux_packages_build_list` - List of package DSC files to build, but only on
  Linux/UNIX  Host OS environments.  The syntax is the same as
  `packages_build_list`.  So far, the only time this parameter is used is to
  build the EmulatorPkg for Linux/UNIX environments.
* `windows_packages_build_list` - List of package DSC files to build, but only
  on Windows like Host OS environments.  The syntax is the same as
  `packages_build_list`.  So far, the only time this parameter is used is to
  build the EmulatorPkg for Windows environments.

## Build single package in TianoCore edk2 repository

The following is the simplest `azure_pipelines.yml` file that builds the
`FatPkg` from the `master` branch of the `edk2` repository on TianoCore .
Builds are performed for the DEBUG build target on VS2015x86, VS2017, GCC5, and
XCODE5 for all the CPU archs that each of those tool chains support.

```
trigger:
  branches:
    include:
      - patchset/*

jobs:
  - template: AzurePipelines/DoEdk2Build.yml
    parameters:
      packages_build_list:
      - 'FatPkg/FatPkg.dsc'
```

## Build developer branch from fork of edk2 repository

The following is a version of `azure_pipelines.yml` that clones a developer fork
of the `edk2` repository and checks out a specific branch.  This is an example
of what an EDK II developer or maintainer may do to test a patchset under review.

```
trigger:
  branches:
    include:
      - patchset/*

jobs:
  - template: AzurePipelines/DoEdk2Build.yml
    parameters:
      git_commands: |
        git clone --depth 1 https://github.com/mdkinney/edk2.git -b BZ_9999_FatPkgFixes
      packages_build_list:
      - 'FatPkg/FatPkg.dsc'
```

## Build EmulatorPkg from TianoCore edk2 repository

The following example builds the EmulatorPkg.  The `x11_prerequisite` must be
set to `'true'` for the EmulatorPkg.  Also, since different `-D` flags are
required for Linux and Windows, the `linux_packages_build_list` and
`windows_packages_build_list` parameters must be used instead of
`packages_build_list`.

```
trigger:
  branches:
    include:
      - patchset/*

jobs:
  - template: AzurePipelines/DoEdk2Build.yml
    parameters:
      x11_prerequisite: 'true'
      linux_packages_build_list:
      - 'EmulatorPkg/EmulatorPkg.dsc -a IA32 -D UNIX_SEC_BUILD'
      - 'EmulatorPkg/EmulatorPkg.dsc -a X64  -D UNIX_SEC_BUILD'
      windows_packages_build_list:
      - 'EmulatorPkg/EmulatorPkg.dsc -a IA32 -D WIN_SEC_BUILD'
      - 'EmulatorPkg/EmulatorPkg.dsc -a X64  -D WIN_SEC_BUILD'
```

## Build Platform from edk2-platforms using Multiple Repositories

The following example builds the 64-bit and 32-bit versions of the
Vlv2TbltDevicePkg platform firmware.  Three repositories are cloned and the
submodules in the edk2 are also updated to add the OpenSSL dependencies.
`packages_path_list` is set based on the Readme.md for the Vlv2TbltDevicePkg.
Since these are platform builds, the `-a` flags are set in `packages_build_list`
as required in the Readme.md for the Vlv2TbltDevicePkg.

```
trigger:
  branches:
    include:
      - patchset/*

jobs:
  - template: AzurePipelines/DoEdk2Build.yml
    parameters:
      git_commands: |
        git clone --depth 1 https://github.com/tianocore/edk2-platforms.git
        git clone --depth 1 https://github.com/tianocore/edk2-non-osi.git
        git clone --depth 1 https://github.com/tianocore/edk2.git
        cd edk2
        git submodule update --init
      packages_path_list:
      - 'edk2'
      - 'edk2-platforms/Silicon/Intel'
      - 'edk2-platforms/Platform/Intel'
      - 'edk2-non-osi/Silicon/Intel'
      packages_build_list:
      - 'Vlv2TbltDevicePkg/Vlv2TbltDevicePkgX64.dsc  -a IA32 -a X64'
      - 'Vlv2TbltDevicePkg/Vlv2TbltDevicePkgIA32.dsc -a IA32'
```

## Build New Feature from edk2-staging

The following example uses new FmpDevicePkg features under development in the
edk2-staging repo.  It builds the FmpDevicePkg from the edk2-staging repository.

```
trigger:
  branches:
    include:
      - patchset/*

jobs:
  - template: AzurePipelines/DoEdk2Build.yml
    parameters:
      git_commands: |
        git clone --depth 1 https://github.com/tianocore/edk2-staging.git -b Bug_1525_FmpDevicePkg_MultipleControllers_V2
        cd edk2-staging
        git submodule update --init
      edk2_path: 'edk2-staging'
      packages_path_list:
      - 'edk2-staging'
      packages_build_list:
      - 'FmpDevicePkg/FmpDevicePkg.dsc'
```

## Use filters to limit number of builds

The following example expands the build targets to both DEBUG and RELEASE, but
limits the tool chains to only VS2015x86 and VS2017 and limits the CPU archs
to only X64.

```
trigger:
  branches:
    include:
      - patchset/*

jobs:
  - template: AzurePipelines/DoEdk2Build.yml
    parameters:
      build_target_list:
      - 'DEBUG'
      - 'RELEASE'
      tool_chain_tag_build_list:
      - 'VS2015x86'
      - 'VS2017'
      arch_build_list:
      - 'X64'
      packages_build_list:
      - 'FatPkg/FatPkg.dsc'
```

# Maintainers

See [Maintainers.txt](Maintainers.txt).
