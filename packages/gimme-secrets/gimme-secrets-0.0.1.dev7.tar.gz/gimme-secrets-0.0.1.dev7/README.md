# Gimme Secrets

gimme-secrets is a cli tool to manage AWS Parameter Store values.

It can:
- Put entry in Parameter Store
- Get value from Parameter Store
- Decrypt and Encrypt value using KMS
- Move Parameter Store entries between AWS accounts and regions.


## Prerequisites
Python 3.6 or above

## Configuration

For AWS set the `AWS_MASTER_ROLE_ARN` to the ARN of the account which has permissions to switch to other accounts.


### How to use?

Install/Upgrade from PyPi:

`pip3 install --upgrade gimme-secrets`

- run `gimme-secrets` for available options

```
gimme-secrets
Usage: gimme-secrets [OPTIONS] COMMAND [ARGS]...

  Command-line interface for managing secrets for:

   AWS

Options:
  --help  Show this message and exit.

Commands:
  aws-decrypt-secret  aws decrypt secrets using kms key
  aws-encrypt-secret  aws encrypt secrets using kms key
  aws-get-secret      aws get values from Parameter Store
  aws-put-secret      aws put values in Parameter Store
  copy-secret         copy secrets

```
