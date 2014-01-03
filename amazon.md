Using Amazon's EC2
=================
Amazon's services can be used to start a txtorg server, upload your data, and index your text for a low rate.  Depending on the size the data you need to index, you will need a larger server.

Pricing is as follows:

As long as your machine is running, you will be charged.  If you terminate your instance, you will no longer be charged.

For roughly $1/hour, you can use a computer with 30gb of memory and 8 cores.  It is possible to pay as little as $.02/hour, or as much as $4.60/hour, depending on the system size required.  Pricing and usage tiers are complicated, so please make sure you understand how you will be charged before signing up.  You will also be charged for any disk space you use, at a rate of $.10/Gb/Month.

Amazon Server Setup
-------------------
Follow these instructions to set up `txtorg` on Amazon's EC2.

1.  Make an Amazon Web Services Account
    *  Sign up here: https://portal.aws.amazon.com/gp/aws/developer/registration/index.html
2.  Make an EC2 Instance
    1. Go to the Amazon EC2 Portal: https://console.aws.amazon.com/ec2
    2. Click "Launch Instance"
    3. Click "Continue" to use the Classic Wizard
    4. Select the Ubuntu Server 13.04 64 bit instance.  This is available for the Free Tier for beginning EC2 users.
    5. Click "Continue" to launch the instance with the default availability zone and the instance size that is required for your data.
    6. Click "Continue" to accept the default advanced instance options.
    7. Click "Continue" to accept the default Storage Device Configuration
    8. Add a tag called Name (this is already filled in) with the Value "txtorg" (or anything else you can recognize)
    9. Click on "Create a new Key Pair" and enter a name.
	* Click on Create and Download your key pair
	* Click Continue
   10. Click on "Create a new Security Group"
	* Click on the dropbox to create a new rule and select SSH. Click Add Rule.
	* Click Continue
   11. Click "Launch", then Click "Close"
   12. Your instance will now be running!  Click on "txtorg" (or whatever you called your instance) and write down its IP address.  This will look something like `ec2-23-21-28-85.compute-1.amazonaws.com`
3.  SSH to your Amazon Instance.
    * *Note:* The username for this instance will be `ubuntu`
    * Windows users, please use these instructions: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html
    * Mac users, open a Terminal and type the following:
	* `chmod 700 ~/Downloads/<your key name>.pem`
	* `ssh -iX ~/Downloads/<your key name>.pem ubuntu@<your-ip-address>`
	* *Note:* My key is saved in the `~/Downloads` folder - yours may be somewhere else!
4.  Install the dependencies on your server by typing the following.
    * `sudo apt-get install git python-tk pylucene python-setuptools`    
5.  Clone this git repository
    * `git clone https://github.com/sbrother/iqss-text-organizer.git`
6.  Install the software
    * `cd iqss-text-organizer`
    * `sudo python setup.py install`

To run txtorg
---------------
The software can be run from your amazon terminal at any time by logging on (see #3) and typing `txtorg` to open the GUI.

To update txtorg
----------------

Once txtorg is installed, you should update it by logging in to you amazon machine (see #3 from above) and typing the following:

`cd iqss-text-organizer`

`git pull`

`python setup.py install --user`
