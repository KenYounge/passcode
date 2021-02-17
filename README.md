# Overview

Use `passcode` to encrypt python modules on your development machine, pass the unreadable code through an open git 
repository, pull the code into production, automatically decrypt the modules on the other end, and run/reference the 
code in production. Do all of that automatically, with just two lines of code.

`passcode` makes it possible to include secrets (such as a login password or some proprietary code) directly in your
code without others being able to read it in a push-to-deploy repository. 

`passcode`  is written in pure Python 3.X, has no dependencies, and requires two lines of code to implement. You can
easily inspect and verify the operation of `passcode` to see what it does. 


## Install

Install with `pip`  

    pip install passcode
    
Or simply copy `passcode/` directory into your project  

## Use
  
    import passcode
    passcode.execute('secrets', locals(), '~/mypasscode.key', '/private/mypasscode.key')


## Instructions  (step-by-step)

  1. Install passcode.
     
    pip install passcode
       

  2. Create a passphrase.
     
     * First option is to generate an ASCII passphrase manually and to thebn save it into a file, such as `passcode.key`
    
     * Second option is to leave the `key_dev` parameter blank, and `passcode` will prompt you for a passcode.
     
     * You can use different keys for different code modules, thereby enforcing differential access-control.
       

  3. Import passcode and private modules:
      
     * The following code uses the `passcode.update()` function to encrypt, decrypt, and import code modules.
     * The original source code is imported into local scope and you can reference variables and functions as normal.

    import passcode 
    passcode.execute('secrets1', locals(), '~/passphrase1.key', '/private/passphrase1.key')
    passcode.execute('secrets1', locals(), '~/passphrase2.key', '/private/passphrase2.key')

  
  4. Exclude the original plaintext files (that you want to secure) from the repository. 
     
     * You do not want the passphrase file(s, or the unencrypted module(s) that you want to protect, to appear in your 
       git repository as plaintext. Therefore do not `git add` those file(s) to the repository. 
       
     * Alternatively, you can list those files for exclusion in the `.gitignore` file.


  5. Include only the encrypted versions of the protected modules in the repository: `git add *.rc4`  


  6. Re-run `passcode.execute()` each time you change a passcode protected module.
     
     * `passcode.execute()` will refresh the encrypted copy of a module each time it is executed.
       
     * Therefore re-run `execute()` each time you change a protected source fie.
       

  7. Push your project to the repository. 
    
     * Configure `.gitignore` to exclude your secret module(s) and your secret password key(s) from the repository.
       
     * And/or make sure that you do not add those files to the repository in the first place.


  8. Deploy keys independently (and privately) to production. 

     * You need to distribute your private keys to production by another, more-protected approach:
       
       - move the password key(s) to a more secure git repository with limited access by others;
         
       - install the password key(s) into a protected directory in a Docker Container or a VM Image;
         
       - manually copy the password key(s) to the production machine.

  
  9. OPTIONAL: Enable code completion for the development IDE. 
     
     * IDEs will autocomplete and check for some errors when they can reference original code declarations. 
       
     * The IDE cannot do that, however, if it cannot find a normal Python import statement to reference.
       
     * The following code will enable code completion & inspection on the dev-side IDE. 
       
     * Note that the code will raise an error on a production machine (because the imports will be missing), 
       so you must catch each error (independently) for each import. 

    try: from private_code import *   
    except: pass   

    try: from another_module import *   
    except: pass  
  
  
  10. OPTIONAL: Recover an original source file from an rc4 file.
 
   * Your original source code is still backed up and protected in the git repository - just not in plain text.
   
   * You can recover the original source code (*.py) file from an encrypted *.rc4 file if you have the original key.

   * Run `passcode.recover()` to recover the original, unencrypted file.


## Disclaimer

*USE THIS CODE AT YOUR OWN RISK*. I provide *no guarantee* about it's security, safety, reliability, or any other 
potential risk or harm. 
 

## Demonstration

See the file `demonstration.py` for an example of how to use `passcode`.


## Tech notes 
 

#### The production environment

The purpose of `passcode` is to protect secrets while in transit through a git repository. It does NOT protect secrets 
in the production environment. Although you can save passcode keys in an access-protected directory of the production 
environment (i.e., separate from the running code) that others cannot access, it may be possible for others to access 
the decryopted code during runtime by re-writing the application to stop, inspect, and dump out the secret code 
(although they also would have to have permission to change the runtime code in the production environment). This is a 
limitation of this apporoach. We are open to suggestions from others about ways to strength the last-stage of security
with other "bring your own encryption key" steps that could be combined with `passcode`.


#### RC4 Encryption
  
Encryption is implemented with the "alleged" RC4 algorithm. Although RC4 is not as secure as AES, it is simple, it is 
fast, it is implemented in pure python, and it has no imports. Another advantage of RC4 is that you can easily inspect 
our code and confirm what it does. A more advanced algorithm would require dependencies and a more complicated 
installation/distribution. You can implement `passcode` by doing nothing more than just copying `passcode.py` into
your project.

There is some concern that RC4 is breakable through a 'man-in-the-middle' attack over a very large volume of encrypted 
traffic. We presume, however, that you will use `passcode` to encrypt only a handful of python files, and that those 
files change infrequently. As such, you should not generate the millions (or billions) of examples that are needed for 
a statistical attack. 


#### Set your own passphrase

Be sure to set your own passphrase in your own password files. In general, it is better to NOT use the file name
`passcode.key` (the default assumed by `passcode.update()`), but rather generate and name your own file. A 
random file name for your key would also seem to reduce the chance of mistakenly using a key file from somone else. 


## Version History

#### Version 0.1.4  -  2021.02.17

  Moved implementation into a `__init__.py` file so user an import it directly as a directory.
  Changed naming of the implementation methods.
  Fixed bug in RC4 which would break on some unicode characters.

#### Version 0.1.2  -  2021.02.11

  Renamed the example files.

#### Version 0.1.1  -  2021.02.10

  Improved the ReadMe.

#### Version 0.1.0  -  2021.02.09

  First distribution to PyPi.


## OPEN BUG REPORTS

  * Terminate modules (that you aim to encrypt) with at least one newline character. This helps python to distinguish 
    complete vs. incomplete statements in the code module.
    
  * There are reports of the python `compile()` function failing to parse some types of code due to whitespace in it. 
    This is being investigated.

  * There are reports of the our encrypt/decrypt sequence, plus the python `compile()` function, dropping an apostrophe 
    (i.e., the ' character) - switching to double quotes seemd to fix the problem for some reason in the known case.  
    This is being investigated.


