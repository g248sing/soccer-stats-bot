from datetime import datetime
from dataclasses import dataclass

import nextcord
import structlog

BARCA_COLOR = 0xa70042
# Lazy's server, FCD, Discoredlona bot server
TESTING_GUILD_IDS = [917711721253179403, 759319329979760671, 911280124995993600]

log = structlog.get_logger(__name__)


class Embed(nextcord.Embed):
    def __init__(self, author=None, show_time=False, **kwargs):
        kwargs['color'] = kwargs.get('color', BARCA_COLOR)
        if show_time:
            kwargs['timestamp'] = datetime.utcnow()
        super().__init__(**kwargs)
        if author:
            super().set_footer(text=f"Requested by {author.display_name}", icon_url=author.display_avatar.url)


@dataclass
class Emoji:
    lock = '\U0001f512'
    unlock = '\U0001f513'
    first_place = '\U0001F947'
    second_place = '\U0001F948'
    third_place = '\U0001F949'
    small_blue_diamond = '\U0001F539'
    medals = [first_place, second_place, third_place]
    left_arrow = '\U000025c1'
    right_arrow = '\U000025b7'
    cheeky = '<:CHEEKYSMILE:781089853525196820>'
    hehe = '<:HEHEHE:840970835569016852>'


class Prediction:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.is_running = True
        self.votes = {}
        self.message = None
        self.embed = None
        self.gd_pts = 7
        self.exact_bonus = 5
        self.exact_pts = 12

    @property
    def match(self):
        return self.team1 + " vs " + self.team2

    def add_vote(self, uid: str, score1: int, score2: int):
        self.votes[uid] = (score1, score2)

    def get_winners_points(self, score1, score2):
        points = {}
        for uid, vote in self.votes.items():
            s1, s2 = vote
            points[uid] = self.gd_pts * int(s1 - s2 == score1 - score2) \
                          + self.exact_bonus * int(s1 == score1 and s2 == score2)
        return points

    def get_match_embed(self):
        self.embed = Embed(title=f"{self.match}")
        members = "\n".join([f"<@!{uid}>" for uid in self.votes])
        score = "\n".join([f"{vote[0]}  -  {vote[1]}" for vote in self.votes.values()])

        if len(self.votes) != 0:
            self.embed.add_field(name="User", value=members)
            self.embed.add_field(name=f"Prediction", value=score)
        return self.embed

    def get_winners_embed(self, points):
        def msg(lst):
            return '\n'.join([f"<@!{uid}>" for uid in lst])

        exact = [uid for uid, pt in points.items() if pt == self.exact_pts]
        correct_gd = [uid for uid, pt in points.items() if pt == self.gd_pts]

        embed = Embed(title=f"Winners for {self.match}")
        if exact:
            embed.add_field(name=f"Exact Prediction ({self.exact_pts} points)", value=msg(exact), inline=False)
        if correct_gd:
            embed.add_field(name=f"Correct GD ({self.gd_pts} points)", value=msg(correct_gd), inline=False)
        elif len(embed.fields) == 0:
            embed.description = "WTF!! nobody got it right!"
        return embed

    async def change_status(self, lock: bool):
        if self.is_running == lock:
            self.is_running = not lock
            self.embed.title = "[Locked] " + self.match if lock else self.match
            self.embed.description = "Status: " + ("Closed" if lock else "Running")
            await self.message.edit(embed=self.embed)


class Leaderboard:
    def __init__(self, db):
        self.db = db
        self.points = {}
        points = self.db.find_by_id("points")
        if points:
            points.pop("_id")
            self.points = {int(uid): pt for uid, pt in points.items()}

    async def update(self, new_pts):
        all_uids = set().union(self.points.keys(), new_pts.keys())
        self.points = {
            uid: self.points.get(uid, 0) + new_pts.get(uid, 0)
            for uid in all_uids
        }
        log.info("Updating leaderboard", updated_points=self.points, all_uids=all_uids)
        await self.db.add_or_update("points", self.points)

    def get_lb_embed(self, page=0):
        top = [uid for uid in sorted(self.points, key=self.points.get, reverse=True)]
        top = top[page:page + 10]
        msg = ""
        if page == 0:
            msg = '\n'.join([
                Emoji.medals[i] + f" <@!{top[i]}> {self.points[top[i]]} points"
                for i in range(min(3, len(self.points)))
            ]) + "\n"
            top = top[3:]
        msg += '\n'.join([
            Emoji.small_blue_diamond + f" <@!{uid}> {self.points[uid]} points"
            for uid in top
        ])
        return Embed(title="Prediction Leaderboard", description=msg, show_time=True)
