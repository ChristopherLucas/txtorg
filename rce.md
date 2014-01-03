Using txtorg on the RCE
=======================

If you are using NX Client
--------------------------

Begin by logging on to the RCE virtual machine that has pylucene installed.

Open your NX Client and connect to the following server:

`rce6-1.hmdc.harvard.edu`

Next click on Applications and then Terminal

If you are using the shell
--------------------------

Begin by logging on to the RCE virtual machine that has pylucene installed.  When you log in, make sure that you enable X-forwarding:

`ssh -X username@rce6-1.hmdc.harvard.edu`

Once you are on the RCE terminal
--------------------------------

Then, clone this very git repository by typing:

`git clone https://github.com/sbrother/iqss-text-organizer.git`

This should make a directory called `iqss-text-organizer`.  Enter this directory by typing the following:

`cd iqss-text-organizer`

Now, run the install script, but specifying that it should be installed only for this user (you do not have to change anything on the following line):

`python setup.py install --user`

In the `iqss-text-organizer/bin` directory there is an executable called `txtorg`.  

If you followed the instructions above, you are in the `iqss-text-organizer` directory and can run txtorg by pasting the following:

`./bin/txtorg`

From a new terminal, you should only need to type the following to run txtorg:

`./iqss-text-organizer/bin/txtorg`

This should open a new window with the txtorg GUI.

To update txtorg
----------------

Once txtorg is installed, you should update it by opening a new terminal, and typing the following commands.

`cd iqss-text-organizer`

`git pull`

`python setup.py install --user`

