# cf-recsys
To run the API follow these steps: 
- cd into the ```api``` folder
- Run the following command: ```python3 -m uvicorn api:app --reload```
- Make sure to use the same enviroment
- In case you're on an M1 mac follow these steps:
    - Create a clone of your terminal in the ```Applications``` Folder and call is ```Terminal Rosetta```
    - Right click on the clone and click on ```get info```
    - Check the box which says ```run with Rosetta```
    - Install the Intel version of Miniconda and create a new environment with the ```environment.yml``` file in this repo.
    - As a sanity check run ```pip3 install -r requirements.txt``` and make sure the ***Python version is 3.7***

After running the API go into the frontend folder in a different terminal and start the frontend using ```npm run start```

A demo of this project can be found here: https://youtu.be/MQSdSy4xQL4