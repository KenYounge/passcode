"""Encrypt modules to pass private code through a repository."""
__module__ = 'passcode'
__author__ = "Kenneth A Younge"
__copyright__ = "Copyright (c) 2021, Kenneth A. Younge"
__license__ = "MIT License"
__email__ = "kenyounge@gmail.com"

import io
from os.path import exists as path_exists

def __crypt(text, keyphrase):
    """ The alleged RC4 encryption method. """

    assert len(keyphrase) > 8, 'INVALID ENCRYPTION KEY: Provide a passphrase of at least 8 characters.'

    msg_chars = sorted(list({c for c in text}))

    # Detect incoming encrypted text when it is all zeros and ones (do not use to encrypt messages of just zeros ones).
    reverse = bool(msg_chars == ['0', '1'])
    if reverse:
        num_message = [int(text[i:i + 8], 2) for i in range(0, len(text), 8)]
    else:
        num_message = [ord(c) for c in text]

    j = 0
    box = [i for i in range(256)]
    for i in range(256):
        j = (j + box[i] + ord(keyphrase[i % len(keyphrase)])) % 256
        box[i], box[j] = box[j], box[i]
    j = 0
    i = 0
    stream = []
    for _ in text:
        j = (j + 1) % 256
        i = (i + box[j]) % 256
        box[j], box[i] = box[i], box[j]
        addon = (box[i] + box[j]) % 256
        stream.append(box[addon])

    if reverse:
        out = ''.join(chr(i ^ j) for i, j in zip(num_message, stream))
    else:
        out = ''.join(['{:08b}'.format(i ^ j) for i, j in zip(num_message, stream)])

    return out


def execute(module, scope, key_dev, key_run):
    """
    Encrypt and decrypt a python module.

    Args:
        module:    name of python module (without .py suffix) to encrypt and/or decrypt
        scope:     scope in which to execute module --- typically globals() or locals()
        key_dev:   path and name of file with passphrase on dev machine
        key_run:   path and name of file with passphrase on production machine
    """

    # Validate
    assert module,             'ERROR in passcode.execute(): No module'
    assert scope,              'ERROR in passcode.execute(): No scope'
    assert key_dev or key_run, 'ERROR in passcode.execute(): No key (for either dev or production)'

    # Input passphrase if none given
    if not path_exists(key_dev) and not path_exists(key_run):
        key = input('Passphrase: ', )
        assert key, 'ERROR in passcode.execute(): No passphrase entered by user'
        with io.open(key_dev, 'w', encoding='utf8') as f_pwd_dev:
            f_pwd_dev.write(key)

    # Encrypt
    if path_exists(module + '.py'):
        key = io.open(key_dev, 'r', encoding='utf8').read()
        with io.open(module + '.py', 'r', encoding='utf8') as f_in:
            with io.open(module + '.rc4', 'w', encoding='utf8') as f_out:
                f_out.write(__crypt(f_in.read(), key))

    # Validate
    assert path_exists(module + '.rc4'),                'ERROR in passcode.execute(): Missing file ' + module + '.rc4'
    assert path_exists(key_dev) or path_exists(key_run), 'ERROR in passcode.execute(): No key'

    # Decrypt
    if path_exists(key_run):
        key = io.open(key_run, 'r', encoding='utf8').read()
    else:
        key = io.open(key_run, 'r', encoding='utf8').read()
    with io.open(module + '.rc4', 'r', encoding='utf8') as f:
        code = __crypt(str(f.read()), key)

    # Execute compiled code
    exec(compile(code, module, 'exec'), scope)


def recover(module, key):

    assert path_exists(module + '.rc4'),     'ERROR in passcode.recover(): Encrypted module file does not exist'
    assert not path_exists(module + '.py'),  'ERROR in passcode.recover(): Unencrypted module file already exists'
    assert path_exists(key),                 'ERROR in passcode.recover(): No key'

    # Decrypt
    key = io.open(key, 'r', encoding='utf8').read()
    with io.open(module + '.rc4', 'r', encoding='utf8') as f:
        code = __crypt(str(f.read()), key)

    # Save
    with io.open(module + '.rc4', 'w', encoding='utf8') as f:
        f.write(__crypt(code, key))
