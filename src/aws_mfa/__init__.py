#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys


def safe_capture_output(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        print(f"Command {cmd} returned {proc.returncode}", file=sys.stderr)
        print("Error:", proc.stderr.decode(), file=sys.stderr)
        sys.exit(1)
    return proc.stdout.decode().strip()


def get_mfa_serial(profile: str) -> str:
    cmd = ["aws", "configure", "get", "mfa_serial", "--profile", profile]
    return safe_capture_output(cmd)


def get_session_token_json(profile: str, token_code: int) -> dict[str, str]:
    mfa_serial = get_mfa_serial(profile)
    cmd = [
        "aws",
        "sts",
        "get-session-token",
        "--serial-number",
        mfa_serial,
        "--token-code",
        token_code,
        "--profile",
        profile,
    ]
    out = safe_capture_output(cmd)
    return json.loads(out)


def make_aws_env_str(access_key_id, secret_access_key, session_token):
    env_strs = []
    env_strs.append(f"export AWS_ACCESS_KEY_ID={access_key_id}")
    env_strs.append(f"export AWS_SECRET_ACCESS_KEY={secret_access_key}")
    env_strs.append(f"export AWS_SESSION_TOKEN={session_token}")
    return "\n".join(env_strs) + "\n"


def main():
    profile = "default"

    prompt = "Token code: "
    print(prompt, file=sys.stderr, end="")
    token_code = input()

    # Get session token
    data = get_session_token_json(profile, token_code)

    credentials = data["Credentials"]
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]

    env_strs = make_aws_env_str(access_key_id, secret_access_key, session_token)
    print(env_strs, end="")

    env_path = pathlib.Path.home() / ".aws" / "env"
    with open(env_path, "w") as f:
        f.write(env_strs)


if __name__ == "__main__":
    main()
