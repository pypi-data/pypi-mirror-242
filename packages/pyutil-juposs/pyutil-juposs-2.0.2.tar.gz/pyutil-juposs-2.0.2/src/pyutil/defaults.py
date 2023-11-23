ldap = {
    "server": "example.org",
    "search_attribute": "userPrincipalName",
    "dn": "OU=OrgUnit,DC=example,DC=org",
    "return_attributes": ["lastlogon"],
}

mail = {
    "from_email": "no-reply@example.org",
    "server": "mailserver.example.org",
    "port": 587,
    "username": "no-reply@example.org",
    "password": None,
    "filepath": None,
}

logger = {
    "logfile_path": "$HOME",
    "logfile_name": "pyutil.log",
    "maxBytes": 0,
    "backupCount": 10,
}

mysql: {
  "host": "localhost",
  "username": "yourusername",
  "password": "yourpassword",
  "database": "mydatabase"
}