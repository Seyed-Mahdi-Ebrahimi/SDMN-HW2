import subprocess
import argparse
import os
import sys
import time

# *************************************************************************************************************

Container_Repository = './Container_Repository'
Default_FileSystem = '{}/DEFAULT_rootfs'.format(Container_Repository)
MyArgs = None

# *************************************************************************************************************

def init_container():
    # 
    if not os.path.exists(Container_Repository):
        os.makedirs(Container_Repository)
    # 
    hostname_fs = '{}/{}'.format(Container_Repository, MyArgs.container_hostname)
    init_hostname_fs(hostname_fs)
    # 
    namespace_dir = '{}/namespaces'.format(hostname_fs)
    ns_flags = '--user={namespace}/usr --uts={namespace}/uts --net={namespace}/net --mount={namespace}/mnt'.format(namespace=namespace_dir)
    os.system('unshare {flags} --pid --fork --map-root-user hostname {hostname}'.format(flags=ns_flags, hostname=MyArgs.container_hostname))
    # 
    print('>> Container with hostname [{}] initialized.'.format(MyArgs.container_hostname))
    print('>>> Starting container [{}] ...'.format(MyArgs.container_hostname))
    # 
    cmd = 'nsenter {flags} unshare -pf chroot {working_dir}/{rootfs} bash -c "mount -t proc proc /proc && bash"'.format(flags=ns_flags, working_dir=os.getcwd(), rootfs=hostname_fs)
    if MyArgs.memory_limit is not None:
        cmd = 'systemd-run --scope -p MemoryLimit={mem_limit}M {command}'.format(mem_limit=MyArgs.memory_limit, command=cmd)
    os.system(cmd)

# # *************************************************************************************************************

def init_hostname_fs(hostname_fs):
    if not os.path.exists(hostname_fs):
        os.makedirs(hostname_fs)
        print('> Creating a directory for hostname: [{}]'.format(hostname_fs))
    # 
    if not check_hostname_fs(hostname_fs):
        print('> Creating root filesystem for [{}]...'.format(MyArgs.container_hostname))
        create_hostname_fs(hostname_fs)

# # *************************************************************************************************************

def check_hostname_fs(hostname_fs):
    expected_default_ubuntu2004_fs = ['bin', 'boot', 'dev', 'etc', 'home', 'lib', 'lib64', 'media', 'mnt', 'opt', 'proc', 'root', 'run', 'sbin', 'srv', 'sys','tmp', 'usr', 'var']
    current_fs = os.listdir(hostname_fs)
    check_fs = all(item in current_fs for item in expected_default_ubuntu2004_fs)
    return check_fs

# *************************************************************************************************************

def create_hostname_fs(hostname_fs):
    if not os.path.exists(Default_FileSystem):
        print('> But DEFAULT root filesystem is not exist.')
        os.makedirs(Default_FileSystem)
        # 
        if not is_debootstrap_installed():
            print('> Instlling debootstrap ...')
            os.system('apt instll debootstrap')
        print('> Creating DEFAULT root filesystem...')
        # If we want a minimal fs, we can add the `--variant=minbase` option.
        os.system('sudo debootstrap focal {}'.format(Default_FileSystem))
        print('> DEFAULT root filesystem created.')
    os.system('cp -r {}/* {}'.format(Default_FileSystem, hostname_fs))
    global MyArgs
    print('> root filesystem for [{}] created.'.format(MyArgs.container_hostname))
    
    # Creating namespaces...
    namespaces_list = ['net', 'usr', 'mnt', 'uts']
    namespace_dir = '{}/namespaces'.format(hostname_fs)
    if not os.path.exists(namespace_dir):
        os.makedirs(namespace_dir)
    for ns in namespaces_list:
        with open('{}/{}'.format(namespace_dir, ns), 'w+') as fd:
            pass
    # 
    os.system("mount --bind {namespace} {namespace}".format(namespace=namespace_dir))
    os.system("mount --make-private {namespace}".format(namespace=namespace_dir))
    os.system('mount --bind {}/proc {}/proc'.format(hostname_fs, hostname_fs))
    os.system('mount --make-private {}/proc'.format(hostname_fs)) 

# *************************************************************************************************************

def delete_container():
    hostname_fs = '{}/{}'.format(Container_Repository, MyArgs.container_hostname)
    if not os.path.exists(hostname_fs):
        print('\n--> [!!!] No such container exist [!!!]\n')
        return
    # At first, we umount some files that we previously mounted.
    os.system('umount {}/namespaces/*'.format(hostname_fs))
    os.system('umount {}/namespaces'.format(hostname_fs))
    os.system('umount {}/proc'.format(hostname_fs))
    # Experimentally, I found that a delay between `umount` and `rm` makes the erase operation always successful.
    time.sleep(1)
    # At the end, we delete container root filesystem.
    os.system("rm -r {}".format(hostname_fs))
    print('>>> Container with hostname [{}] has been deleted.'.format(MyArgs.container_hostname))

# # *************************************************************************************************************

def list_containers():
    containers_dir = os.listdir(Container_Repository)
    containers_list = []
    for d in containers_dir:
        containers_list.append(d.split('/')[-1])
    if 'DEFAULT_rootfs' in containers_list:
        containers_list.remove('DEFAULT_rootfs')
    print('\n******************* Available Containers: ******************* ')
    for el in containers_list:
        print('-> {}'.format(el))
    
    # print a newline
    print('')

# # *************************************************************************************************************

def is_debootstrap_installed():
    try:
        subprocess.run(['debootstrap', '--version'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

# *************************************************************************************************************

def read_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', help='This option starts a container. If it does not exist, it will be created first.')
    parser.add_argument('-d', '--delete', help="With this flag, the user determines whether to delete a container or not.")
    parser.add_argument('-ml', '--memory-limit', type=int, help="Its unit is megabytes. This argument is optional and can be left unspecified.")
    parser.add_argument('-l', '--list', action='store_true', help="With this flag, the user can view all available containers.")
    args = parser.parse_args()
    if args.delete is not None:
        args.container_hostname = args.delete
    elif args.start is not None:
        args.container_hostname = args.start
    return args

# *************************************************************************************************************

if __name__ == '__main__':
    MyArgs = read_args()
    # 
    if MyArgs.list:
        list_containers()
        sys.exit()
    # 
    if MyArgs.delete is not None:
        delete_container()
    elif MyArgs.start is not None:
        init_container()
    else:
        # We should never be in this part of the code.
        assert(False)
