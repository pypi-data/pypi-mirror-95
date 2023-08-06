MCServerLib
===========

MCServerLib is a Python library that helps build Minecraft servers.

[한국어 README 바로가기](https://github.com/myoung2namur/MCServerLib/blob/master/docs/README-kr.md)
# Installation

### From PyPi:

`pip install MCServerLib`


### From Repo:

`python -m pip install git+https://github.com/myoung2namur/MCServerLib`

# Usage

```py
import MCServerLib as mcs

properties = mcs.Prop.Properties()
properties.properties['enable-command-block'] = 'true'

setup = mcs.Setup.Setup(version='1.16.5',xmx='1024M',xms='3G',properties=properties)

# Setup Server Files

# Download All Basic Server Files
setup.downloadAll() 

# Download Only Paper Bukkit
setup.downloadPaper()

# Make Only Batch File
setup.makeBatch()

# Make only Eula File
setup.makeEula()
```