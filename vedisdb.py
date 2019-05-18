from vedis import Vedis
import config

def get_user_state(user_id):
    with Vedis(config.DB_USER_STATE) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return None


def set_user_state(user_id, state):
    with Vedis(config.DB_USER_STATE) as db:
        db[user_id] = state
    