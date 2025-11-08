# NetOps
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Ansible](https://img.shields.io/badge/ansible-automation-red)
![License](https://img.shields.io/github/license/gwill1337/NetOps)
## About
This project provides an automated network validation pipeline powered by Batfish, Ansible, and GitHub Actions. It supports customizable configuration tests, ensuring that all network configs are validated, verified, and safely backed up. The project also supports generating device configurations using Jinja2 templates.  


## Using
Clone this repository, create a Personal Access Token (PAT) in GitHub Developer Settings, then add a repository secret named "GH-PAT" and paste your PAT there.

To start validating with the basic test, push any ".cfg" file into:
```
snapshots/ci_net/s1/configs/manual
```
Or push a ".yaml" file for Jinja2 autogeneration into:
```
snapshots/ci_net/s1/device-yaml/
```
## Tests and Validation
> ⚠️ **Note:** This project includes a basic default test, but for the best results you should create and customize your own validation tests.


## Execution workflow

On config push, the CI pipeline steps:   
1. Downloads and starts Batfish in Docker
2. Sets up Python 3.11
3. Installs pybatfish (2025.7.7.2423), Ansible, PyTest, and Jinja2
4. Prepares Batfish directories
5. Generates configs from YAML (if present)
6. Ensure Batfish snapshot folder exists (Ansible)
7. Runs PyTest validation
8. Creates backup of generated configs (on success)
9. Commits and pushes backups to the repo (on success)

## Support vendors
Out of the box, the project supports generating configs from YAML for Cisco, Juniper, and Palo Alto Networks.
In fact, the project supports [**all vendors supported by batfish**](https://batfish.readthedocs.io/en/latest/supported_devices.html) but configuration generation is manual except for the three vendors mentioned above.


## Repository structure/map
This project includes many directories, structured as illustrated below:
```
NetOps/
├── .github/
│    └── workflows/
│        └── workflow.yml
│
├── ansible/   
│   ├── hosts     
│   └── playbook.yml                  
│   
├── snapshots/   
│   └── ci_net/   
│       └── s1/   
│           ├── configs/   
│           │   ├── manual/
│           │   │   └── *.cfg
│           │   └──generated/
│           │      └── *.cfg     
│           └── device-yaml/
│               └── *.yaml               
│   
├── tests/    
│   └── test_batfish.py          
│   
├── tools/
│   ├── templates/
│   │   └── *.j2   
│   ├── conf-generator.py                    
│   └── render_config.py               
│   
├── backup/       <-- Backup storage for validated configs        
│   └── *.cfg   
│        
│   
├── README.md   
└── LICENSE   
 ```
