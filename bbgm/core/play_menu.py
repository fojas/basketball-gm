import cPickle as pickle
from juggernaut import Juggernaut
import time

from flask import url_for, g, render_template

jug = Juggernaut()

def options(keys=None):
    all_options = [{'id': 'stop', 'url': '#', 'label': 'Stop', 'normal_link': False},
                   {'id': 'day', 'url': url_for('play', league_id=g.league_id, amount='day'), 'label': 'One day', 'normal_link': False},
                   {'id': 'week', 'url': url_for('play', league_id=g.league_id, amount='week'), 'label': 'One week', 'normal_link': False},
                   {'id': 'month', 'url': url_for('play', league_id=g.league_id, amount='month'), 'label': 'One month', 'normal_link': False},
                   {'id': 'until_playoffs', 'url': url_for('play', league_id=g.league_id, amount='until_playoffs'), 'label': 'Until playoffs', 'normal_link': False},
                   {'id': 'through_playoffs', 'url': url_for('play', league_id=g.league_id, amount='through_playoffs'), 'label': 'Through playoffs', 'normal_link': False},
                   {'id': 'until_draft', 'url': url_for('play', league_id=g.league_id, amount='until_draft'), 'label': 'Until draft', 'normal_link': False},
                   {'id': 'view_draft', 'url': url_for('draft'), 'label': 'View draft', 'normal_link': True},
                   {'id': 'until_free_agency', 'url': url_for('play', league_id=g.league_id, amount='until_free_agency'), 'label': 'Until free agency', 'normal_link': False},
                   {'id': 'until_preseason', 'url': url_for('play', league_id=g.league_id, amount='until_preseason'), 'label': 'Until preseason', 'normal_link': False},
                   {'id': 'until_regular_season', 'url': url_for('play', league_id=g.league_id, amount='until_regular_season'), 'label': 'Until regular season', 'normal_link': False},
                   {'id': 'negotiate', 'url': '#', 'label': 'Negotiate', 'normal_link': False},
                   {'id': 'cancel', 'url': '#', 'label': 'Cancel', 'normal_link': False}]

    if keys:
#        dict_you_want = { your_key: old_dict[your_key] for your_key in your_keys }
#        some_options = {key: old_dict[your_key] for key in keys}
        some_options = []
        for key in keys:
            some_options.append()
        return some_options
    else:
        return all_options

def set_status(status=None):
    """Save status to database and push to client.

    If no status is given, load the last status from the database and push that
    to the client.

    Args:
        status: A string containing the current status message to be pushed to
            the client.
        db: A database cursor (if not given, g.db is used).
        league_id: League ID (if not given, g.league_id is used).
        season: Year of the current season (if not given, g.season is used).
    """
    g.db.execute('SELECT pm_status FROM %s_game_attributes WHERE season = %s', (g.league_id, g.season))
    old_status, = g.db.fetchone()

    if not status:
        status = old_status
        jug.publish('%d_status' % (g.league_id,), status)
    if status != old_status:
        g.db.execute('UPDATE %s_game_attributes SET pm_status = %s WHERE season = %s', (g.league_id, status, g.season))
        jug.publish('%d_status' % (g.league_id,), status)

def set_options(options_keys=None):
    """Save options_ids to database and push rendered play button to client.

    If no options_ids are given, load the last ones from the database and push
    a button created from them.

    Args:
        status: A list containing the IDs of the various predefined options to
            be shown to the user (see bbgm.core.play_menu.options()).
    """
    if options_keys:
        g.db.execute('UPDATE %s_game_attributes SET pm_options = %s WHERE season = %s', (g.league_id, pickle.dumps(options_ids), g.season))
    else:
        g.db.execute('SELECT pm_options FROM %s_game_attributes WHERE season = %s', (g.league_id, g.season))
        row = g.db.fetchone()
        try:
            options_keys = pickle.loads(row[0].encode('ascii'))
        except:
            options_keys = []
    button = render_template('play_button.html', league_id=g.league_id, options=options(options_keys))
    jug.publish('%d_button' % (g.league_id,), button)

