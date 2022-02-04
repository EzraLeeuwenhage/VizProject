# Traviz-app

## About this app

This app is TraViz.
Note: Python 3.8+ is REQUIRED.

## What part we implemented

We implemented the code in all of the .py files of this project.
That includes all of the plots, the data loading, and the UI interaction with Dash.
We use the libraries plotly, pandas, and Dash.

When you first run the code, it will ask a sampling rate.
Higher values make the code run faster.
We suggest trying 30 to see the graphs quickly.

# Organization
`app.py`: the entry point
`ave/`: various data loading utilities
`jbi100_app/`: the main project code, organized by page number
`jbi100_app/`: all of the graphs shown in the tool, one per file

## Requirements

* Python 3 (add it to your path (system variables) to make sure you can access it from the command prompt)
* Git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## How to run this app

Clone this repository and open your terminal/command prompt in the root folder.


open the command prompt
cd into the folder where you want to save the files and run the following commands. To get the HTTPS link, press the clone button in the right top corner and then copy the link under "Clone with HTTPS". 

```
> git clone <HTTPS link>
> cd <folder name on your computer>
> python -m venv venv

```
If python is not recognized use python3 instead

In Windows: 

```
> venv\Scripts\activate

```
In Unix system:
```
> source venv/bin/activate
```

Install all required packages by running:
```
> pip install -r requirements.txt
```

Run this app locally with:
```
> python app.py
```
You will get a http link, open this in your browser to see the results. You can edit the code in any editor (e.g. Visual Studio Code) and if you save it you will see the results in the browser.

## Resources

* [Dash](https://dash.plot.ly/)