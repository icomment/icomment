#!/bin/bash
git pull origin master
git add -A

echo " input your comment: "
read cmt
git commit -m "$cmt"
git push --all
