""" Demonstration of how to use passcode:

  1. When you install passcode, there is no passcode.key file. Therefore, the first time you
     call passcode.update() the code will prompt you to make your own passphrase for this demonstration.

  2. We define a few private variables and private functions in the file secrets.py

  5. The example below imports `passcode` and then uses passcode.update() to
     - encrypt the file secrets.py into example_private_code.rc4
     - import the module into the local scope so it can then be accessed as normal.

"""

# Encrypt, decrypt, and import your private code file into the local namespace
import passcode
passcode.execute('secrets', scope=locals(), key_dev='./demo.key', key_run='./demo.key')


# Uncomment the below to enable code completion/inspection in your development IDE
#try: from secrets import *
#except: pass  # trap errors that arise due to missing source files in production


# Demonstrate that we can now access the secret variables and functions
print()
print('Secret variables and functions:')
print()
print('\t', 'SQL password:  ', SQL_PASSWORD)        # Print the value of an encrypted variable
print('\t', 'Emergency SMS: ', EMERGENCY_SMS)       # Print the value of an encrypted variable
print('\t', 'Golden Ratio:  ', golden_ratio())      # Run an encrypted function


# Print out what is now in the local scope
print()
print('The following are now in Locals:')
print()
for item in dir():
    if not str(item).startswith('__'):
        print('\t', item)
