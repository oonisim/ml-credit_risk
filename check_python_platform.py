import sysconfig
import platform
import distutils

print(distutils.util.get_platform())
print("Platform:", sysconfig.get_platform())
print("Machine:", platform.machine())
print("System:", platform.system())

# Get all compatible tags
from packaging.tags import sys_tags
for tag in list(sys_tags())[:10]:  # Show first 10
    print(f"{tag.interpreter}-{tag.abi}-{tag.platform}")
