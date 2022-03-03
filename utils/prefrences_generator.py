from configparser import ConfigParser

config = ConfigParser()

config['AUTOPILOT'] = {
    'primaryrole': 'top',
    'secondaryrole': 'jungle'
}

with open('autopilot.ini', 'w') as f:
    config.write(f)
