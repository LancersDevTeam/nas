#!/bin/bash  

rm -rf dist  
mkdir dist  
cp -r src/* dist  
pipenv lock -r > requirements.txt  
pip install -r requirements.txt -t dist  
cd dist  
zip -r ../lambda_function.zip *  
cd ..  
rm requirements.txt
rm -rf dist
echo "done"