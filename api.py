import requests

# https://www.thebluealliance.com/apidocs

class BlueAllianceAPI:
    BASE_URL = "https://www.thebluealliance.com/api/v3"

    def check(self, response):
        if 'Error' in response:
            return None
        return response

    def __init__(self, auth_key):
        self.headers = {"X-TBA-Auth-Key": auth_key}

    def get_teams_at_event(self, event_key):
        url = f"{self.BASE_URL}/event/{event_key}/teams"
        response = requests.get(url, headers=self.headers)
        return self.check(response.json())

    def get_events_for_team(self, team_key):
        url = f"{self.BASE_URL}/team/{team_key}/events"
        response = requests.get(url, headers=self.headers)
        return self.check(response.json())
    
    def get_event_key_from_name(self, year, event_name):
        url = f"{self.BASE_URL}/events/{year}/simple"
        response = requests.get(url, headers=self.headers)
        events = self.check(response.json())
        if not events:
            return None
        for event in events:
            if event['name'].lower() == event_name.lower():
                return event

    def get_event_winners(self, event_key):
        url = f"{self.BASE_URL}/event/{event_key}/teams/statuses"
        response = requests.get(url, headers=self.headers)
        statuses = self.check(response.json())
        if not statuses:
            return None
        winners = []
        for team, status in statuses.items():
            playoff = status.get('playoff')
            if playoff and playoff.get('status') == "won":
                winners.append(team)
        return winners if winners else None

    def get_team_ranking_at_event(self, event_key, team_key):
        url = f"{self.BASE_URL}/event/{event_key}/teams/statuses"
        response = requests.get(url, headers=self.headers)
        statuses = response.json()
        if team_key in statuses:
            team_info = statuses[team_key]
            rank = team_info['qual']['ranking']['rank']
            overall_record = team_info['qual']['ranking']['record']
            return rank, overall_record
        return None

    def get_event_info(self, event_key):
        url = f"{self.BASE_URL}/event/{event_key}"
        response = requests.get(url, headers=self.headers)
        return self.check(response.json())
    
    def get_team_info(self, team_key):
        url = f"{self.BASE_URL}/team/{team_key}"
        response = requests.get(url, headers=self.headers)
        return self.check(response.json())

# midwest regional is "2024ilch"
# 4645 is "frc4645"