""" Demonstration of how to use passcode:

  1. When you install passcode, there is no passcode.key file. Therefore, the first time you
     call passcode.import_export() the code will prompt you to make your own passphrase for this demonstration.

  2. We define a few private variables and private functions in the file example_private_code.py

  5. The example below imports `passcode` and then uses passcode.import_export() to
     - encrypt the file example_private_code.py into example_private_code.rc4
     - import the module into the local scope so it can then be accessed as normal.

"""

# Encrypt, decrypt, and import your private code file into the local namespace
import passcode
passcode.import_export('example_private_code', locals())


# Uncomment the below to enable code completion/inspection in your development IDE
# try: from example_private_code import *
# except: pass  # trap errors that arise due to missing source files in production


# Demonstrate that we can now access the privat variables and functions
print()
print('Private variables:')
print('\t', 'SQL password:  ', SQL_PASSWORD)        # Print the value of an encrypted variable
print('\t', 'Emergency SMS: ', EMERGENCY_SMS)       # Print the value of an encrypted variable
print()
print('Private functions:')
print('\t', 'Golden Ratio:  ', golden_ratio())      # Run an encrypted function
print('\t', 'My Timestamp:  ', timestamp_uuid())    # Run an encrypted function
print()


# Note that the imports are now in locals() scope
print('Local scope:')
for item in dir():
    if not str(item).startswith('__'):
        print('\t', item)
