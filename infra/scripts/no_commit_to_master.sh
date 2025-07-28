#!/bin/sh
branch_name=$(git symbolic-ref --short HEAD)

if [ "$branch_name" = "master" ]; then
    echo "❌ Commit direto na branch 'master' não é permitido."
    exit 1
fi
