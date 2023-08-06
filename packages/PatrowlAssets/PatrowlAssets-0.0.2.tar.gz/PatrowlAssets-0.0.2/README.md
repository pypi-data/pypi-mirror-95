# PatrowlAssets
Installation:
```
pip3 install PatrowlAssets
```

Create a config.txt file:
```
aws_access_key=""
aws_secret_key=""
aws_region="eu-west-3"

ovh_endpoint="ovh-eu"
ovh_application_key=""
ovh_application_secret=""
ovh_consumer_key=""

patrowl_url="http://localhost:8000"
patrowl_auth_token="a4218191e1d5ad27ad40dbce0360e4f05e92ceb0"
```

Usage:
```
pa aws --config config.txt
```

# Roadmap
' ': Nothing, '/': In Progress, 'X': Mostly done
- [/] OVH
- [/] AWS
- [ ] GCP
- [ ] Azure
- [ ] AliCloud
- [ ] Scaleway
- [ ] Digital Ocean
- [ ] Proxmox
- [ ] VMWare vCenter
- [ ] Kubernetes
- [ ] Docker
- [ ] Docker Swarm
- [ ] OpenShift
- [ ] SCCM
- [ ] GLPI
- [ ] Terraform state
- [ ] Ansible Inventory

# Updates
Information, news and updates are regularly posted on [Patrowl.io Twitter account](https://twitter.com/patrowl_io) and on [the  blog](https://blog.patrowl.io/).

# Contributing
Please see our [Code of conduct](https://github.com/Patrowl/PatrowlDocs/blob/master/support/code_of_conduct.md). We welcome your contributions. Please feel free to fork the code, play with it, make some patches and send us pull requests via [issues](https://github.com/Patrowl/PatrowlEngines/issues).

# Support
Please [open an issue on GitHub](https://github.com/Patrowl/PatrowlEngines/issues) if you'd like to report a bug or request a feature. We are also available on [Gitter](https://gitter.im/Patrowl/Support) to help you out.

If you need to contact the project team, send an email to <getsupport@patrowl.io>.

# Commercial Services
Looking for advanced support, training, integration, custom developments, dual-licensing ? Contact us at getsupport@patrowl.io

# Security contact
Please disclose any security-related issues or vulnerabilities by emailing security@patrowl.io, instead of using the public issue tracker.

# Copyright
Copyright (C) 2018-2021 Nicolas MATTIOCCO ([@MaKyOtOx](https://twitter.com/MaKyOtOx) - nicolas@patrowl.io)

# Pypi Deployment commands
rm -rf dist/ build/ PatrowlAssets.egg-info
python3 setup.py sdist bdist_wheel
twine upload -u Patrowl dist/*
