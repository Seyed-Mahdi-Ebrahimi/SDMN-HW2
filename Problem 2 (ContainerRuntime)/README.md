# Problem 2 (Container Runtime)
In the following, the explanation of problem 2 from HW2 will be given.

In this problem, a container runtime (a very simple version of Docker) is developed and implemented with **Python3**.

All the demands of the program are developed in script `ContainerManager.py`.

The following can be done with this script:
- [Creating and starting a container and even defining memory limit consumption for it.](#start)
- [Listing all available containers](#list)
- [Deleting a container](#del)

This script is used as follows:

<a id="start"></a>
- **Starting a container**: **`-s`** or **`--start`**
```bash
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --start [myhostname]
# For example:
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --start MyNewContainer
> Creating a directory for hostname: [./Container_Repository/MyNewContainer]
> Creating root filesystem for [MyNewContainer]...
> root filesystem for [MyNewContainer] created.
>> Container with hostname [MyNewContainer] initialized.
>>> Starting container [MyNewContainer] ...
root@MyNewContainer:/# 
root@MyNewContainer:/# ps fax
    PID TTY      STAT   TIME COMMAND
      1 ?        S      0:00 bash
      9 ?        R+     0:00 ps fax
root@MyNewContainer:/#
```
After running the above command, if the container does not already exist, it will create it first.

For each counter, a folder named `[myhostname]` is created, which is entered by the user. All the required files and folders (related to the filesystem and container spaces) are created in `[myhostname]` folder.
It should also be noted that all containers are created and stored in the `Container_Repository` folder, which is automatically created in the same folder as `ContainerManager.py`.

- Starting a container with **memory limitation**: **`-s`** or **`--start`** with **`-ml`** or **`--memory-limit`**
```bash
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --start [myhostname] --memory-limit [IntValueMB]
# For example:
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --start MyNewContainer --memory-limit 100
>> Container with hostname [MyNewContainer] initialized.
>>> Starting container [MyNewContainer] ...
Running scope as unit: run-rc294d728bddc42dfa7b0a03a10de76d1.scope
root@MyNewContainer:/# 
root@MyNewContainer:/# python3
Python 3.8.2 (default, Mar 13 2020, 10:14:16) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> lst = ['Hello!'] * 500000000
Killed
root@MyNewContainer:/#
```
`[IntValue]` is an integer number with units of megabytes.

<a id="list"></a>
- **Listing all available containers**: **`-l`** or **`--list`**
```bash
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --list

******************* Available Containers: ******************* 
-> AnotherContainer
-> MyNewContainer

~/sdmn/hw2/q2$
```
After executing this command, all the containers that have been created by this script will be displayed.

<a id="del"></a>
- **Deleting a container**: **`-d`** or **`--delete`**
```bash
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --delete [desired-hostname]
# For example:
~/sdmn/hw2/q2$ sudo python3 ContainerManager.py --delete MyNewContainer
>>> Container with hostname [MyNewContainer] has been deleted.
~/sdmn/hw2/q2$ 
```
After the execution of this command, some `umount` commands (related to the namespaces of this container) will be executed and finally the desired container and all its related folders will be deleted.
