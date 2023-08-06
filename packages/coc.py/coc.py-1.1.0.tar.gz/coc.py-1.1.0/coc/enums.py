"""
MIT License

Copyright (c) 2019-2020 mathsman5133

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from enum import Enum


class Role(Enum):
    """Enum to map a player's role in the clan."""

    member = "member"
    elder = "admin"
    co_leader = "coLeader"
    leader = "leader"

    def __str__(self):
        return self.in_game_name

    @property
    def in_game_name(self) -> str:
        """Get a neat client-facing string value for the role."""
        lookup = {Role.member: "Member", Role.elder: "Elder", Role.co_leader: "Co-Leader", Role.leader: "Leader"}
        return lookup[self]


class WarRound(Enum):
    previous_war = 0
    current_war = 1
    current_preparation = 2

    def __str__(self):
        return self.name


ELIXIR_TROOP_ORDER = [
    "Barbarian",
    "Archer",
    "Giant",
    "Goblin",
    "Wall Breaker",
    "Balloon",
    "Wizard",
    "Healer",
    "Dragon",
    "P.E.K.K.A",
    "Baby Dragon",
    "Miner",
    "Electro Dragon",
    "Yeti",
]

DARK_ELIXIR_TROOP_ORDER = [
    "Minion",
    "Hog Rider",
    "Valkyrie",
    "Golem",
    "Witch",
    "Lava Hound",
    "Bowler",
    "Ice Golem",
    "Headhunter",
]

SIEGE_MACHINE_ORDER = [
    "Wall Wrecker",
    "Battle Blimp",
    "Stone Slammer",
    "Siege Barracks",
    "Log Launcher",
]

SUPER_TROOP_ORDER = [
    "Super Barbarian",
    "Super Archer",
    "Super Giant",
    "Sneaky Goblin",
    "Super Wall Breaker",
    "Super Wizard",
    "Inferno Dragon",
    "Super Minion",
    "Super Valkyrie",
    "Super Witch",
    "Ice Hound",
]

# TODO: when SC fixes Super Troops in API add them here
HOME_TROOP_ORDER = ELIXIR_TROOP_ORDER + DARK_ELIXIR_TROOP_ORDER + SIEGE_MACHINE_ORDER

BUILDER_TROOPS_ORDER = [
    "Raged Barbarian",
    "Sneaky Archer",
    "Boxer Giant",
    "Beta Minion",
    "Bomber",
    "Baby Dragon",
    "Cannon Cart",
    "Night Witch",
    "Drop Ship",
    "Super P.E.K.K.A",
    "Hog Glider",
]

ELIXIR_SPELL_ORDER = [
    "Lightning Spell",
    "Healing Spell",
    "Rage Spell",
    "Jump Spell",
    "Freeze Spell",
    "Clone Spell",
    "Invisibility Spell",
]

DARK_ELIXIR_SPELL_ORDER = [
    "Poison Spell",
    "Earthquake Spell",
    "Haste Spell",
    "Skeleton Spell",
    "Bat Spell",
]

SPELL_ORDER = ELIXIR_SPELL_ORDER + DARK_ELIXIR_SPELL_ORDER

HERO_ORDER = ["Barbarian King", "Archer Queen", "Grand Warden", "Royal Champion", "Battle Machine"]

ACHIEVEMENT_ORDER = [
    "Bigger Coffers",
    "Get those Goblins!",
    "Bigger & Better",
    "Nice and Tidy",
    "Release the Beasts",
    "Gold Grab",
    "Elixir Escapade",
    "Sweet Victory!",
    "Empire Builder",
    "Wall Buster",
    "Humiliator",
    "Union Buster",
    "Conqueror",
    "Unbreakable",
    "Friend in Need",
    "Mortar Mauler",
    "Heroic Heist",
    "League All-Star",
    "X-Bow Exterminator",
    "Firefighter",
    "War Hero",
    "Treasurer",
    "Anti-Artillery",
    "Sharing is caring",
    "Games Champion",
    "Get those other Goblins!",
    "Dragon Slayer",
    "War League Legend",
    "Keep your village safe",
    "Well Seasoned",
    "Shattered and Scattered",
    "Master Engineering",
    "Next Generation Model",
    "Un-Build It",
    "Champion Builder",
    "High Gear",
    "Hidden Treasures",
]

UNRANKED_LEAGUE_DATA = {
    "id": 29000000,
    "name": "Unranked",
    "iconUrls": {
        "small": "https://api-assets.clashofclans.com/leagues/72/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png",
        "tiny": "https://api-assets.clashofclans.com/leagues/36/e--YMyIexEQQhE4imLoJcwhYn6Uy8KqlgyY3_kFV6t4.png",
    },
}
