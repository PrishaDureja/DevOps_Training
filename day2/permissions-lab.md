Scenario 1: A private file is readable by others

Goal: alice’s file should be secret, but right now bob can read it.

1.1 Alice creates a file.

bash
su - alice -c 'echo "alice secret" > /srv/lab/alice/secret.txt'

What it does: As alice, it writes the text alice secret into a new file called secret.txt in her folder. The > means “put the output into this file”.

1.2 Bob tries to read it.

bash
su - bob -c 'cat /srv/lab/alice/secret.txt'

What it does: As bob, it prints the file’s contents. You will see alice secret, which is the problem: bob should not be able to read it.

1.3 Fix it: lock the file.

bash
su - alice -c 'chmod 600 /srv/lab/alice/secret.txt'

What it does: chmod changes permissions. 600 means the owner (alice) can read and write, and nobody else gets anything.

1.4 Bob tries again.

bash
su - bob -c 'cat /srv/lab/alice/secret.txt'

What it does: Same as 1.2. Expected: Permission denied.

1.5 Check the permissions.

bash
ls -l /srv/lab/alice/secret.txt

What it does: ls -l lists the file with its permissions. Expected: -rw------- (only the owner can read and write).

Scenario 2: A shared folder for the devs team only

Goal: alice and bob can edit files together, and carol is locked out.

2.1 Give the folder to the devs group.

bash
chown root:devs /srv/lab/devs-share

What it does: chown changes the owner. This sets the owner to root and the group to devs, so alice and bob (both in devs) now count as the group.

2.2 Set the folder permissions.

bash
chmod 2770 /srv/lab/devs-share

What it does: 770 means owner and group have full access, and others (like carol) have none. The extra 2 is the setgid bit: every new file in this folder automatically belongs to group devs.

2.3 Alice creates a shared file.

bash
su - alice -c 'umask 002; echo "from alice" > /srv/lab/devs-share/plan.txt'

What it does: umask 002 tells Linux to make new files group-writable, so bob can edit them. Then alice writes from alice into plan.txt.

2.4 Bob adds a line to the same file.

bash
su - bob -c 'echo "from bob" >> /srv/lab/devs-share/plan.txt'

What it does: >> means “add to the end of the file” (unlike >, which replaces the contents). It works because bob is in devs.

2.5 Read the file.

bash
cat /srv/lab/devs-share/plan.txt

What it does: Prints the file. Expected: both lines, from alice and from bob.

2.6 Carol tries to look inside.

bash
su - carol -c 'ls /srv/lab/devs-share'

What it does: Carol tries to list the folder. Expected: Permission denied, because she is not in devs.

2.7 Check the folder permissions.

bash
ls -ld /srv/lab/devs-share

What it does: -d shows the folder itself, not its contents. Expected: drwxrws---. The s is the setgid bit.

Scenario 3: A script won’t run

Goal: fix Permission denied when running a script.

3.1 Alice creates a script.

bash
su - alice -c 'printf "#!/bin/bash\necho Hello from script\n" > /srv/lab/alice/hello.sh'

What it does: printf writes two lines into hello.sh. \n means “new line”. Line 1 (#!/bin/bash) says “run this with bash”. Line 2 prints Hello from script.

3.2 Alice tries to run it.

bash
su - alice -c '/srv/lab/alice/hello.sh'

What it does: Tries to run the script. Expected: Permission denied, because new files don’t get the execute permission.

3.3 Fix: add execute.

bash
su - alice -c 'chmod u+x /srv/lab/alice/hello.sh'

What it does: u+x means “give the user (owner) the execute permission”. The other parts of the permissions stay the same.

3.4 Run it again.

bash
su - alice -c '/srv/lab/alice/hello.sh'

What it does: Runs the script. Expected: Hello from script.

Scenario 4: The wrong owner blocks editing

Goal: alice can’t edit a file in her own folder because root owns it.

4.1 Root creates a file in alice’s folder.

bash
echo "owned by root" > /srv/lab/alice/report.txt

What it does: You are root here, so the file is owned by root. Alice only gets “others” permission, which is read-only.

4.2 Alice tries to edit it.

bash
su - alice -c 'echo "alice edit" >> /srv/lab/alice/report.txt'

What it does: Alice tries to add a line. Expected: Permission denied, because she doesn’t own the file.

4.3 Fix: change the owner.

bash
chown alice:devs /srv/lab/alice/report.txt

What it does: Makes alice the owner and devs the group of the file.

4.4 Alice tries again.

bash
su - alice -c 'echo "alice edit" >> /srv/lab/alice/report.txt'

What it does: Same edit as 4.2. This time it works silently (no output means success).

4.5 Check the result.

bash
cat /srv/lab/alice/report.txt
ls -l /srv/lab/alice/report.txt

What it does: The first prints the file (both lines). The second shows the owner. Expected: alice devs in the listing.

Scenario 5: Anyone can delete other people’s files

Goal: in a shared folder, users must not delete each other’s files.

5.1 Make the folder open to everyone (this creates the problem).

bash
chmod 777 /srv/lab/dropbox

What it does: 777 gives everyone read, write and execute on the folder. With write on a folder, anyone can delete anything inside it.

5.2 Alice creates a file.

bash
su - alice -c 'touch /srv/lab/dropbox/alice.txt'

What it does: touch creates an empty file.

5.3 Bob deletes it.

bash
su - bob -c 'rm /srv/lab/dropbox/alice.txt'

What it does: rm removes a file. It works, which is the problem: bob deleted alice’s file.

5.4 Confirm it’s gone.

bash
ls /srv/lab/dropbox

What it does: Lists the folder. Expected: empty.

5.5 Fix: add the sticky bit.

bash
chmod 1777 /srv/lab/dropbox

What it does: Everyone still has full access, but the leading 1 is the sticky bit: only a file’s owner (or root) can delete or rename it.

5.6 Alice creates the file again.

bash
su - alice -c 'touch /srv/lab/dropbox/alice.txt'

What it does: Same as 5.2.

5.7 Bob tries to delete it again.

bash
su - bob -c 'rm /srv/lab/dropbox/alice.txt'

What it does: Same as 5.3. Expected: Operation not permitted.

5.8 Check the folder.

bash
ls -ld /srv/lab/dropbox

What it does: Shows the folder’s permissions. Expected: drwxrwxrwt. The t is the sticky bit.
