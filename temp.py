
import re
import punycode
def is_valid(email): # multiple function calls at same time
    # Basic checks on email
    if (email.length() > 255) or (email.length() == 0):
        return False
    if (email.count != 1):
        return False


    #Split
    parts = email.split()
    local, domain = parts[0], parts[1]

    #Handle Local Section
    #Quoted Strings: "(),:;<>@[\] characters are allowed with restrictions (they are only allowed inside a quoted string
    if (local.length() > 64 or checkQuotedString(local) == False):
        return False


    #Handle Domain section
    if (domain.length() > 255 or domain.length() < 1) or domain.endswith('.') or domain.count("..") > 0:
        return False

    return True

def checkQuotedString(local):
    if (local.count('"') % 2 == 1):
        return False
    return True
