#!/bin/bash 

infrastructure_dir=pepr
parent=../..

sshOrHttps=${1:-ssh}

if [ "$sshOrHttps" = "ssh" ]; then
    address="git@github.com:"
else
    address="https://github.com/"
fi

echo ${address}

if [ ! -d $parent/$infrastructure_dir/.git ]; then
    git clone ${address}marek094/infrastructure.git $infrastructure_dir
else 
    # parent
    cd $parent 
fi

# CD TO INFRASTRUCTURE_DIR
cd $infrastructure_dir

# Config Git Hooks
hooks=./mngr/git_hooks
git config core.hooksPath "$hooks"

# git repos as listed at one place in .gitignore
tag=persian_repos
repos=`awk "/$tag/{f=1;next} /$tag/{f=0} f" .gitignore | tr -d /`

for repo in $repos; do
    git clone git@github.com:marek094/$repo.git
    ( 
        cd "$repo"; 
        git config core.hooksPath "../$hooks"
    )
done