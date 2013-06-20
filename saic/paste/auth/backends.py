from django.contrib.auth.backends import RemoteUserBackend

import json, urllib

def _get_ldap_users():
    res = {}
    users = json.loads(urllib.urlopen("http://esgdataweb.intra.gsacapital.com:64469/esgdata/users/users.json", proxies={}).read())
    for u in users:
        pn = u.get("userPrincipalName")
        if pn and "@" in pn:
            res[pn.lower()] = u
    return res

class CustomHeaderBackend(RemoteUserBackend):
    def clean_username(self, username):
        return username.lower()
    
    def configure_user(self, user):
        print "config user", user.username
        u = _get_ldap_users().get(user.username)
        print _get_ldap_users().keys()
        print u
        if u is not None and 'mail' in u:
            print "Setting email to ", u['mail']
            user.email = u['mail'] 
        return user
 
    def authenticate(self, remote_user):
        print "auth", remote_user
        u = _get_ldap_users().get(remote_user.lower())
        if u is None:
            print "not found"
            return None
        else:
            print u
            return RemoteUserBackend.authenticate(self, remote_user)
