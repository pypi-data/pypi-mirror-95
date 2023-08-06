=====
LDEEP
=====

Help is self-explanatory. Let's check it out::

  $ ldeep -h                                                             
  usage: ldeep [-h] [-o OUTFILE] {ldap,cache} ...

  optional arguments:
      -h, --help            show this help message and exit
      -o OUTFILE, --outfile OUTFILE
                        Store the results in a file
      --security_desc   Enable the retrieval of security descriptors in ldeep
                        results

			
  Modes:
      Available modes

      {ldap,cache}          Mode to query


Ldeep can either run against an Active Directory LDAP server or locally on saved files::

  $ ldeep ldap -u Administrator -p 'password' -d winlab -s ldap://10.0.0.1 all backup/winlab
  [+] Retrieving computers output
  [+] Retrieving domain_policy output
  [+] Retrieving gpo output
  [+] Retrieving groups output
  [+] Retrieving groups verbose output
  [+] Retrieving machines output
  [+] Retrieving machines verbose output
  [+] Retrieving ou output
  [+] Retrieving pso output
  [+] Retrieving trusts output
  [+] Retrieving users output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving users verbose output
  [+] Retrieving zones output
  [+] Retrieving zones verbose output

  $ ldeep cache -d backup -p winlab users
  Administrator
  [...]

These two modes have different options:

LDAP
----

