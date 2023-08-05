import requests
from pysmashgg import exceptions, tournaments, brackets, players, events

class SmashGG(object):
    def __init__(self, key):
        self.key = key
        self.header = {"Authorization": "Bearer " + key}
        
    def set_key_and_header(self, new_key):
        self.key = new_key
        self.header = {"Authorization": "Bearer " + new_key}

    def print_key(self):
        print(self.key)

    def print_header(self):
        print(self.header)

    # Event_id for a tournament
    def tournament_show_event_id(self, tournament_name, event_name):
        return tournaments.get_event_id(tournament_name, event_name, self.header)

    # Metadata for a tournament
    def tournament_show(self, tournament_name):
        return tournaments.show(tournament_name, self.header)

    # Metadata for a tournament with a bracket
    def tournament_show_with_brackets(self, tournament_name, event_name):
        return tournaments.show_with_brackets(tournament_name, event_name, self.header)

    # Same as tournament_show_with_brackets but for all brackets
    def tournament_show_with_brackets_all(self, tournament_name):
        return tournaments.show_with_brackets_all(tournament_name, self.header)

    # List of events for a tournament
    def tournament_show_events(self, tournament_name):
        return tournaments.show_events(tournament_name, self.header)

    # List of sets for an event
    def tournament_show_sets(self, tournament_name, event_name, page_num):
        return tournaments.show_sets(tournament_name, event_name, page_num, self.header)

    # List of entrants for an event
    def tournament_show_entrants(self, tournament_name, event_name, page_num):
        return tournaments.show_entrants(tournament_name, event_name, page_num, self.header)
    
    # Bracket info for an event at a tournament
    def tournament_show_event_brackets(self, tournament_name, event_name):
        return tournaments.show_event_brackets(tournament_name, event_name, self.header)
    
    # Bracket info for all events at a tournament
    def tournament_show_all_event_brackets(self, tournament_name):
        return tournaments.show_all_event_brackets(tournament_name, self.header)

    # All sets from an entrant at an event
    def tournament_show_entrant_sets(self, tournament_name, event_name, entrant_name):
        return tournaments.show_entrant_sets(tournament_name, event_name, entrant_name, self.header)

    # All sets between two entrants at an event
    def tournament_show_head_to_head(self, tournament_name, event_name, entrant1_name, entrant2_name):
        return tournaments.show_head_to_head(tournament_name, event_name, entrant1_name, entrant2_name, self.header)

    # All tournaments with events (of a certain game) of a minimum size in between two unix timestamps
    def tournament_show_event_by_game_size_dated(self, num_entrants, videogame_id, after, before, page_num):
        return tournaments.show_event_by_game_size_dated(num_entrants, videogame_id, after, before, page_num, self.header)

    # Results of an event with only entrant name, id, and placement
    def tournament_show_lightweight_results(self, tournament_name, event_name, page_num):
        return tournaments.show_lightweight_results(tournament_name, event_name, page_num, self.header)

    # All entrants in a bracket (phaseGroup) at a tournament
    def bracket_show_entrants(self, bracket_id, page_num):
        return brackets.bracket_show_entrants(bracket_id, page_num, self.header)

    # All sets in a bracket (phaseGroup) at a tournament
    def bracket_show_sets(self, bracket_id, page_num):
        return brackets.bracket_show_sets(bracket_id, page_num, self.header)

    # Player metadata
    def player_show_info(self, player_id):
        return players.show_info(player_id, self.header)

    # All tournaments by a player (where they registered with their smash.gg account)
    def player_show_tournaments(self, player_id, page_num):
        return players.show_tournaments(player_id, page_num, self.header)
    
    # All tournaments by a player for a certain game
    # Use https://docs.google.com/spreadsheets/d/1l-mcho90yDq4TWD-Y9A22oqFXGo8-gBDJP0eTmRpTaQ/
    # to find the game_id you're looking for
    def player_show_tournaments_for_game(self, player_id, player_name, videogame_id, page_num):
        return players.show_tournaments_for_game(player_id, player_name, videogame_id, page_num, self.header)

    # List of sets for an event
    def event_show_sets(self, event_id, page_num):
        return events.show_sets(event_id, page_num, self.header)

    # List of entrants for an event
    def event_show_entrants(self, event_id, page_num):
        return events.show_entrants(event_id, page_num, self.header)

    # All sets from an entrant at an event
    def event_show_entrant_sets(self, event_id, entrant_name):
        return events.show_entrant_sets(event_id, entrant_name, self.header)
    
    # All sets between two entrants at an event
    def event_show_head_to_head(self, event_id, entrant1_name, entrant2_name):
        return events.show_head_to_head(event_id, entrant1_name, entrant2_name, self.header)

    # Results of an event with only entrant name, id, and placement
    def event_show_lightweight_results(self, event_id, page_num):
        return events.show_lightweight_results(event_id, page_num, self.header)