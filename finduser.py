import pwd

# need to stip the newline
with open('badusers.txt', 'r') as f:
    lines = f.read().splitlines()


def finduser(user):
    try:
        if pwd.getpwnam(user):
            print user, "user exists"
            return True
            return False
    except:
        print user, "doesnt exist"

for i in lines:
    finduser(i)
