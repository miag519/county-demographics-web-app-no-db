from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    states = get_state_options()
    #print(states)
    return render_template('home.html', state_options=states)

@app.route('/showFact')
def render_fact():
    states = get_state_options()
    state = request.args.get('state')
    county = county_most_under_18(state)
    county2 = persons_below_poverty_line(state)
    county3 = asians_alone(state)
    fact = "In " + state + ", the county with the highest percentage of under 18 year olds is " + county + "."
    facts = "In " + state + ", the county with the highest percentage of persons below the poverty line is " + county2 + "."
    facts2 = "In " + state + ", the county with the highest percentage of asians alone is " + county3 + "."
    return render_template('home.html', state_options=states, funFact=fact, funFacts=facts, funFacts2=facts2)
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    states=[]
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options

def county_most_under_18(state):
    """Return the name of a county in the given state with the highest percent of under 18 year olds."""
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county
    
def persons_below_poverty_line(state):
    with open('demographics.json') as demographics_data:
       counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Income"]["Persons Below Poverty Level"] > highest:
                highest = c["Income"]["Persons Below Poverty Level"]
                county = c["County"]
    return county
    
def asians_alone(state):
    with open('demographics.json') as demographics_data:
       counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Ethnicities"]["Asian Alone"] > highest:
                highest = c["Ethnicities"]["Asian Alone"]
                county = c["County"]
    return county
        

    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=True) # change to False when running in production
