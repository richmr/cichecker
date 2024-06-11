# cichecker

This is an extensible tool to allow for verifying critical configuration items of mutable servers.

Critical configuration items are anything that an application running on that server needs to run correctly.  This could be:
- Ensuring code or configuration files are not modified
- Ability to connect to downstream resources
- Registry key settings (Windows only)
- etc. (more capabilities added as new types of configuration items are identified)

It is intended to be queried by another tool (such as Nagios) for alerting and analysis.

Currently the tool has been written to be used as a Nagios plugin, see Installation below

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

Currently the best way to install is to clone this repository, move into the directory, and then use `pip install -e .`.  This will set the `cichecker` command up in your path.  The `-e` will allow you to keep your install updated with a simple `git pull` when needed.  On Windows you may get warnings about the script location not being on the path, be sure to fix those issues.

### Installation as a Nagios plugin

#### Windows

To use cichecker as a plugin for Nagios you need to turn it into an executable and put in the Nagios plugin folder.

To turn into an executable, move into the `src` directory and then use `pyinstaller cicheckercli.py`.  Pyinstaller should have been installed when you installed cichecker.  If not, use `pip install pyinstaller`.  This will generate an executable and accompanying folder under the `dist` folder:

```
 Directory of C:\Users\user\Documents\GitHub\cichecker\src\dist\cicheckercli

06/11/2024  12:47 PM    <DIR>          .
06/11/2024  12:47 PM    <DIR>          ..
06/11/2024  12:47 PM        19,624,530 cicheckercli.exe
06/11/2024  12:47 PM    <DIR>          _internal
               1 File(s)     19,624,530 bytes
               3 Dir(s)  324,520,841,216 bytes free
```

You need to copy the executable and the full directory tree in _internal to `C:\Program Files\Nagios\NCPA\plugins`.

If you are doing development work on the cichecker, set up symbolic links in the plugins directory to the `dist` folder:

```
C:\Program Files\Nagios\NCPA\plugins>dir
 Volume in drive C is Windows
 Volume Serial Number is 7C9D-643E

 Directory of C:\Program Files\Nagios\NCPA\plugins

06/07/2024  11:08 AM    <DIR>          .
06/06/2024  11:47 AM    <DIR>          ..
06/07/2024  11:08 AM    <SYMLINK>      cicheckercli.exe [C:\Users\user\Documents\GitHub\cichecker\src\dist\cicheckercli\cicheckercli.exe]
06/07/2024  11:01 AM    <SYMLINKD>     _internal [C:\Users\user\Documents\GitHub\cichecker\src\dist\cicheckercli\_internal]
               6 File(s)     28,901,010 bytes
               4 Dir(s)  324,519,378,944 bytes free

C:\Program Files\Nagios\NCPA\plugins>
```

Avoid making a single-file executable because the unpacking operation will take too long and will slow down your check times.

#### Linux

Actually, this has not been tested on linux yet.  You might be able to copy the `cicheckercli.py` script to the plugins directory but this will only work if the packages needed to run cichecker have been installed at the root level or as the user NCPA uses when it is running.

## Usage

When using this as a NCPA plugin, use it as you would any other NCPA plugin.

It is planned to make cichecker expose an API service in the future for integration into other tooling, but this is not in place yet.

## License

`cichecker` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