::

   $ ldeep ldap -h                                                        
   usage: ldeep ldap [-h] [-d DOMAIN] [-s LDAPSERVER] [-b BASE]
                           [-u USERNAME] [-p PASSWORD] [-k] [-a]
                           {computers,domain_policy,gpo,groups,machines,ou,pso,trusts,users,zones,from_guid,from_sid,memberships,membersof,object,sddl,zone,all,search,modify_password,unlock}
                           ...

   optional arguments:
       -h, --help            show this help message and exit
       -d DOMAIN, --domain DOMAIN
                             The domain as NetBIOS or FQDN
       -s LDAPSERVER, --ldapserver LDAPSERVER
                             The LDAP path (ex : ldap://corp.contoso.com:389)
       -b BASE, --base BASE  LDAP base for query (by default, this value is pulled
                             from remote Ldap)

   NTLM authentication:
       -u USERNAME, --username USERNAME
                             The username
       -p PASSWORD, --password PASSWORD
                             The password or the corresponding NTLM hash

   Kerberos authentication:
       -k, --kerberos        For Kerberos authentication, ticket file should be
                             pointed by $KRB5NAME env variable

   Anonymous authentication:
   -a, --anonymous           Perform anonymous binds

   commands:
       available commands

       {computers,domain_policy,gpo,groups,machines,ou,pso,trusts,users,zones,from_guid,from_sid,memberships,membersof,object,sddl,zone,all,search,modify_password,unlock}
       computers           List the computer hostnames and resolve them if --resolve is specify.
       domain_policy       Return the domain policy.
       gpo                 Return the list of Group policy objects.
       groups              List the groups.
       machines            List the machine accounts.
       ou                  Return the list of organizational units with linked GPO.
       pso                 List the Password Settings Objects.
       trusts              List the domain's trust relationships.
       users               List users according to a filter.
       zones               List the DNS zones configured in the Active Directory.
       from_guid           Return the object associated with the given `guid`.
       from_sid            Return the object associated with the given `sid`.
       memberships         List the group for which `users` belongs to.    
       membersof           List the members of `group`.
       object              Return the records containing `object` in a CN.
       sddl                Returns the SDDL of an object given it's CN.
       zone                Return the records of a DNS zone.
       all                 Collect and store computers, domain_policy, zones, gpo, groups, ou, users, trusts, pso information
       search              Query the LDAP with `filter` and retrieve ALL or `attributes` if specified.
       modify_password     Change `user`'s password.
       unlock              Unlock `user`.

CACHE
-----

::
   
   usage: ldeep cache [-h] [-d DIR] -p PREFIX
                         {computers,domain_policy,gpo,groups,machines,ou,pso,trusts,users,zones,from_guid,from_sid,memberships,m                         embersof,object,sddl,zone}
                         ...

   optional arguments:
     -h, --help            show this help message and exit
     -d DIR, --dir DIR     Use saved JSON files in specified directory as cache
     -p PREFIX, --prefix PREFIX
                           Prefix of ldeep saved files
   
   commands:
     available commands
   
     {computers,domain_policy,gpo,groups,machines,ou,pso,trusts,users,zones,from_guid,from_sid,memberships,membersof,object,sddl,zone}
       computers           List the computer hostnames and resolve them if --resolve is specify.
       domain_policy       Return the domain policy.
       gpo                 Return the list of Group policy objects.
       groups              List the groups.
       machines            List the machine accounts.
       ou                  Return the list of organizational units with linked GPO.
       pso                 List the Password Settings Objects.
       trusts              List the domain's trust relationships.
       users               List users according to a filter.
       zones               List the DNS zones configured in the Active Directory.
       from_guid           Return the object associated with the given `guid`.
       from_sid            Return the object associated with the given `sid`.
       memberships         List the group for which `users` belongs to.
       membersof           List the members of `group`.
       object              Return the records containing `object` in a CN.
       sddl                Returns the SDDL of an object given it's CN.
       zone                Return the records of a DNS zone.
   
  

=======
INSTALL
=======

``ldeep`` is Python3 only.::

	pip3 install ldeep

=====
USAGE
=====

Listing users without verbosity::

	$ ldeep ldap -u Administrator -p 'password' -d winlab.local -s ldap://10.0.0.1 users
	userspn2
	userspn1
	gobobo
	test
	krbtgt
	DefaultAccount
	Guest
	Administrator


Listing users with reversible password encryption enable and with verbosity::

	$ ldeep ldap -u Administrator -p 'password' -d winlab.local -s ldap://10.0.0.1 users reversible -v
	[
	  {
	    "accountExpires": "9999-12-31T23:59:59.999999",
	    "badPasswordTime": "1601-01-01T00:00:00+00:00",
	    "badPwdCount": 0,
	    "cn": "User SPN1",
	    "codePage": 0,
	    "countryCode": 0,
	    "dSCorePropagationData": [
	      "1601-01-01T00:00:00+00:00"
	    ],
	    "displayName": "User SPN1",
	    "distinguishedName": "CN=User SPN1,CN=Users,DC=winlab,DC=local",
	    "dn": "CN=User SPN1,CN=Users,DC=winlab,DC=local",
	    "givenName": "User",
	    "instanceType": 4,
	    "lastLogoff": "1601-01-01T00:00:00+00:00",
	    "lastLogon": "1601-01-01T00:00:00+00:00",
	    "logonCount": 0,
	    "msDS-SupportedEncryptionTypes": 0,
	    "name": "User SPN1",
	    "objectCategory": "CN=Person,CN=Schema,CN=Configuration,DC=winlab,DC=local",
	    "objectClass": [
	      "top",
	      "person",
	      "organizationalPerson",
	      "user"
	    ],
	    "objectGUID": "{593cb08f-3cc5-431a-b3d7-9fbad4511b1e}",
	    "objectSid": "S-1-5-21-3640577749-2924176383-3866485758-1112",
	    "primaryGroupID": 513,
	    "pwdLastSet": "2018-10-13T12:19:30.099674+00:00",
	    "sAMAccountName": "userspn1",
	    "sAMAccountType": "SAM_GROUP_OBJECT | SAM_NON_SECURITY_GROUP_OBJECT | SAM_ALIAS_OBJECT | SAM_NON_SECURITY_ALIAS_OBJECT | SAM_USER_OBJECT | SAM_NORMAL_USER_ACCOUNT | SAM_MACHINE_ACCOUNT | SAM_TRUST_ACCOUNT | SAM_ACCOUNT_TYPE_MAX",
	    "servicePrincipalName": [
	      "HOST/blah"
	    ],
	    "sn": "SPN1",
	    "uSNChanged": 115207,
	    "uSNCreated": 24598,
	    "userAccountControl": "ENCRYPTED_TEXT_PWD_ALLOWED | NORMAL_ACCOUNT | DONT_REQ_PREAUTH",
	    "userPrincipalName": "userspn1@winlab.local",
	    "whenChanged": "2018-10-22T18:04:43+00:00",
	    "whenCreated": "2018-10-13T12:19:30+00:00"
	  }
	]

Listing GPOs::

	$ ldeep -u Administrator -p 'password' -d winlab.local -s ldap://10.0.0.1 gpo
	{6AC1786C-016F-11D2-945F-00C04fB984F9}: Default Domain Controllers Policy
	{31B2F340-016D-11D2-945F-00C04FB984F9}: Default Domain Policy

Getting all things::

	$ ldeep ldap -u Administrator -p 'password' -d winlab.local -s ldap://10.0.0.1 all /tmp/winlab.local_dump
	[+] Retrieving computers output
	[+] Retrieving domain_policy output
	[+] Retrieving gpo output
	[+] Retrieving groups output
	[+] Retrieving groups verbose output
	[+] Retrieving ou output
	[+] Retrieving pso output
	[+] Retrieving trusts output
	[+] Retrieving users output
	[+] Retrieving users verbose output
	[+] Retrieving zones output
	[+] Retrieving zones verbose output

Using this last command line switch, you have persistent output in both verbose and non-verbose mode saved::

	$ ls winlab.local_dump_*
	winlab.local_dump_computers.lst      winlab.local_dump_groups.json  winlab.local_dump_pso.lst     winlab.local_dump_users.lst
	winlab.local_dump_domain_policy.lst  winlab.local_dump_groups.lst   winlab.local_dump_trusts.lst  winlab.local_dump_zones.json
	winlab.local_dump_gpo.lst            winlab.local_dump_ou.lst       winlab.local_dump_users.json  winlab.local_dump_zones.lst

The the cache mode can be used to query some other information.

========
Upcoming
========

* Proper DNS zone enumeration
* Project tree
* Python package
* Useful Kerberos delegation information
* Any ideas?

================
Related projects
================

* https://github.com/SecureAuthCorp/impacket
* https://github.com/ropnop/windapsearch
* https://github.com/shellster/LDAPPER

