from flask import render_template
from forms import SteamTime
import st_functions as st
from steamtime import app
import requests


###################################################################################
# SteamTime  ######################################################################
@app.route('/', methods=['GET', 'POST'])
def steamtime():
    form = SteamTime()
    return render_template('/home.html',
                           form=form,
                           title='Visualize Time Spent In Your Steam Library')


@app.route('/results', methods=['GET', 'POST'])
def results():
    form = SteamTime()
    try:
        data = st.get_results_data()
        return render_template('/results.html',
                               form=form,
                               shame_list=data['shame_list'],
                               shame_total=data['shame_total'],
                               two_weeks=data['two_weeks'],
                               all_10=data['all_10'],
                               all_20=data['all_20'],
                               all_all=data['all_all'],
                               donut_data_2weeks=data['donut_data_2weeks'],
                               donut_data_10=data['donut_data_10'],
                               donut_data_20=data['donut_data_20'],
                               line_data_2weeks=data['line_data_2weeks'],
                               line_data_10=data['line_data_10'],
                               line_data_20=data['line_data_20'],
                               bar_data_2weeks=data['bar_data_2weeks'],
                               bar_data_10=data['bar_data_10'],
                               bar_data_20=data['bar_data_20'],
                               display_name=data['display_name'],
                               user_image=data['user_image'],
                               user_image_icon=data['user_image_icon'],
                               friends=data['friends'],
                               profile_url=data['profile_url'],
                               two_weeks_stats_pages=data['two_weeks_stats_pages'],
                               stats=data['stats'],
                               distinctions=data['distinctions'],
                               title='Results')
    except (KeyError, IndexError):
                    return render_template('/home.html',
                                           form=form,
                                           message='Invalid profile name or SteamID, please try again.',
                                           title='Visualize Time Spent In Your Steam Library')
    except requests.ConnectionError:
        return render_template('/home.html',
                               form=form,
                               message='The API request took too long and has timed out, please try again.',
                               title='Visualize Time Spent In Your Steam Library')