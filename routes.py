from flask import render_template, request
from forms import SteamTime
import requests
import st_functions
from steamtime import app


#######################################################################################
#####  SteamTime  ######################################################################
@app.route('/', methods=['GET', 'POST'])
def steamtime():
    form = SteamTime()

    return render_template('/home.html',
                           form=form,
                           title='Visualize Time Spent In Your Steam Library')


@app.route('/results', methods=['GET', 'POST'])
def results():
    form = SteamTime()
    if request.method == 'POST':
        # If the form does not validate an error message will be displayed
        if not form.validate():
            return render_template('/home.html',
                                   form=form,
                                   title='Visualize Time Spent In Your Steam Library')
        else:
            # Return to /home and display error if the connection times out or invalid input
            try:
                steam_id = st_functions.test_user_input(form.steamid.data)[0]
                display_name = st_functions.test_user_input(form.steamid.data)[1]

                # Performing the two main API calls
                api_call_all = requests.get('%s' % url_format % (API_URL, API_KEY, steam_id))
                api_call_2weeks = requests.get('%s' % url_format % (API_2_WEEKS, API_KEY, steam_id))

                # Storing Steam API JSON response in variables
                data_all = api_call_all.json()
                data_2weeks = api_call_2weeks.json()

                if data_all['response']:
                    print 'Response exists'
                else:
                    message = 'This profile is either private or inactive, please try another SteamID.'
                    return render_template('/home.html',
                                           form=form,
                                           message=message,
                                           title='Visualize Time Spent In Your Steam Library')

                # Parsing API calls into organized lists
                two_weeks = st_functions.parse_data(data_2weeks, playtime_2weeks, 'all', 1, steam_id)
                all_10 = st_functions.parse_data(data_all, playtime_all, 10, 0, steam_id)
                all_20 = st_functions.parse_data(data_all, playtime_all, 20, 0, steam_id)
                all_all = st_functions.parse_data(data_all, playtime_all, 'all', 0, steam_id)

                # Calling chart formatting function on organized API data
                if two_weeks == 'privacy':
                    donut_data_2weeks = ''
                    line_data_2weeks = ''
                    bar_data_2weeks = ''
                else:
                    donut_data_2weeks = st_functions.format_data(two_weeks[0], 'donut')
                    line_data_2weeks = st_functions.format_data(two_weeks[0], 'line')
                    bar_data_2weeks = st_functions.format_data(two_weeks[0], 'bar')

                donut_data_10 = st_functions.format_data(all_10[0], 'donut')
                donut_data_20 = st_functions.format_data(all_20[0], 'donut')
                line_data_10 = st_functions.format_data(all_10[0], 'line')
                line_data_20 = st_functions.format_data(all_20[0], 'line')
                bar_data_10 = st_functions.format_data(all_10[0], 'bar')
                bar_data_20 = st_functions.format_data(all_20[0], 'bar')

                # Pulling out Hall of Shame data
                shame_list = st_functions.hall_of_shame(data_all)[0]
                shame_total = st_functions.hall_of_shame(data_all)[1]

                # Grabbing friends list
                friends = st_functions.get_friends(steam_id)

                # Getting user images
                user_images = st_functions.get_user_images(steam_id)
                user_image = user_images[0]
                user_image_icon = user_images[1]

                profile_url = 'http://steamcommunity.com/profiles/%s' % steam_id

                two_weeks_stats_pages = st_functions.get_two_weeks_stats_page(two_weeks[0], steam_id, two_weeks)
                st_functions.append_2weeks_stat_pages(two_weeks_stats_pages, two_weeks)

                stats = st_functions.statistics(all_all, two_weeks, shame_list)

                distinctions = st_functions.get_distinctions(all_all, two_weeks, stats)

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

        return render_template('/results.html',
                               form=form,
                               shame_list=shame_list,
                               shame_total=shame_total,
                               two_weeks=two_weeks,
                               all_10=all_10,
                               all_20=all_20,
                               all_all=all_all,
                               donut_data_2weeks=donut_data_2weeks,
                               donut_data_10=donut_data_10,
                               donut_data_20=donut_data_20,
                               line_data_2weeks=line_data_2weeks,
                               line_data_10=line_data_10,
                               line_data_20=line_data_20,
                               bar_data_2weeks=bar_data_2weeks,
                               bar_data_10=bar_data_10,
                               bar_data_20=bar_data_20,
                               display_name=display_name,
                               user_image=user_image,
                               user_image_icon=user_image_icon,
                               friends=friends,
                               profile_url=profile_url,
                               two_weeks_stats_pages=two_weeks_stats_pages,
                               stats=stats,
                               distinctions=distinctions,
                               title='Results')

# Different API urls - Steam uses different URLs for different services within the API
API_URL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
API_2_WEEKS = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/'
API_URL_STEAMID = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
API_PLAYER = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
API_FRIENDS = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
API_KEY = st_functions.get_steam_api_key()
url_format = '%s?key=%s&steamid=%s&format=json&include_appinfo=1'
playtime_all = 'playtime_forever'
playtime_2weeks = 'playtime_2weeks'