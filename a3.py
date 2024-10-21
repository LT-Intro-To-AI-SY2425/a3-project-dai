from api import BlueAllianceAPI
from match import match
from typing import List, Callable, Tuple

api = BlueAllianceAPI("YZUHjjkawrWXVjXfKJHzGKgTecWKNgcAoe48bzO23gq20K1vR0Ww5m9k7CJADdnI")

def get_event_key_from_name(matches: List[str]) -> List[str]:
    event_year = matches[0][:4]
    event_name = matches[0][5:]
    event = api.get_event_key_from_name(event_year, event_name)
    if event:
        return [event['key']]
    return ["No event found"]

def list_teams_at_event(matches: List[str]) -> List[str]:
    event_key = matches[0]
    teams = api.get_teams_at_event(event_key)
    if teams:
        return [team['nickname'] for team in teams]
    return ["No teams found"]

def list_events_for_team(matches: List[str]) -> List[str]:
    team_key = matches[0]
    events = api.get_events_for_team(team_key)
    if events:
        return [event['name'] for event in events]
    return ["No events found"]

def get_event_winner(matches: List[str]) -> List[str]:
    event_key = matches[0]
    winners = api.get_event_winners(event_key)
    if winners:
        return winners
    return ["No winner found"]

def get_team_ranking_at_event(matches: List[str]) -> List[str]:
    event_key = matches[1]
    team_key = matches[0]
    ranking = api.get_team_ranking_at_event(event_key, team_key)
    if ranking:
        record = ranking[1]
        record_str = f"{record['wins']} wins, {record['losses']} losses, {record['ties']} ties"
        return [f"{team_key} ranked {ranking[0]} at {event_key} with a record of {record_str}."]
    return ["No ranking found"]

def get_event_info(matches: List[str]) -> List[str]:
    event_key = matches[0]
    event = api.get_event_info(event_key)
    if event:
        # return [event['name'], event['location_name'], event['start_date'], event['end_date']]
        return [f"The {event['name']} was hosted at {event['location_name']} and ran from {event['start_date']} to {event['end_date']}."]
    return ["No event found"]

# Define pattern-action list
pa_list: List[Tuple[List[str], Callable[[List[str]], List[str]]]] = [
    (str.split("what is the identifier for %"), get_event_key_from_name),
    (str.split("list teams that played at _"), list_teams_at_event),
    (str.split("list events that _ played at"), list_events_for_team),
    (str.split("who won _"), get_event_winner),
    (str.split("what place did _ rank at _"), get_team_ranking_at_event),
    (str.split("tell me about _"), get_event_info),
    (["bye"], lambda _: exit())
]

def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    for pattern, action in pa_list:
        matches = match(pattern, src)
        if matches is not None:
            answers = action(matches)
            return answers if answers else ["No answers"]
    return ["I don't understand"]

def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully.
    """
    print("Welcome to the FRC chatbot!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nGoodbye!\n")

if __name__ == "__main__":
    query_loop()