"""Encrypt python files for posting to a git repository. Later, import code back into global namespace."""
from os.path import exists as path_exists

# Local constants
DOT_PY = '.py'
DOT_RC4 = '.rc4'

def __crypt(data, key):
    """The alleged RC4 encryption method."""
    x = 0
    box = [i for i in range(256)]
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    return ''.join(out)

def import_export(name, scope, key_dev='passcode.key', key_run='passcode.key'):
    """Encrypt and decrypt a python module.

    Args:
        name:     name of a python module to encrypt/decrypt (without the file ending of .py)
        scope:    scope in which to execute the module --- typically globals() or locals()
        key_dev:  path and name of file containing password on dev machine; otherwise, a string password
        key_run:  path and name of file containing password on runtime production machine; otherwise, a string password

    Returns:
        AST code object    The return object can then be executed with the python exec() function
    """

    # Validate
    assert name, 'passcode.import_export() error: No module name'
    assert scope, 'passcode.import_export() error: No scope'
    assert key_dev or key_run, 'passcode.import_export() error: No filename for a dev or production key'

    # Make random passcode if none exists on either dev side or production side
    if not path_exists(key_dev) and not path_exists(key_run):
        key = input('Passphrase: ', )
        assert key, 'passcode.import_export() error: No passphrase entered'
        with open(key_dev, 'w') as f_pwd_dev:
            f_pwd_dev.write(key)

    # Encrypt
    if path_exists(name + DOT_PY):
        if path_exists(key_dev):
            key = open(key_dev, 'r').read()
        else:
            key = str(key_dev)
        with open(name + DOT_PY, 'r') as f_in:
            with open(name + DOT_RC4, 'w') as f_out:
                f_out.write(__crypt(f_in.read(), key))

    # Validate
    assert path_exists(name + DOT_RC4), 'passcode.import_export() error: missing encrypted file - ' + name
    assert path_exists(key_dev) or path_exists(key_run), 'passcode.import_export() error: no key'

    # Decrypt
    if path_exists(key_dev):
        key = open(key_dev, 'r').read()
    else:
        key = open(key_run, 'r').read()
    with open(name + DOT_RC4, 'r') as f:
        code = __crypt(str(f.read()), key)

    # Compile and execute code
    exec(compile(code, name, 'exec'), scope)


def recover_source(name, key_dev='passcode.key'):

    assert not path_exists(name + DOT_PY), 'passcode.recover_source() error: source file already exists'
    assert path_exists(name + DOT_RC4), 'passcode.recover_source() error: encrypted source file does not exist'
    assert path_exists(key_dev), 'passcode.recover_source() error: no key'

    # Decrypt
    key = open(key_dev, 'r').read()
    with open(name + DOT_RC4, 'r') as f:
        code = __crypt(str(f.read()), key)

    # Save
    with open(name + DOT_RC4, 'w') as f:
        f.write(__crypt(code, key))
