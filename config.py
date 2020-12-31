import os
import re
import configparser
from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import prompt, print_json

file_config_ini = 'config.ini'

class IPAddressValidator(Validator):
    def validate(self, document):
        ok = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", document.text)
        if not ok:
            raise ValidationError(message='Please enter a valid IPv4 Address', cursor_position=len(document.text))

# Ask what to do about currently existing config file
opt_overwrite = None
if os.path.exists(file_config_ini):
    questions = [
        {
            'type': 'list',
            'name': 'overwrite',
            'message': 'A configuration file already exists. What would you like to do?',
            'choices': [
                '1) Keep Current',
                '2) Overwrite existing',
                '3) Create new but preserve old (creates config.ini.old)'
            ]
        }
    ]
    answers = prompt(questions)
    opt_overwrite = answers['overwrite'][:1]

# Exit if user wishes to keep current config file
if opt_overwrite == '1':
    print('Changing nothing, exiting!')
    exit(0)

questions = [
    {
        'type': 'input',
        'name': 'bridge_ip',
        'message': 'What is the IP Address of the bridge?: ',
        'validate': IPAddressValidator
    },
    {
        'type': 'input',
        'name': 'uuid',
        'message': 'Input the UUID for the Hue Bridge API Requests:'
    },
    {
        'type': 'input',
        'name': 'light_id',
        'message': 'What is the light ID:'
    },
    {
        'type': 'confirm',
        'name': 'continue',
        'message': 'Are you sure you want to create the config.ini file with these settings?',
        'default': False
    }
]
answers = prompt(questions)

# Exit immediately if user isn't sure
if not answers['continue']:
    print('User Cancelled!')
    exit(1)

# Execute overwrite logic
if not opt_overwrite is None:
    if opt_overwrite == '2':
        os.remove(file_config_ini)
    elif opt_overwrite == '3':
        # Delete old file first, if it exists
        if os.path.exists(file_config_ini + '.old'):
            os.remove(file_config_ini + '.old')
        os.rename(file_config_ini, file_config_ini + '.old')
    else:
        print('Unrecongized overwrite command')
        exit(1)

# Get answers
bridge_ip = answers['bridge_ip']
uuid = answers['uuid']
light_id = answers['light_id']

# Configure the INI object
config = configparser.ConfigParser()
config['DEFAULT'] = {
    'ip_address': 'http://' + bridge_ip,
    'uuid': uuid,
    'light_id': light_id
}

# Write Object to file
with open(file_config_ini, 'w') as conf:
    config.write(conf)

print('Successfully created', file_config_ini)