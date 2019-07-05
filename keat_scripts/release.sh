#!/usr/bin/env bash

EMOJI="\xE2\x9C\xA8 \xF0\x9F\x8C\xB2 \xE2\x9C\xA8"
SEP="*****"
CURRENT=$(poetry run keats version)
NAME=$(poetry run keats package)
COLOR="\e[1;31m"
CINPUT="\e[32m"
CWARN="\e[1;31m"
CINFO="\e[34m"
END="\e[0m"

COMMIT=0
PUSH=0
REPO=""
VERSION=""

echo "$EMOJI $NAME $CURRENT $EMOJI"

################################
# Version
################################
printf "$CINPUT Version (or bump): $END"
read input
if [ "$input" != "" ]; then
    VERSION=$input
fi

poetry run keats bump $VERSION

################################
# Setup
################################
printf "$CINPUT Commit changes to git (y/[n]): $END"
read input
if [ "$input" == "y" ]; then
    COMMIT=1
fi

if [ "$COMMIT" == 1 ]; then
    printf "$CINPUT Add a commit message prefix?: $END"
    read PREFIX

    printf "$CINPUT Push changes to github (y/[n]): $END"
    read input
    if [ "$input" == "y" ]; then
        PUSH=1
    fi
fi

printf "$CINPUT Would you like to publish this package to a repo?$END\n"
printf "$CINPUT New repos can be configures using $CINFO 'poetry config repositories.<reponame> <url>' $END\n"
printf "$CINPUT Repository name (default: pypi): $END"
read input
if [ "$input" != "" ]; then
    REPO=$input
fi
