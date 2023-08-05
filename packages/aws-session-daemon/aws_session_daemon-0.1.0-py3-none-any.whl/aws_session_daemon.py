#!/usr/bin/env python3
import os
import fileinput
import sys
import click
import aws_credential_process
import time
import configparser

"""
.config/systemd/user/aws-session-daemon@.service

[Unit]
Description=Amazon Web Services token daemon

[Service]
Type=simple
ExecStart=/usr/bin/python3 -u %h/bin/aws_session-daemon --rolearn='...%i...' --oath_slot=... --serialnumber=... --profile_name='...%i...'
Restart=on-failure

[Install]
WantedBy=default.target
"""

"""
.aws/credentials

[default]
aws_access_key_id = ...
aws_secret_access_key = ...

[...]
aws_access_key_id = ...
aws_secret_access_key = ...
aws_session_token = ...
"""


class NoYubiKeyException(Exception):
    pass


@click.command()
@click.option("--rolearn", required=False)
@click.option("--oath_slot", required=True)
@click.option("--serialnumber", required=True)
@click.option("--profile_name", required=True)
@click.option("--access-key-id", required=False)
@click.option("--secret-access-key", required=False)
@click.option("--mfa-session-duration", type=int)
@click.option("--credentials-section", default="default")
def main(
    rolearn,
    oath_slot,
    serialnumber,
    profile_name,
    access_key_id,
    secret_access_key,
    mfa_session_duration,
    credentials_section,
):
    invalid_token = None
    if not access_key_id:
        access_key_id, secret_access_key = aws_credential_process.get_credentials(
            credentials_section
        )

    if access_key_id is None:
        click.echo(
            "Missing access_key_id, please use --access-key-id or add to ~/.aws/credentials"
        )
        sys.exit(1)
    if secret_access_key is None:
        click.echo(
            "Missing secret_access_key, please use --secret-access-key or add to ~/.aws/credentials"
        )
        sys.exit(1)

    access_key = aws_credential_process.AWSCred(access_key_id, secret_access_key)

    def token_code():
        stdout, _ = aws_credential_process.ykman_main("oath", "code", "-s", oath_slot)

        if len(stdout) == 1:
            (token_code,) = stdout
            return token_code

        raise NoYubiKeyException()

    while 1:
        mfa_session = None
        while mfa_session is None:
            try:
                mfa_session = aws_credential_process.get_mfa_session_cached(
                    access_key, mfa_session_duration, serialnumber, token_code
                )
            except NoYubiKeyException:
                pass
            time.sleep(1)

        if rolearn:
            session = aws_credential_process.get_assume_session(
                access_key, mfa_session, rolearn, None
            )
        else:
            session = mfa_session

        credentials_file = os.path.expanduser("~/.aws/credentials")
        # rotate credentials files
        for i in range(5, 0, -1):
            original = "{}.{}".format(credentials_file, i)
            if os.path.exists(original):
                os.rename(original, "{}.{}".format(credentials_file, i + 1))

        # update credentials file
        updated = {}
        profile = False
        for line in fileinput.input(credentials_file, inplace=True, backup=".1"):
            if profile and line[0] == "[":
                profile = False
            if line == "[{}]\n".format(profile_name):
                updated["profile"] = True
                profile = True
            if profile and line.startswith("aws_access_key_id"):
                updated["aws_access_key_id"] = True
                line = "aws_access_key_id = {}\n".format(session.awscred.access_key_id)
            if profile and line.startswith("aws_secret_access_key"):
                updated["aws_secret_access_key"] = True
                line = "aws_secret_access_key = {}\n".format(
                    session.awscred.secret_access_key
                )
            if profile and line.startswith("aws_session_token"):
                updated["aws_session_token"] = True
                line = "aws_session_token = {}\n".format(session.session_token)
            print(line, end="")

        if len(updated) == 0:
            print("Profile [{}] not found in ~/.aws/credentials".format(profile_name))
        if len(updated) < 4:
            for k in [
                "aws_access_key_id",
                "aws_secret_access_key",
                "aws_session_token",
            ]:
                if not k in updated:
                    print(
                        "{} not found in ~/.aws/credentials profile [{}]".format(
                            k, profile_name
                        )
                    )

        time.sleep(60 * 15)
