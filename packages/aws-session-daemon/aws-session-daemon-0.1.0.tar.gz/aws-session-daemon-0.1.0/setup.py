# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_session_daemon']
install_requires = \
['aws_credential_process>=0.2', 'click>=7']

entry_points = \
{'console_scripts': ['aws-session-daemon = aws_session_daemon:main']}

setup_kwargs = {
    'name': 'aws-session-daemon',
    'version': '0.1.0',
    'description': 'AWS session token refreshing daemon',
    'long_description': "AWS Assume daemon\n=================\n\nThis script automatically assumes every 15 minutes the specified role using a Yubikey as MFA (multi factor authentication) and updates\n`~/.aws/credentials`.\n\nAs long as you've got your yubikey connected to your computer you'll never have to enter a second factor authentication code for the aws\ncli. As other tools / libraries (boto3) use `~/.aws/credentials` as well you don't have to enter a token for these either.\n\nUsage\n-----\n\nYou can install `aws-session-daemon` using pip (`pip install aws-session-daemon`), I recommend to install `aws-session-daemon` using poetry\n(`poetry install aws-session-daemon`) or in a virtualenv.\n\nYour `~/.aws/credentials` should contain your credentials and a profile with the the keys `aws_access_key_id`,\n`aws_secret_access_key` and `aws_session_token`.\n\nFor example:\n\n`~/.aws/credentials`\n\n```ini\n[default]\naws_access_key_id = ...(your key id)...\naws_secret_access_key = ...(your access key)...\n\n[profile]\naws_access_key_id = ...(placeholder, can be anything)...\naws_secret_access_key = ...(placeholder, can be anything)...\naws_session_token = ...(placeholder, can be anything)...\n```\n\nYour `~/.aws/credentials` will be updated in place, only the specified profile section should be touched (your comments will be safe).\n\nOlder versions are rotated up to 5 items.\n\nNext `aws-session-daemon` should be started with the following arguments:\n\n```bash\naws-session-daemon --rolearn ... --oath_slot=... --serialnumber=... --profile_name=... --access-key-id=... --secret-access-key=... --mfa-session-duration=...\n```\n\nArgument                 | Description\n-------------------------|-------------------------------------\n`--rolearn`              | arn of the role you'd like to assume\n`--oath_slot`            | oath slot on your yubikey\n`--serialnumber`         | serial number of your MFA\n`--profile_name`         | profile used in `~/.aws/credentials`\n`--access-key-id`        | access key (as obtained from IAM console)\n`--secret-access-key`    | secret access key (as obtained from IAM console)\n`--mfa-session-duration` | duration (in seconds) for MFA session\n`--credentials-section`  | you can specify a different section than default in `~/.aws/credentials`\n\nYou should only run one `aws-session-daemon` process per profile, I use systemd for starting `aws-session-daemon`, by using the\nfollowing unit file:\n\n`~/.config/systemd/user/aws-session-daemon@.service`\n\n```ini\n[Unit]\nDescription=Amazon Web Services token daemon\n\n[Service]\nType=simple\nExecStart=%h/bin/aws-session-daemon --rolearn='...%i...' --oath_slot=... --serialnumber=... --profile_name='...%i...' --access-key-id='...' --secret-access-key='...'\nRestart=on-failure\n\n[Install]\nWantedBy=default.target\n```\n\nAnd reload systemd using `systemctl --user daemon-reload`, start `aws-session-daemon` using `systemctl --user start aws-session-daemon@...`\n\nIf you're not so fortunate to have systemd you can also use something like `supervisord` to start `aws-session-daemon`.\n\n`~/supervisord.conf`\n\n```ini\n[supervisord]\n\n[supervisorctl]\nserverurl=unix:///home/user/supervisord.sock\n\n[unix_http_server]\nfile=/home/user/supervisord.sock\n\n[rpcinterface:supervisor]\nsupervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface\n\n[program:assume-...]\ncommand=/home/user/bin/aws-session-daemon --rolearn=... --oath_slot=... --serialnumber=... --profile_name=... --access-key-id=... --secret-access-key=...\nautorestart=true\n```\n\nStart supervisord using `supervisord -c supervisor.conf` and start assume using\n`supervisorctl -c supervisor.conf start assume-...`.\n",
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meeuw/aws-session-daemon',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
