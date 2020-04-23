# nasクラスを作る。
import math
import os

from .db import load_send_nas_num
from .utils import get_last_week_ref_timestamp, get_ref_timestamp

NAS_LIMIT = int(os.environ['NAS_LIMIT'])


class Nas:
    def __init__(self, user_id, user_name, team_id):
        self.user_id = user_id
        self.user_name = user_name
        self.team_id = team_id

    def nas_bonus(self):
        this_week_ref_timestamp = get_ref_timestamp()
        this_week_send_nas = load_send_nas_num(self.user_id, this_week_ref_timestamp)

        last_week_ref_timestamp = get_last_week_ref_timestamp()
        last_week_send_nas = load_send_nas_num(self.user_id, last_week_ref_timestamp)

        nas_bonus = math.ceil((last_week_send_nas - this_week_send_nas) * 0.2)
        return nas_bonus

    def nas_status(self):
        ref_timestamp = get_ref_timestamp()
        sended_nas = load_send_nas_num(self.user_id, ref_timestamp)
        nas_bonus = self.nas_bonus()
        remain_nas = (NAS_LIMIT - sended_nas) + nas_bonus
        return remain_nas
