# Overview

Use `passcode` to pass python code through a git repository in encrypted form.  

`passcode` is useful when you want to include secrets (such as proprietary code or a login password) in a public 
repository, and you do not want others to have access to that information. `passcode` encrypts the protected 
code with a private passphrase, which you can then deploy from your development machine  into production by a more 
secure means (for example, by accessing the passphrase from an access-controlled metadata server, or by simply
installing the key in a protected directory within a Docker container).

`passcode`  is written in pure Python 3.X, has no dependencies, and requires two lines of code to implement.


## Install

Install with pip

    pip install passcode

Or copy `passcode.py` into your project.


## Use
  
    import passcode
    exec(passcode.import_export('private_settings', '~/passcode.key', '/private/passcode.key')) 


## Instructions  (step-by-step)

  1. Install passcode.
     
     * `pip install passcode` into your environment  
       
     *  or copy `passcode.py` into your project folder.


  2. Create a passphrase.
     
     * Generate an ASCII passphrase and save it into a file (by default, `passcode.key`).
    
     * If no key file exists, `passcode` will prompt you to enter one and will then save it to `passcode.key`.
     
     * You can use different keys for different modules, to enforce differential access-control.
       

  3. Import passcode and private modules:
      
     * The following code first imports passcode
     * Then the code uses the `passcode.import_export()` function to encrypt, decrypt, and import modules.
     * The original source code will be imported into the `local` scope.
     * After running `import_export()` you can reference variables and functions from the indicated modules as normal.

    import passcode 
    exec(passcode.import_export('private_settings', '~/passcode1.key', '/private/passcode1.key')) 
    exec(passcode.import_export('private_functions', '~/passcode2.key', '/private/passcode2.key')) 

  
  4. Exclude the original plaintext files (that you want to secure) from the repository. 
     
     * You do not want the passphrase file(s, or the unencrypted module(s) that you want to protect, to appear in your 
       git repository as plaintext. Therefore do not `git add` those file(s) to the repository. 
       
     * Alternatively, you can list those files for exclusion in the `.gitignore` file.


  5. Include only the encrypted versions of the protected modules in the repository.
     
   `git add *.rc4`  


  6. Re-run `import_export()` each time you change a protected module.
     
     * `passcode.import_export()` will refresh the encrypted copy of a module each time it is run.
       
     * Therefore re-run `import_export()` each time you change a protected source fie.
       

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

    try: from privatesettings import *   
    except: pass  #  missing source files will raise an error on the production machine, so catch it

    try: from privatemethods import *   
    except: pass  
  
  
  10. OPTIONAL: Recover an original source file (if all you have is the rc4 file)  
 
   * You can run `passcode.recover_source()` to recover the source *.py file if you have an encrypted *.rc4 file and 
     the appropriate key file.


## Example

See the file `example_demonstration.py` for a complete example of how to use `passcode`.


## Tech notes 
 
#### Trust in the production environment

The purpose of `passcode` is to protect secrets while in transit through a git repository. It does NOT necessarily 
protect secrets in the production environment. Although you can save passcode keys in a protected folder of the
production environment that most users cannot access, it could be possible for someone with access to the machine to 
re-write the application to stop, instpect, and dump out the secrets during runtime (of that person had access to the
machine and runtime in order to do so.) We are open to ideas about how to make the runtime production side more secure,
but `passcode` has generally served it's purpose of keeping secrets out of git repos.

#### RC4 Encryption
  
Encryption is implemented with the "alleged" RC4 algorithm. Although RC4 is not as secure as AES, it is simple, it is 
fast, it is implemented in pure python, and it has no imports. Another advantage of RC4 is that you can easily inspect 
our code and confirm what it does. A more advanced algorithm could require dependencies and/or a more complicated 
installation and distribution. You can implement `passcode` by doing nothing more than just copying the `passcode.py` 
file into your project directory.

There is some concern that RC4 might be breakable under certain conditions -- such as a 'man-in-the-middle' attack over 
a very large volume of encrypted traffic. We presume, however, that you will use `passcode` to encrypt only a handful of 
python files, and that those files will change infrequently. As such, you should not generate the millions (or even 
billions) of examples that are needed for a statistical attack. 

#### WARNING

Be sure to set your own passphrase in your own password files. In general, it is better to NOT use the default file 
`passcode.key` file, but rather to generate and name your own file.  


## Version History

Version 2.00 - February 6, 2021 - Python 3.x

  * Renamed from `Security` to `passcode`
  * Updated for Python 3.x
  * Decryption stage now returns a compiled code module, allowing for multiline functions and other code.
  * Readme changed to highlight how to use `passcode` to keep secrets out of your git repository.

Version 1.03 - January 31, 2015 - Python 2.7

  * Restructured the `import` procedure to silently encrypt/decrypt everything with a call to `security.secure()`.

Version 1.00 - January 20, 2015 - Python 2.7 

  * Initial release (named `Security`) for Python 2.7.


## Issues & Bugs

  * It is best to terminate the modules that you aim to encrypt with at least one newline character. This is to 
    facilitate detection of incomplete and complete statements in the code module.
    
  * There are some reports of the compile() function failing to parse code due to whitespace within in. TBD.


## Disclaimer

We use this code to protect simple secrets from general dissemination through our lab. It works well for us. I am 
posting it here for others to use as a *_pay-it-forward_* to the opensource community, be we provide *no support*, and 
we provide *no guarantees* about the security, safety, or appriateness of this package. 
*USE THIS CODE AT YOUR OWN RISK*.
 
