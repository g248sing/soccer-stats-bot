# Types of plots (based on position)
RT2POS = {
    'Forwards': ['FW','FW,MF','MF,FW','FW,DF'],
    'Attacking Mids/Winger/Wingbacks': ['MF,FW','FW,MF','FW,DF','DF,FW'],
    'Central/Defensive/Wide Mids': ['MF,FW', 'MF','MF,DF'],
    'Centerbacks/Fullbacks/Wingbacks': ['DF','DF,FW','DF,MF'],
    'Goalkeepers': ['GK']
}

RADAR_TYPES = RT2POS.keys()

_FWD_COLS = [
 'Shots',
 'Non-penalty goals',
 'Non-penalty xG',
 'Passes into final third',
 'Passes into box',
 'xA',
 'Shot-creating actions',
 'Successful dribbles',
 'Dribbles_Success%',
 'Carries into the final third',
 'Carries into the box',
 'Progressive passes received',
 'Progressions',
#  'PAdj Pressures',
 'Turnover'
]

_MF_COLS = [
 'Progressive passes',
 'Passes into final third',
 'Passes into box',
 'xA',
 'Shot-creating actions',
 'Progressive carries',
 'Carries into the final third',
 'Successful dribbles',
 'Dribbles_Success%',
 'Dribbled_Past',
 'TrueTackleWin%',
 'PAdj TrueTackle',
#  'PAdj Pressures',
 'PAdj True Interceptions',
 'Turnover',
]

_DEFNDER_COLS = [
 'Passes into final third',
 'Passes into box',   
 'xA',
 'Carries into the final third',
 'Successful dribbles',
 'Dribbles_Success%',
 'Dribbled_Past',
 'Progressions',
 'Aerial Duels_Won%',
 'TrueTackleWin%',
 'PAdj TrueTackle',
#  'PAdj Pressures',
 'PAdj True Interceptions'
]

_GK_COLS = [
 'Shots on Target Against',
 'PK Against',
#  'PK Save %',
 'PSxG +/-',
 'GSAA %',
 'Launch Passes Attempted',
 'Launch Passes Completed',
 'Cross Stop%',
 'Defensive Actions Outside PA',
 'Avg. Dist. of Defensive Actions from Goal',
 'Shortpass_Completion%',
 'Mistakes Leading to a Shot',
]

# Columns to use for these group of players in "radar" plot
RT_COLS = {
    'Forwards': _FWD_COLS,
    'Attacking Mids/Winger/Wingbacks': _FWD_COLS,
    'Central/Defensive/Wide Mids': _MF_COLS,
    'Centerbacks/Fullbacks/Wingbacks': _DEFNDER_COLS,
    'Goalkeepers': _GK_COLS,
}


SHOOTING_COLS = [
 'Goals',
 'Shots',
 'Shots_on_Target',
 'Shots_on_Target%',
 'Goals/Shot',
 'Goals/Shots_on_Target',
 'Shot_Distance',
 'Freekicks',
 'Penalties_scored',
 'Penalties_attempted',
 'Non-penalty goals',
 'Non-penalty xG',
 'xG',
 'NpxG/Shot',
 'Goals-xG',
 'NpGoals-xG',
 'NpxG+xA',
 'NpG+A'
]

PASSING_COLS = [
 'Progressive passes',
 'Passes into final third',
 'Passes into box',
 'Passes_Completed',
 'Passes_Attempted',
 'Pass_Completion%',
 'Passes_TotalDistance',
 'Passes_ProgressiveDistance',
 'Shortpasses_Completed',
 'Shortpasses_Attempted',
 'Shortpass_Completion%',
 'Mediumpasses_Completed',
 'Mediumpasses_Attempted',
 'Mediumpass_Completion%',
 'Longpasses_Completed',
 'Longpasses_Attempted',
 'Longpass_Completion%',
 'KeyPasses',
]

ADV_PASSING_COLS = [
 'Crosses_into_box',
 'Live_Passes',
 'Dead_ball_passes',
 'FreeKick_passes',
 'ThroughBalls',
 'Under_Pressure_passes',
 'Switches',
 'Crosses',
 'CornerKick_passes',
 'CornerKicks_Inswinging',
 'CornerKicks_Outswinging',
 'CornerKicks_Straight',
 'Ground_passes',
 'Low_passes',
 'High_passes',
 'Passes_Leftfoot',
 'Passes_Rightfoot',
 'Head_passes',
 'ThrowIns',
 'Passes_other_body_parts',
 'Offside_passes'
]

