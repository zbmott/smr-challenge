#!/bin/bash

ansible-playbook app.yml -i inventories/$1 --ask-pass --ask-become-pass --ask-vault-pass
