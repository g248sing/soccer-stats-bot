import gc
from io import BytesIO
from typing import Any, Dict

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from highlight_text import fig_text

from utils.data import (
    FBREF_LOGO,
    SB_LOGO,
    FCD_QR,
    RT_COLS
)

CREDITS = "FC Discordelona"

COLOR1 = '#d67171'
COLOR2 = '#8787e3'
BGCOLOR = '#222222'
TEXT_COLOR = '#f6f6f6'
HIGHLIGHT_COLOR = 'w'
EMP_COLOR = '#FFED02'

FONT = 'Slabo 27px'

ALPHA_1 = 0.9
ALPHA_2 = 0.8

def radar_plot(player1_info: Dict[str, Any], player2_info: Dict[str, Any], stat_cols=None) -> BytesIO:
    p1_90s = float(player1_info['data']['Nineties'])
    p1 = f"{player1_info['name']} | {player1_info['team']} | 90's - {p1_90s:2}"
    if player2_info['name'] != None:
        p2_90s = float(player2_info['data']['Nineties'])
        p2 = f"{player2_info['name']} | {player2_info['team']} | 90's - {p2_90s:2}"
    else:
        p2 = ''

    radar_type = player1_info['radar_type']

    if stat_cols is None:
        stat_cols = RT_COLS[player1_info['radar_type']]
    percentile_cols = [f'_Percentile_{col}' for col in stat_cols]

    p1_data = player1_info['data']
    p2_data = player2_info['data']
    p1_pvals = [p1_data[col].item() for col in percentile_cols]
    p1_vals = [p1_data[col].item() for col in stat_cols]
    if(p2 == ''):
        p2_pvals = [0.0 for _ in range(len(p1_pvals))]
        p2_vals = [0.0 for _ in range(len(p1_vals))]
    else:
        p2_pvals = [p2_data[col].item() for col in percentile_cols]
        p2_vals = [p2_data[col].item() for col in stat_cols]

    arr1 = np.asarray(p1_pvals)
    arr2 = np.asarray(p2_pvals)
    N = len(p1_vals)
    bottom = 0.0
    theta, width = np.linspace(0.0, 2 * np.pi, N, endpoint=False, retstep=True)

    fig = plt.figure(figsize=(15, 9), dpi=100)
    ax = plt.subplot(121, polar=True)
    fig.set_facecolor(BGCOLOR)
    ax.patch.set_facecolor(BGCOLOR)
    ax.set_rorigin(-20)
    
    bars = ax.bar(
        theta, height=arr1,
        width=width,
        bottom=bottom,
        color=COLOR1, edgecolor=HIGHLIGHT_COLOR, zorder=1,
        alpha=ALPHA_1,
        linewidth=0.5
    )
    bars2 = ax.bar(
        theta, arr2,
        width=width,
        bottom=bottom,
        color=COLOR2, zorder=1,
        alpha=ALPHA_2,
        edgecolor=HIGHLIGHT_COLOR, linewidth=0.5
    )
    # for bar in bars:
    #     indx = bars.index(bar)
    #     if arr1[indx] <= arr2[indx]:
    #         bar.set_zorder(1.5)

    ax.set_rticks(np.arange(0.0, 120.0, 20.0))
    ax.set_thetagrids((theta+width/2) * 180 / np.pi)
    # ax.set_rlabel_position(-100)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.grid(zorder=10.0, color=HIGHLIGHT_COLOR, linestyle='--', linewidth=0.5)
    ax.spines['polar'].set_visible(False)
    # ax.set_rticks([])
    ticks = [str(i+1) for i in range(len(stat_cols))]
    ax.set_xticklabels([])
    rotations = np.rad2deg(theta)
    for x, bar, rotation, label in zip(theta, bars, rotations, stat_cols):
        lab = ax.text(x, 105, label, ha='center', va='center', color=TEXT_COLOR,
                      rotation=-rotation if rotation <= 90 or rotation >= 270 else 180 - rotation, 
                      rotation_mode='anchor', fontsize=10,
                      fontfamily=FONT)
    ax.spines["polar"].set_color(HIGHLIGHT_COLOR)
    ax.spines["polar"].set_linewidth(2)
    ax.set_yticklabels([])
    ax2 = plt.subplot(122)
    ax2.patch.set_facecolor(BGCOLOR)
    ax2.axis('off')
    ax2.text(0.15, 1.02, 'Stat (Percentile in bracket)', fontsize=20, color=TEXT_COLOR,
             fontfamily=FONT)
    for i in range(len(stat_cols)+1):
        ax2.text(0, 1.0-0.07*i, '|', fontsize=35, color=TEXT_COLOR, fontfamily=FONT)
    for i in range(32):
        ax2.text(0+0.04*i, 1, '_', fontsize=10, color=TEXT_COLOR, fontfamily=FONT)
    for i in range(len(stat_cols)):
        ax2.text(0.05, 0.95-0.07*i, str(i+1)+' :  '+ stat_cols[i], fontsize=15, color=TEXT_COLOR, fontfamily=FONT)
    for i in range(len(stat_cols)+1):
        ax2.text(0.75, 1.0-0.07*i, '|', fontsize=35, color=TEXT_COLOR, fontfamily=FONT)
    ax2.text(0.8, 1.02, 'Player 1', fontsize=20, color=COLOR1, fontfamily=FONT)
    for i in range(len(stat_cols)+1):
        ax2.text(0.99, 1.0-0.07*i, '|', fontsize=35, color=TEXT_COLOR, fontfamily=FONT)
    ax2.text(1.05, 1.02, 'Player 2', fontsize=20, color=COLOR2, fontfamily=FONT)
    for i in range(len(stat_cols)):
        ax2.text(0.8, 0.95-0.07*i, 
            str(round(p1_vals[i], 2))+'  ('+str(round(p1_pvals[i], 2))+ ')', 
            fontsize=15, color=TEXT_COLOR, fontfamily=FONT)
        if(p2 != ''):
            ax2.text(1.05, 0.95-0.07*i, str(round(p2_vals[i], 2))+'  ('+str(round(p2_pvals[i], 2)) + ')', 
                fontsize=15, color=TEXT_COLOR, fontfamily=FONT)

    
    season = player1_info['season']
    text1 = f"{radar_type}"
    text2 = f"({season} season)"
    long_title = False
    if len(text1) > len(text2):
        long_title = True
    fig_text(s=text1 + ('\n' if long_title else ' ') + text2, x=0.03, y=0.95,
             fontsize=25 if long_title else 30, color=EMP_COLOR, fontfamily=FONT, textalign='center')
    
    highlight_textprops = [{"color": COLOR1}, {"color": COLOR2}]
    fig_text(s=f"<{p1}>"+'\n'+f"<{p2}>", x=0.03, y=0.85 if long_title else 0.88,
             highlight_textprops=highlight_textprops,
             fontsize=20, color=TEXT_COLOR, fontfamily=FONT)
    
    ax2.text(0.01, 1.12, '\n\n' + 'Design idea :  Tom Worville / The Athletic/ Football Slices'
             +'\n\n'+'Code base :  Soumyajit Bose (@Soumyaj15209314)', 
             fontsize=15, color=TEXT_COLOR, fontfamily=FONT)
    
    fig_text(x = 0.48, y = 0.97,
        s=f'Presented to you by : <{CREDITS}>',
        fontsize=15, color=TEXT_COLOR, fontfamily=FONT,
        highlight_textprops=[{"color": EMP_COLOR, "weight": "bold", "fontsize": 20}])
    
    ax3 = fig.add_axes([0.79, 0.88, 0.1, 0.1])
    ax3.axis('off')
    ax3.imshow(FBREF_LOGO)
    ax4 = fig.add_axes([0.79, 0.83, 0.1, 0.1])
    ax4.axis('off')
    ax4.imshow(SB_LOGO)
    ax5 = fig.add_axes([0.9, 0.8, 0.1, 0.18])
    ax5.axis('off')
    ax5.imshow(FCD_QR)
    
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    fig.clear()
    plt.close(fig)
    
    gc.collect()
    
    return buffer
