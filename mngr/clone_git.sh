#!/bin/bash 

infrastructure_dir=pepr
parent=../..

if [ ! -d $parent/$infrastructure_dir/.git ]; then
    git clone git@github.com:marek094/infrastructure.git $infrastructure_dir
else 
    # parent
    cd $parent 
fi

cd $infrastructure_dir

# git repos as listed at one place in .gitignore
tag=persian_repos
repos=`awk "/$tag/{f=1;next} /$tag/{f=0} f" .gitignore | tr -d /`

for repo in $repos; do
    git clone git@github.com:marek094/$repo.git 
done