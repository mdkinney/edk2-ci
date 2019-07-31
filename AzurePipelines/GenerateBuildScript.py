## @file
#  Python script that generate shell script to set PACKAGES_PATH and a set of
#  EDK II build commands.
#
#  Copyright (c) 2019, Intel Corporation. All rights reserved.<BR>
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#
##

import os

#print (os.environ['WORKSPACE'])
#print (os.environ['EDK2_PATH'])
#print (os.environ['PACKAGES_PATH'])
#print (os.environ['TOOL_CHAIN_TAG'])
#print (os.environ['TOOL_CHAIN_ARCHS'])
#print (os.environ['BUILD_TARGET_LIST'])
#print (os.environ['PACKAGES_BUILD_LIST'])
#print (os.environ['TOOL_CHAIN_TAG_BUILD_LIST'])
#print (os.environ['ARCH_BUILD_LIST'])

Workspace = os.environ['WORKSPACE'].replace('\\','/')
Edk2Path = os.environ['EDK2_PATH'].replace('\\','/')
PackagesPathList = os.environ['PACKAGES_PATH'].strip('"').split(os.pathsep)
ToolChainTag = os.environ['TOOL_CHAIN_TAG']
ToolChainArchs = os.environ['TOOL_CHAIN_ARCHS'].strip('"').split()
BuildTargetList = os.environ['BUILD_TARGET_LIST'].strip('"').split()
PackagesBuildList = os.environ['PACKAGES_BUILD_LIST'].strip('"').replace('\\','/').split(':')
ToolChainTagBuildList = os.environ['TOOL_CHAIN_TAG_BUILD_LIST'].strip('"').split()
ArchBuildList = os.environ['ARCH_BUILD_LIST'].strip('"').split()
BuildArtifactStagingDirectory = os.environ['BUILD_ARTIFACTSTAGINGDIRECTORY'].replace('\\','/')
if (os.pathsep == ':'):
  print ('cd ' + os.path.normpath(Edk2Path))
  print ('. edksetup.sh')
  print ('cd ..')
  BuildCommand = 'build'
else:
  print ('cd ' + os.path.normpath(Edk2Path))
  print ('call edksetup.bat')
  print ('cd ..')
  BuildCommand = 'call build'
for Package in PackagesBuildList:
  if Package.strip() == '':
    continue
  if ToolChainTag not in ToolChainTagBuildList:
    continue
  PackageDec = os.path.normpath(Package.split()[0])
  PackageArchs = []
  PackageDirName = ''
  for PackagePath in PackagesPathList:
    PackageFileName = os.path.normpath(os.path.join (PackagePath, PackageDec))
    if os.path.exists (PackageFileName):
      for Line in open (PackageFileName, 'r').readlines():
        if PackageArchs == []:
          if Line.strip().startswith ('SUPPORTED_ARCHITECTURES'):
            PackageArchs = Line.split('=')[1].split('|')
            PackageArchs = [x.strip() for x in PackageArchs]
        if PackageDirName == '':
          if Line.strip().startswith ('OUTPUT_DIRECTORY'):
            PackageDirName = os.path.split(Line.split('=')[1])[1].strip()
    if PackageArchs != [] and PackageDirName != '':
      break
  if PackageArchs == [] or PackageDirName == '':
    continue
  for BuildTarget in BuildTargetList:
    if '-a' in Package.split():
      Compat = True
      for Arch in PackageArchs:
        if Arch not in ArchBuildList:
          Compat = False
        if Arch not in ToolChainArchs:
          Compat = False
      if not Compat:
        continue
      Arch = Package.split('-a')[1].split()[0].strip()
      PackageDirName = PackageDirName.replace('$(ARCH)', Arch)
      LogFile = os.path.normpath(os.path.join(BuildArtifactStagingDirectory, PackageDirName + '_' + BuildTarget + '_' + ToolChainTag + '.log'))
      ReportFile = os.path.normpath(os.path.join(BuildArtifactStagingDirectory, PackageDirName + '_' + BuildTarget + '_' + ToolChainTag + '.report'))
      Cmd = '{BuildCommand} -n 0 -b {BuildTarget} -t {ToolChainTag} -p {Package} -j {LogFile} -y {ReportFile}'.format (
        BuildCommand = BuildCommand,
        BuildTarget = BuildTarget,
        ToolChainTag = ToolChainTag,
        Package = Package,
        LogFile = LogFile,
        ReportFile = ReportFile
        )
      print (Cmd)
    else:
      for Arch in ToolChainArchs:
        if Arch not in PackageArchs:
          continue
        if Arch not in ArchBuildList:
          continue
        LogFile = os.path.normpath(os.path.join(BuildArtifactStagingDirectory, PackageDirName + '_' + BuildTarget + '_' + ToolChainTag + '_' + Arch + '.log'))
        ReportFile = os.path.normpath(os.path.join(BuildArtifactStagingDirectory, PackageDirName + '_' + BuildTarget + '_' + ToolChainTag + '_' + Arch + '.report'))
        Cmd = '{BuildCommand} -n 0 -a {Arch} -b {BuildTarget} -t {ToolChainTag} -p {Package} -j {LogFile} -y {ReportFile}'.format (
          BuildCommand = BuildCommand,
          Arch = Arch,
          BuildTarget = BuildTarget,
          ToolChainTag = ToolChainTag,
          Package = Package,
          LogFile = LogFile,
          ReportFile = ReportFile
          )
        print (Cmd)
