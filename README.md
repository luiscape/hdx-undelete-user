## Undelete User from HDX
Sometimes we make mistakes -- and end up deleting users from HDX by accident. CKAN never deletes users, but changes their status in the system to `"deleted"`. Thanks to that functionality, to undelete an user just run this script passing the user id as a parameter.

## Installation
If you are on an Unix machine, run:
```shell
$ ./setup.sh
```

## Usage
```shell
$ python undelete_user USER_ID
```

This will fail if you don't include your API key to the configuration file on `config/config.json`:

```json
{
  "hdx_key": "XXX"
}
```