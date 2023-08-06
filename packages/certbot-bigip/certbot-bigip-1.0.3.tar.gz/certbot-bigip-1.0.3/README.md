# certbot-bigip-plugin

# Requirements
see certbot rquirements: https://certbot.eff.org/docs/install.html#system-requirements

* F5
    * LE Chain needs to be at /Common/chain_Letsencrypt and in every other folder that uses this plugin. ( f.e.: /Internal/chain_Letsencrypt)
      At the moment, the plugin checks if a corresponding certificate/chain is located in the same partition/folder as the profile that uses it
      This is eligible to change in future versions
    * clientssl profile needs to be attached to the virtual server (DOMAIN_clientssl)
      At the moment, the plugin only updates the client profile but does not attach it to the virtual server

# Install

# Usage

  Parameters:
    --certbot-bigip:bigip-username            Username for F5 Connection
    --certbot-bigip:bigip-password            Password for F5 Connection
    --certbot-bigip:bigip-partition           Partition the Virtual Server is configured on
    --certbot-bigip:bigip-clientssl-parent    Parent Profile for new client SSL profile
    --certbot-bigip:bigip-vs-list             List of virtual servers, the certificate shoudl be used for
    --certbot-bigip:bigip-device-group        Big IP device group for synchronization
    --certbot-bigip:bigip-iapp                IApp, if any, the virtual server is part of

Example:
  certbot --non-interactive --expand --email 'admin@example.com' --agree-tos
        -a certbot-bigip:bigip -i certbot-bigip:bigip
        -d 'example.com'
        --certbot-bigip:bigip-list 'example-f5.local,example-f5-ha.local'
        --certbot-bigip:bigip-username 'user'
        --certbot-bigip:bigip-password 'secret'
        --certbot-bigip:bigip-partition 'internal'"
        --certbot-bigip:bigip-clientssl-parent '/Common/parent_clientssl'
        --certbot-bigip:bigip-vs-list '/internal/example.com.app/example.com_vs'
        --certbot-bigip:bigip-device-group 'fail-sync'
        --certbot-bigip:bigip-iapp '/internal/example.com.app/example.com_vs'

# Contribute
If you find errors please add a ticket
If you fix errors please create a new branch and then a merge request 
- to the master branch if it is a bugfix
- to the development branch if it is a feature
- docker run --volume $PWD:/src -it registry.ong.at:5555/infra/certbot-plugins/environments/certbot_docker_image:master sh
- /src/python setup.py develop

use the docker image for local development

# release
to release a version on pypi tag a commit on the master branch like this "v1.0.3"