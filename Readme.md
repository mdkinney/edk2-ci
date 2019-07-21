# EDK II Continuous Integration Project

* [Overview](#overview)
* [Maintainers](#maintainers)

# Overview

The majority of the content in the EDK II open source project uses a
[BSD-2-Clause Plus Patent License](License.txt).

The master branch of the edk2-ci rpository contains the templates for files
required in a patchset branch that initiates an Continuous Integration(CI)
process.  git repositories and git branches may be used from TianoCore or public
forks of TianoCore.  The branch naming convention is:

    patchset/<github id>/BZ_<bz id>/V<patch set version>/<title>

For example:

    patchset/mdkinney/BZ_1234/V1/Add_My_New_Feature

The required files in a `patchset` branch are:

    Readme.txt            # Same as edk2-ci/master
    License.txt           # Same as edk2-ci/master
    Maintainers.txt       # Same as edk2-ci/master 
    azure_pipelines.yml   # Same as edk2-ci/master
    GitCommands.txt       # Customize
    BuildCommands.txt     # Customize

There is no FW code in a patchset branch.  Instead, a patchset branch provides
an inventory of git repositories/branches to use for a CI build and the set of
build commands to run against those git repositories/branches.  When a branch
that follows the branch naming convension is pushed to edk2-ci, it starts a 
CI build using the inventory of git repositories/branches and build commands.
A developer typically prepares a patchset in branch(s) in their personal fork of
the EDK II repositories.  The GitCommands.txt file in the patchset branch is
updated to point to these branch(s) in their personal fork of the EDK II
repositories.

Each CI environment must be initialized to be compatible with an EDK II build.
The following CI environments are supported:

* Azure Pipelines - azure_pipelines.yml

If the default evironment provided is not compatible with the build commands,
then the YML file can be customized in the patchset branch.


Any contributions to this branch should be submitted via email to the
EDK II mailing list with a subject prefix of `[edk2-ci]`. See
[Laszlo's excellent guide](https://github.com/tianocore/tianocore.github.io/wiki/Laszlo's-unkempt-git-guide-for-edk2-contributors-and-maintainers)
for details on how to do this successfully.

# Maintainers

See [Maintainers.txt](Maintainers.txt).
