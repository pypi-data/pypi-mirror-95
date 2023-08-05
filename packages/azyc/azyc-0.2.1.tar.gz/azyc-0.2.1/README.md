# azyc: Yaml to azure deployment parameter json converter

[![PyPI - License](https://img.shields.io/pypi/l/azyc)](https://pypi.org/project/azyc/)
[![PyPI](https://img.shields.io/pypi/v/azyc)](https://pypi.org/project/azyc/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/azyc)

Helper to create large large deployment-parameters.json files from small yaml files

# Usage

You can specify deployment variables in a yml file. 

Additionally to simple variables, you can add file pathes, which are read and written into the deplyoemnt file as string.

KeyVault values as also supported.

Examples:
```yaml
foo: bar
booleanParam: true
numericParam: 22
fileParam:
    file: path_to_file # will be read as utf-8, escaped and passed as string
binaryFileParam:
    binary: path_to_binary_file # will be read as binary, base64 encoded and passed as string
keyVaultParam:
    keyVault: /subscriptions/<subscription-id>/resourceGroups/<rg-name>/providers/Microsoft.KeyVault/vaults/<vault-name>
    secretName: ExamplePassword

keyVaultParamWitVersion:
    keyVault: /subscriptions/<subscription-id>/resourceGroups/<rg-name>/providers/Microsoft.KeyVault/vaults/<vault-name>
    secretName: ExamplePassword
    secretVersion: cd91b2b7e10e492ebb870a6ee0591b68
 ```

Basic call:

```bash
python3 -m azyc -i path_to_config.yml -o paramters.json
```

You can add/overwrite parameters on the call:

```bash
python3 -m azyc -i path_to_config.yml -o paramters.json --param suffix=bar --param booleanParam=false 
```

