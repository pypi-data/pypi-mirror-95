# Syst3m
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: ubuntu.
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"/>
</p>

## WARNING!
THIS REPO IS UNSTABLE AND UNDER DEVELOPMENT.

## Installation
	pip3 install syst3m --upgrade && python3 -c "import syst3m" --create-alias


## CLI:
The syst3m cli tool.

	Usage: syst3m <mode> <options> 
	Modes:
	    --user myuser : Configure a system user (linux).
	        --check : Check the existance of the specified group.
	        --create : Create the specified group.
	        --delete : Delete the specified group.
	        --password MyPassword : Set the password of the specifed user (leave password blank for safe prompt).
	        --add-groups group1,group2 : Add the specified user to groups.
	        --delete-groups group1,group2 : Remove the specified user from groups.
	    --group mygroup : Configure a system group (linux).
	        --list-users : List the users of the specified group.
	        --add-users user1,user2 : Add users from the specified group.
	        --delete-users user1,user2 : Delete users from the specified group.
	        --force-users user1,user2 : Add the specified users to the group and remove all others.
	    -h / --help : Show the documentation.
	Options:
	    -c : Do not clear the logs.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2020. All rights reserved.


## Python Examples.

### The syst3m.cache.Cache object class.
the system.cache.Cache() object class.
```python

# imports.
import cl1, syst3m

# initialize the webserver.
cache = syst3m.cache.Cache(path=f"{HOME}/.{ALIAS}/.cache/",)

# get data.
response = cache.get(group="passphrases", id="master")

# set data.
response = cache.set(group="passphrases", id="master", data=...)
			

```

### The syst3m.cache.WebServer object class.
the system.cache.WebServer() object class.
```python

# imports.
import cl1, syst3m

# initialize the webserver.
webserver = syst3m.cache.WebServer(serialized={
	"id":f"{ALIAS}-webserver",
	"path":f"{HOME}/.{ALIAS}/.cache/",
	"host":"127.0.0.1",
	"default":{},
	"port":52379,
})

# automatically fork & stop.
if cl1.argument_present(f"--stop-{ALIAS}-webserver"):
	response = webserver.stop()
elif not webserver.running(): 
	response = webserver.fork()
	r3sponse.log(response=response, json=JSON)
	if not response.success: sys.exit(0)

# get data.
response = webserver.get(group="passphrases", id="master")

# set data.
response = webserver.set(group="passphrases", id="master", data=...)
			

```

### The User() object class.
The User() object class. 
```python

# import the package.
import syst3m

# initialize a user object.
user = syst3m.User("testuser")

# check if the user exists.
response = user.check()
if response["success"]: print("User existance:",response["exists"])

# create a user.
response = user.create()

# delete a user.
response = user.delete()

# set a users password.
response = user.set_password(password="Doeman12!")

# add the user to groups.
response = user.add_groups(groups=[])

# delete the user from groups.
response = user.add_groups(groups=[])

```


### The Group() object class.
The Group() object class. 
```python

# import the package.
import syst3m

# initialize a group object.
group = syst3m.Group("testgroup")

# check if the group exists.
response = group.check()
if response["success"]: print("Group existance:",response["exists"])

# create a group.
response = group.create()

# delete a group.
response = group.delete()

# list the current users.
response = group.list_users()
if response["success"]: print(f"Users of group {group.name}:",response["users"])

# add users to the group.
response = group.add_users(users=["testuser"])

# delete users from the group.
response = group.delete_users(users=["testuser"])

# check if the specified users are enabled and remove all other users.
response = group.check_users(users=["testuser"])


```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}