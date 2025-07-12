from datetime import datetime

from grape.database.db import make_request

class Event:
    def __init__(self, wine_id, consumed_bottles, date=None, people=None, food=None, notes=None, event_id=None):
        self.id = event_id
        self.wine_id = wine_id
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.people = people
        self.food = food
        self.notes = notes
        self.consumed_bottles = consumed_bottles

    @staticmethod
    def add_event(event):
        query = """
            INSERT INTO events (wine_id, date, people, food, notes, consumed_bottles)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            event.wine_id, event.date, event.people, event.food, event.notes, event.consumed_bottles
        )
        make_request(query, params, fetch="none")

    @staticmethod
    def get_events_for_wine(wine_id):
        query = "SELECT id, wine_id, date, people, food, notes, consumed_bottles FROM events WHERE wine_id = ? ORDER BY date DESC"
        rows = make_request(query, (wine_id,), fetch="all")
        return [
            Event(row[1], date=row[2], people=row[3], food=row[4], notes=row[5],
                  consumed_bottles=row[6], event_id=row[0])
            for row in rows
        ]
