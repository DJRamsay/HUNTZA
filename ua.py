import unicodedata


ASCII_ATEXT = frozenset(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "!#$%&'*+-/=?^_`{|}~"
)


def _is_utf8_text(value):
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_control_or_surrogate(character):
    return unicodedata.category(character) in {"Cc", "Cs"}


def _split_address(email):
    at_index = None
    escaped = False
    in_quote = False

    for index, character in enumerate(email):
        if escaped:
            escaped = False
            continue

        if in_quote and character == "\\":
            escaped = True
            continue

        if character == '"':
            in_quote = not in_quote
            continue

        if character == "@" and not in_quote:
            if at_index is not None:
                return None
            at_index = index

    if escaped or in_quote or at_index is None:
        return None

    return email[:at_index], email[at_index + 1:]


def _is_valid_quoted_local(local):
    if len(local) < 2 or local[0] != '"' or local[-1] != '"':
        return False

    escaped = False
    for character in local[1:-1]:
        if escaped:
            if character in "\r\n" or _is_control_or_surrogate(character):
                return False
            escaped = False
            continue

        if character == "\\":
            escaped = True
            continue

        if character == '"' or character in "\r\n":
            return False

        if _is_control_or_surrogate(character):
            return False

    return not escaped


def _is_valid_unquoted_local(local):
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False

    for character in local:
        if character == ".":
            continue

        if ord(character) < 128:
            if character not in ASCII_ATEXT:
                return False
            continue

        if _is_control_or_surrogate(character):
            return False

        if unicodedata.category(character).startswith("Z"):
            return False

        if not _is_utf8_text(character):
            return False

    return True


def _is_valid_local(local):
    if not local:
        return False

    if not _is_utf8_text(local) or len(local.encode("utf-8")) > 64:
        return False

    if local.startswith('"') or local.endswith('"'):
        return _is_valid_quoted_local(local)

    if '"' in local or "\\" in local:
        return False

    return _is_valid_unquoted_local(local)


def _is_valid_domain(domain):
    if not domain or domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False

    if "." not in domain:
        return False

    try:
        ascii_domain = domain.encode("idna")
    except UnicodeError:
        return False

    if len(ascii_domain) > 255:
        return False

    for label in ascii_domain.decode("ascii").split("."):
        if not label or len(label) > 63:
            return False

        if label.startswith("-") or label.endswith("-"):
            return False

        if any(not (character.isalnum() or character == "-") for character in label):
            return False

    return True


def is_valid(email):  # multiple function calls at same time

    # Preprocessing
    ##################################################################

    if not isinstance(email, str):
        return False

    # Strip
    email = email.strip()

    # Normalise
    email = unicodedata.normalize("NFC", email)

    # Validation
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

    local, domain = parts

    # Handle Local Section
    if not _is_valid_local(local):
        return False

    # Handle Domain section
    if not _is_valid_domain(domain):
        return False

    return True
