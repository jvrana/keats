# keats change log
## 0.2.26
**2019-07-29T10:19:39.575446**
new functionality

 - `keats install` will install keats to development and update changelog and version


## 0.2.25
**2019-07-28T07:44:49.444992**





## 0.2.23
**2019-07-07T21:25:53.051008**
minor features

 - added Safe file writer for changelog


## 0.2.22
**2019-07-07T14:59:32.805161**
fixed changelog bugs

 - fixed error in which uninitialized project would through error due to changelog being missing
 - changelog json is now sorted by date
 - fixed bug in which changelog.json would go missing if exception was thrown


## 0.2.21
**2019-07-07T14:44:16.586064**
bug fixes

 - fixed bug that was causing error when initializing a new changelog


## 0.2.20
**2019-07-07T14:39:19.932877**
bug fixes

 - fixed bug in which autogeneration tag displayed the wrong number
 - remove version.py, an legacy file


## 0.2.19
**2019-07-07T13:41:14.833050**
minor api changes

 - develop will now remove 'dist' and 'pip-wheel-metadata' folders


## 0.2.18
**2019-07-07T13:29:00.145886**
new features

 - new global_install and develop commands
 - exits gracefully from the cli if cwd is does not have a pyproject.toml file


## 0.2.17
**2019-07-07T13:28:00.960624**
new features

 - new develop and global_install commands


## 0.2.15
**2019-07-05T15:06:43.817247**
bug fix

 - during update, poetry cache was not clearing


## 0.2.14
**2019-07-05T11:37:54.021629**
change to interface

 - update and install will now be quiet


## 0.2.13
**2019-07-05T11:33:10.379093**
new features

 - added 'install' and 'update' methods to cline


## 0.2.12
**2019-07-05T11:22:14.488037**
update to release script

 - more information displayed for publishing repository


## 0.2.11
**2019-07-05T11:19:45.284233**
bug fixes

 - fixed release script


## 0.2.10
**2019-07-05T11:18:17.928748**





## 0.2.9
**2019-07-05T11:16:36.512630**


 - updates to cli documentation
 - update to interactive scripts


## 0.2.8
**2019-07-05T10:00:22.396703**
minor api change

 - release can be accessed from 'keats release' instead of 'keats run release'
 - updated README.md


## 0.2.7
**2019-07-05T09:18:24.979212**
Adds support for lesser Python3 versions

 - support for py35, py35, py37
 - added tox tests


## 0.2.6
**2019-07-04T21:20:54.169900**
minor bug fix

 - fixed bug that was causing warning about missing file


## 0.2.5
**2019-07-04T21:18:38.725436**





## 0.2.4
**2019-07-04T21:10:34.993149**
updated package info




## 0.2.3
**2019-07-04T21:08:29.136853**
updated readme




## 0.2.2
**2019-07-04T21:05:35.607437**
minor change

 - added pypi classifiers


## 0.2.1
**2019-07-04T20:13:05.147834**
fixed bug




## 0.2.0
**2019-07-04T20:10:42.970256**
api changes

 - 'package' and 'name' are now different
 - tests for 'package' and 'name'
 - fixed bug in which the keats version referred to the old version instead of the one located in the toml file


## 0.1.1
**2019-07-04T19:53:24.318926**
major bug fixes

 - 'v' now returns version number


## 0.1.0
**2019-07-04T19:39:56.624179**
refactored and api changes

 - interface is split into 'run', 'version', and 'changelog'


## 0.0.2
**2019-07-04T19:39:13.400230**





## 0.0.3
**2019-07-04T19:32:36.374869**



