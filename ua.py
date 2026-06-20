import email_normalize

def is_valid(email): # multiple function calls at same time

    # Preprocessing
    ##################################################################

    if not isinstance(email, str):
        return False

    # Strip
    email = email.strip()

    #Normalise
    email = email_normalize(email)

    


    #Validation
###############################################################

    # Error checking
    if not email:
        return False

    if not _is_utf8_text(email) or len(email.encode("utf-8")) > 254:
        return False

    # Split
    parts = _split_address(email)
    if parts is None:
        return False
    if (email.count != 1):
        return False


    #Split
    parts = email.split()
    local, domain = parts[0], parts[1]

    #Handle Local Section
    

    #Handle Domain section
    if (domain.length() > 255 or domain.length() < 1) or domain.endswith('.') or domain.count("..") > 0:
        return False
    

    #IDNA Conversion
    idn = domain.encode('idna')



    return True


