# 2IOA0-2019-2020-Group13

This is the repo for Goup 13 for the 2019-2020 edition of the course 2IOA0 DBL HTI+Webtech

## FOR THOSE WHO WANT TO WORK ON PYTHON STUFF AND  DOWNLOAD THE FILES 

# Data Visualizer (DBL HTI+Webtech Group 13 2019-2020)

This is the repo for Group 13 for the 2019-2020 edition of the course 2IOA0 DBL HTI+Webtech

## What languages do we use

Python (version 3.8)-Backend

HTML+CSS+Javascript-Frontend

## What Libraries did we use (Check the 'how to install' section on how to install them)

1.Backend:

-Pandas

-Numpy

-OpenCV-python

-SciPy

-Matplotlib

-Flask

-Pillow

-Bokeh

-sklearn



2.Frontend:

-BootstrapVue (It's a combination of Bootstrap (CSS) with Vue (Javascript))

## How to setup the website (initial setup)

### If using the command line
1. Go to the directory of the folder where the website is (using ```cd: ....```)

2. Create a virtual enviroment: 
```py -3 -m venv venv```

3.Activate the enviroment:
```venv\Scripts\activate```

***NOTE*** Step 2 needs to only be done once, when first downloading the project, step 1 and 3 must be done only once before running the project after booting up your PC every time

4.Install the backend libraries (the ones mentioned above) using:
```pip install <library>```
***NOTE*** for the frontend libraries, you do not need to install anything

### If Using an code editor, like VS Code
1.Open the folder where you have downloaded the files

2.Install the backend libraries (the ones mentioned above) using:
```pip install <library>```
***NOTE*** for the frontend libraries, you do not need to install anything

## How to run the code:

### If using command line
-Type the following command:
```flask run```

### If using a code editor, like VS Code:
-Run the code from the ```app.py``` file

***COMMON FOR BOTH OPTIONS***
-Once you run the file, you will get the following:
``` * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://<IP address>:5000/ (Press CTRL+C to quit)
 ```
 -Just copy the given ``http://`` adress into a web browser and it should run

## How to navigate the website:
1. Upload the csv database
2. Upload the Stimuli image you wish to be visualized
3.Wait a few seconds for the visualizations to be computed and visualized
4. Navigate the visualizations

## What visualizations do we have
1.Gaze plot

2.Gaze stripe

4.Heat map

5.Eye clouds

If you have any questions on the website or wish to improve it,send me an email: ``s.robu@student.tue.nl```
