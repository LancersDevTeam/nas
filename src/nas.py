# nasクラスを作る。
import math
import os
from decimal import Decimal
from datetime import datetime
from configparser import ConfigParser, ExtendedInterpolation

from db import create_nas_record, load_send_nas_num, scan_user_receive_nas_num, load_latest_nas_gacha_record, create_nas_gacha_record
from utils import get_last_week_ref_timestamp, get_ref_timestamp
from gacha import roll_a_gacha

STAMP_CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
STAMP_CONFIG.read('stamp_config.ini')

NAS_LIMIT = int(os.environ['NAS_LIMIT'])
NAS_GACHA_COST = int(os.environ['NAS_GACHA_COST'])


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

    def sended_nas_num(self):
        ref_timestamp = get_ref_timestamp()
        sended_nas = load_send_nas_num(self.user_id, ref_timestamp)
        return sended_nas

    def nas_status(self):
        sended_nas = self.sended_nas_num()
        nas_bonus = self.nas_bonus()
        remain_nas = (NAS_LIMIT - sended_nas) + nas_bonus
        return remain_nas

    def chack_self_portrait(self, receive_user_id):
        if self.user_id == receive_user_id:
            return True
        return False

    def check_can_send_nas(self):
        if self.nas_status() > 0:
            return True
        return False

    def nas_stamp(self, receive_user_id, receive_user_name, stamp_name):
        if self.chack_self_portrait(receive_user_id) is True:
            print('self_portrait')
            return False

        if self.check_can_send_nas() is False:
            print('nas send limit')
            return False

        if STAMP_CONFIG.has_section(stamp_name) is False:
            print('this is not nas stamp')
            return False

        send_nas_num = STAMP_CONFIG.get(stamp_name, 'nas_num')
        for i in range(int(send_nas_num)):
            create_nas_record(self.user_id, self.user_name, receive_user_id, receive_user_name, 'stamp', self.team_id)

        return True

    def nas_message(self, receive_user_id, receive_user_name):
        if self.chack_self_portrait(receive_user_id) is True:
            print('self_portrait')
            return False

        if self.check_can_send_nas() is False:
            print('nas send limit')
            return False

        create_nas_record(self.user_id, self.user_name, receive_user_id, receive_user_name, 'message', self.team_id)
        return True

    def check_can_run_gacha(self):
        all_receive_nas_num = scan_user_receive_nas_num(self.user_id)
        latest_nas_gacha_record = load_latest_nas_gacha_record(self.user_id)
        if latest_nas_gacha_record == {}:
            return True
        already_used_nas_num = int(latest_nas_gacha_record['used_nas_num']) + NAS_GACHA_COST

        if already_used_nas_num >= all_receive_nas_num:
            print(all_receive_nas_num)
            return False

        return True

    def nas_gacha_status(self):
        all_receive_nas_num = scan_user_receive_nas_num(self.user_id)
        latest_nas_gacha_record = load_latest_nas_gacha_record(self.user_id)
        if latest_nas_gacha_record == {}:
            remain_nas_gacha = 1
            return remain_nas_gacha

        remain_nas_gacha = int((all_receive_nas_num - int(latest_nas_gacha_record['used_nas_num']))/NAS_GACHA_COST)
        return remain_nas_gacha

    def calc_until_next_time_nas_num(self):
        all_receive_nas_num = scan_user_receive_nas_num(self.user_id)
        latest_nas_gacha_record = load_latest_nas_gacha_record(self.user_id)
        if latest_nas_gacha_record == {}:
            until_next_time_nas_num = 0
            return until_next_time_nas_num

        diff_remain_used_num = all_receive_nas_num - int(latest_nas_gacha_record['used_nas_num'])

        until_next_time_nas_num = NAS_GACHA_COST - diff_remain_used_num if diff_remain_used_num < NAS_GACHA_COST else 0
        return until_next_time_nas_num

    def nas_gacha(self):
        now = datetime.now()
        all_receive_nas_num = scan_user_receive_nas_num(self.user_id)
        latest_nas_gacha_record = load_latest_nas_gacha_record(self.user_id)

        gacha_result = roll_a_gacha()
        if latest_nas_gacha_record == {}:
            already_used_nas_num = 0
            has_tickets = {}
            if gacha_result != '':
                has_tickets[gacha_result] = 1
        else:
            already_used_nas_num = int(latest_nas_gacha_record['used_nas_num']) + NAS_GACHA_COST
            has_tickets = latest_nas_gacha_record['has_tickets']
            if gacha_result != '':
                has_tickets[gacha_result] = has_tickets.get(gacha_result, 0) + 1

        create_nas_gacha_record(self.user_id, Decimal(now.timestamp()), all_receive_nas_num, already_used_nas_num, has_tickets)
        return gacha_result

    def check_nas_gacha_tickets(self):
        latest_nas_gacha_record = load_latest_nas_gacha_record(self.user_id)
        if latest_nas_gacha_record == {}:
            ticket_dict = {}
            return ticket_dict

        ticket_dict = latest_nas_gacha_record['has_tickets']
        return ticket_dict

    def use_nas_gacha_tickets(self, ticket_name):
        latest_nas_gacha_record = load_latest_nas_gacha_record(self.user_id)
        if latest_nas_gacha_record == {}:
            print('empty gacha record')
            return False

        has_tickets = latest_nas_gacha_record['has_tickets']
        if ticket_name not in has_tickets.keys():
            print('not exist the ticket in your has tickets')
            return False

        now = datetime.now()
        all_receive_nas_num = scan_user_receive_nas_num(self.user_id)
        already_used_nas_num = latest_nas_gacha_record['used_nas_num']
        has_tickets[ticket_name] -= 1

        if has_tickets[ticket_name] <= 0:
            del has_tickets[ticket_name]

        create_nas_gacha_record(self.user_id, Decimal(now.timestamp()), all_receive_nas_num, already_used_nas_num, has_tickets)
