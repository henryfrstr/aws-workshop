#! /bin/bash
yum update -y
yum install python3 -y
pip3 install flask
TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
FOLDER="https://$TOKEN@raw.githubusercontent.com/clarusway/clarusway-aws-devops-1-20/master/aws/class-notes/portfolio-project-002-07_26_2020/"
curl -s --create-dirs -o "/home/ec2-user/templates/index.html" -L "$FOLDER"templates/index.html
curl -s --create-dirs -o "/home/ec2-user/templates/result.html" -L "$FOLDER"templates/result.html
curl -s --create-dirs -o "/home/ec2-user/app.py" -L "$FOLDER"app.py
python3 /home/ec2-user/app.py