CREATION_COLS = [
 'Assists',
 'xA',
 'Assists-xA',
 'Shot-creating actions',
 'SCA_PassLive',
 'SCA_PassDead',
 'SCA_Dribbles',
 'SCA_Shots',
 'SCA_Fouls_drawn',
 'SCA_Defensive_actions',
 'GCA',
 'GCA_PassLive',
 'GCA_PassDead',
 'GCA_Dribbles',
 'GCA_Shots',
 'GCA_Fouls_drawn',
 'GCA_Defensive_actions',
 'GCA_OwnGoals'
]

POSESSION_COLS = [
 'Progressive carries',
 'Carries into the final third',
 'Carries into the box',
 'Progressive passes received',
 'Fouls drawn',
 'Touches',
 'Touches_Def_Pen',
 'Touches_Def_3rd',
 'Touches_Mid_3rd',
 'Touches_Att_3rd',
 'Touches_Att_Pen',
 'Touches_Live',
 'Dribbles_Attempted',
 'Successful dribbles',
 'Dribbles_Success%',
 '#Players_dribbled_past',
 'Nutmegs',
 'Carries',
 'Carries_TotalDistance',
 'Carries_ProgressiveDistance',
 'Pass_Target',
 'Passes_Received',
 'Pass_Receive%',
 'Progressions',
 'Fouled'
]



DEFENCE_COLS = [
 'Tackles_Attempted',
 'Tackles_Won',
 'Tackles_Def_3rd',
 'Tackles_Mid_3rd',
 'Tackles_Att_3rd',
 'Dribblers_Tackled',
 'Dribbles_Contested',
 'Dribblers_Tackled%',
#  'Pressures',
#  'Successful_pressures',
#  'Pressures_success%',
#  'Pressures_Def_3rd',
#  'Pressures_Mid_3rd',
#  'Pressures_Att_3rd',
 'Blocks',
 'Blocks_Shots',
 'Blocks_Shots_on_target',
 'Blocks_Pass',
 'Interceptions',
 'Tackles+Interceptions',
 'Clearances','Ball_Recoveries',
 'Aerial Duels_Won',
 'Aerial Duels_Won%',
]

ADV_DEFENCE_COLS = [
 'TrueTackle',
 'TrueTackleWin%',
 'PAdj TrueTackle',
 'PAdj Tackles_Attempted',
 'PAdj Tackles_Won',
 'PAdj Tackles_Def_3rd',
 'PAdj Tackles_Mid_3rd',
 'PAdj Tackles_Att_3rd',
#  'PAdj Pressures',
#  'PAdj Successful_pressures',
#  'PAdj Pressures_Def_3rd',
#  'PAdj Pressures_Mid_3rd',
#  'PAdj Pressures_Att_3rd',
 'PAdj Blocks',
 'PAdj Blocks_Shots',
 'PAdj Blocks_Shots_on_target',
 'PAdj Blocks_Pass',
 'PAdj Interceptions',
 'PAdj Tackles+Interceptions',
 'PAdj Clearances',
 'True Interceptions',
 'PAdj True Interceptions',
 'PAdj True Tackles+Interceptions'
]

GK_COLS = [
'Goals Against',
'Shots on Target Against',
'Saves',
'Save %',
'Clean Sheet %',
'PK Against',
'PK Allowed',
'PK Saved',
'PK Missed',
'PK Save %',
'Free Kick Goals',
'Corner Kick Goals',
'Own Goals',
'PSxG',
'PSxG per Shot on Target',
'PSxG +/-',
'Launch Passes Completed',
'Launch Passes Attempted',
'Lauch Pass Completion%',
'Passes Attempted',
'Throws Attempted',
'Launch %',
'Average Pass length (yards)',
'Goal Kicks Attempted',
'Goal Kick Launch%',
'Average Goal Kick Length',
'Crosses Against',
'Crosses Stopped',
'Cross Stop%',
'Defensive Actions Outside PA',
'Avg. Dist. of Defensive Actions from Goal',
'Possession%',
]

# lower is better
NEGATIVE_COLS = [
 'Dribbled_Past',
 'Aerial Duels_Lost',
 'Miscontrols',
 'Yellow_Cards',
 'Red_Cards',
 'Second_Yellow_Card',
 'Fouls',
 'Offsides',
 'OwnGoals',
 'Turnover',
 'Turnovers_per_100Touches',
 'Goals Against',
 'Shots on Target Against',
 'PK Against',
 'PK Allowed',
 'Corner Kick Goals',
 'Own Goals',
 'Crosses Against',
 'Mistakes Leading to a Shot',
]

# ALL_COLS = \
#     SHOOTING_COLS + \
#     PASSING_COLS + \
#     ADV_PASSING_COLS + \
#     CREATION_COLS + \
#     POSESSION_COLS + \
#     DEFENCE_COLS + \
#     ADV_DEFENCE_COLS + \
#     NEGATIVE_COLS
