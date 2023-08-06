# ZFS Manager Manager

Tool to add version control and historic data of a directory with ZFS. The functionality is similar to Solaris beadm but generalized for any ZFS filesystem, not just ROOT and VAR.

The suggested workflow is:
1. Initialize (zcm init)
2. Make changes in active clone
3. Create clone (zcm create)
4. Make changes in new clone
5. Activate clone (zcm activate)
6. [Remove older clones (zcm rm)]
7. Go to step 2

## Usage

- Initialize ZCM

```bash
$ zcm init rpool/directory /directory
ZCM initialized ZFS rpool/directory at path /directory
```

"rpool/directory" -> root of the ZFS for clones and snapshots.

"/directory" -> path of the filesystem (mountpoint of the active clone).


- Show ZCM information

```bash
$ zcm ls /directory
MANAGER          A  ID        CLONE                     MOUNTPOINT  ORIGIN    DATE                 SIZE    
rpool/directory     00000001  rpool/directory/00000000  /directory            2021-02-16 10:46:59  32.00 KB
```

- Create new clones (derived from active)

```bash
$ zcm create /directory
Created clone 00000001 at path /directory/.clones/00000001
$ zcm create /directory
Created clone 00000002 at path /directory/.clones/00000002
$ zcm ls /directory
MANAGER          A  ID        CLONE                     MOUNTPOINT                   ORIGIN    DATE                 SIZE    
rpool/directory  *  00000000  rpool/directory/00000000  /directory                             2021-02-20 06:51:14  32.00 KB
rpool/directory     00000001  rpool/directory/00000001  /directory/.clones/00000001  00000000  2021-02-20 06:57:01  18.00 KB
rpool/directory     00000002  rpool/directory/00000002  /directory/.clones/00000002  00000000  2021-02-20 06:57:02  18.00 KB
```

- Activate the previously created clone, mounting it at ZCM path 

```bash
$ zcm activate /directory 00000002
Activated clone 00000002
```

The activate command can not be executed from inside the path, therefore the parameter -p <path> is mandatory.  

- All the clones are visible at <path>/.clones

```bash
$ cd /directory
$ ls .clones
0000000 00000001 00000002
```


- Remove clones

```bash
$ zcm rm /directory 00000001
WARNING!!!!!!!!
All the filesystems, snapshots and directories associated with clone 00000001 will be permanently deleted.
This operation is not reversible.
Do you want to proceed? (yes/NO) yes
Removed clone 00000001
```


- Destroy ZCM related data

This is dangerous, you should backup data first.

```bash
$ zcm destroy /directory
WARNING!!!!!!!!
All the filesystems, clones, snapshots and directories associated with rpool/directory will be permanently deleted.
This operation is not reversible.
Do you want to proceed? (yes/NO) yes
Destroyed ZCM rpool/directory
```
