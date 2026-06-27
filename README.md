# aws-mfa

AWS MFA session token setup helper.

## setup

Set `mfa_serial` field in `~/.aws/config`.

```
[default]
mfa_serial = arn:aws:iam::XXXXXXXXXXXX:mfa/XXXXXX
```

## usage

```
eval $(aws-mfa)
```

- Input your MFA code to `Token code:` prompt.
- The result is also stored in `~/.aws/env` file.
