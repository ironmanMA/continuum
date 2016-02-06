__author__ = 'mohammad'

from boto.s3.connection import S3Connection
from dynamo_io import put_item
from datetime import datetime, timedelta
import simplejson as json
import gzip
import os


AWS_ACCESS_KEY = 'AKIAJ6XUO5KUSL2ZQKSA'
AWS_SECRET_KEY = '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'

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
bb_bucket = conn.get_bucket('bb-instrumentation')

date_dd_mm_yyyy = datetime.today().strftime('%Y-%m-%d')

login_metric = {}
client_metric = {"www.staples.com": 0, "www.officedepot.com": 0, "www.zalando.de": 0, "www.homedepot.com": 0, "www.staples.ca": 0,"jet.com": 0, "www.searspartsdirect.com": 0, "www.sears.com": 0}
user_metric = {}
action_metric = {}
date_metric = {}

days_this_week ={}
hits_this_week = {"total": 0, "action":{}, "users":{}, "clients": {"www.staples.com": 0, "www.officedepot.com": 0, "www.zalando.de": 0, "www.homedepot.com": 0, "www.staples.ca": 0,"jet.com": 0, "www.searspartsdirect.com": 0, "www.sears.com": 0}}
days_prev_1_week = {}
hits_prev_1_week= {"total": 0, "action":{}, "users":{}, "clients": {"www.staples.com": 0, "www.officedepot.com": 0, "www.zalando.de": 0, "www.homedepot.com": 0, "www.staples.ca": 0,"jet.com": 0, "www.searspartsdirect.com": 0, "www.sears.com": 0}}
days_prev_2_week = {}
hits_prev_2_week = {"total": 0, "action":{}, "users":{}, "clients": {"www.staples.com": 0, "www.officedepot.com": 0, "www.zalando.de": 0, "www.homedepot.com": 0, "www.staples.ca": 0,"jet.com": 0, "www.searspartsdirect.com": 0, "www.sears.com": 0}}
days_prev_3_week = {}
hits_prev_3_week = {"total": 0, "action":{}, "users":{}, "clients": {"www.staples.com": 0, "www.officedepot.com": 0, "www.zalando.de": 0, "www.homedepot.com": 0, "www.staples.ca": 0,"jet.com": 0, "www.searspartsdirect.com": 0, "www.sears.com": 0}}

def create_stats(data, hit_date):

    # date metric
    if hit_date in date_metric:
        date_metric[hit_date] += 1

    if hit_date in days_this_week:
        days_this_week[hit_date] += 1
        hits_this_week["total"] += 1

    if hit_date in days_prev_1_week:
        days_prev_1_week[hit_date] += 1
        hits_prev_1_week["total"] += 1

    if hit_date in days_prev_2_week:
        days_prev_2_week[hit_date] += 1
        hits_prev_2_week["total"] += 1

    if hit_date in days_prev_3_week:
        days_prev_3_week[hit_date] += 1
        hits_prev_3_week["total"] += 1

    for metric_pos in range(0, len(data)):
        metric = data[metric_pos].split('=')
        metric_name = metric[0]
        metric_variant = metric[1].replace("/", "")
        if metric_name == 'loggedIn':
            if metric_variant in login_metric:
                login_metric[metric_variant] += 1
            else:
                login_metric[metric_variant] = 1
        elif metric_name == 'client':
            if metric_variant in client_metric:
                client_metric[metric_variant] += 1
            else:
                print metric_variant, 'metric_variant not in', client_metric

            if hit_date in days_this_week:
                if metric_variant in hits_this_week["clients"]:
                    hits_this_week["clients"][metric_variant] += 1

            if hit_date in days_prev_1_week:
                if metric_variant in hits_prev_1_week["clients"]:
                    hits_prev_1_week["clients"][metric_variant] += 1

            if hit_date in days_prev_2_week:
                if metric_variant in hits_prev_2_week["clients"]:
                    hits_prev_2_week["clients"][metric_variant] += 1

            if hit_date in days_prev_3_week:
                if metric_variant in hits_prev_3_week["clients"]:
                    hits_prev_3_week["clients"][metric_variant] += 1

        elif metric_name == 'username':
            if metric_variant in user_metric:
                user_metric[metric_variant] += 1
            else:
                user_metric[metric_variant] = 1

            if hit_date in days_this_week:
                if metric_variant in hits_this_week["users"]:
                    hits_this_week["users"][metric_variant] += 1
                else:
                    hits_this_week["users"][metric_variant] = 1

            if hit_date in days_prev_1_week:
                if metric_variant in hits_prev_1_week["users"]:
                    hits_prev_1_week["users"][metric_variant] += 1
                else:
                    hits_prev_1_week["users"][metric_variant] = 1

            if hit_date in days_prev_2_week:
                if metric_variant in hits_prev_2_week["users"]:
                    hits_prev_2_week["users"][metric_variant] += 1
                else:
                    hits_prev_2_week["users"][metric_variant] = 1

            if hit_date in days_prev_3_week:
                if metric_variant in hits_prev_3_week["users"]:
                    hits_prev_3_week["users"][metric_variant] += 1
                else:
                    hits_prev_3_week["users"][metric_variant] = 1

        elif metric_name == 'action':
            if metric_variant in action_metric:
                action_metric[metric_variant] += 1
            else:
                action_metric[metric_variant] = 1

            if hit_date in days_this_week:
                if metric_variant in hits_this_week["action"]:
                    hits_this_week["action"][metric_variant] += 1
                else:
                    hits_this_week["action"][metric_variant] = 1

            if hit_date in days_prev_1_week:
                if metric_variant in hits_prev_1_week["action"]:
                    hits_prev_1_week["action"][metric_variant] += 1
                else:
                    hits_prev_1_week["action"][metric_variant] = 1

            if hit_date in days_prev_2_week:
                if metric_variant in hits_prev_2_week["action"]:
                    hits_prev_2_week["action"][metric_variant] += 1
                else:
                    hits_prev_2_week["action"][metric_variant] = 1

            if hit_date in days_prev_3_week:
                if metric_variant in hits_prev_3_week["action"]:
                    hits_prev_3_week["action"][metric_variant] += 1
                else:
                    hits_prev_3_week["action"][metric_variant] = 1

        else:
            print "NOTA"

    return "Done"


def run(look_back_days):
    for key in bb_bucket.list():
        act_date = datetime.strptime(str(date_dd_mm_yyyy), "%Y-%m-%d").date()
        log_date = datetime.strptime(key.last_modified.split('T')[0], "%Y-%m-%d").date()
        if ("cf-logs/" in key.name) and (abs((act_date - log_date).days) < look_back_days):
            print key.name, key.size, key.last_modified
            key.get_contents_to_filename(key.name.split('/')[1])
            # process this
            with gzip.open(key.name.split('/')[1], 'rb') as fin:
                next(fin)
                next(fin)
                for line in fin:
                    # print line.split('\t')[0]
                    try:
                        create_stats(line.split('\t')[11].split('&'), line.split('\t')[0])
                    except Exception:
                        pass

            os.remove(key.name.split('/')[1])
    update_time = datetime.today().strftime('%H:%M:%S %d-%m-%Y')+" UTC"
    final_json = json.dumps({'users': user_metric,
                             'clients': client_metric,
                             'action': action_metric,
                             'hits_by_date': date_metric,
                             'update_time': update_time,
                             'stats_by_week': {"week-0": hits_this_week, "week-1": hits_prev_1_week, "week-2": hits_prev_2_week, "week-3": hits_prev_3_week,}})
    put_item('boombar', datetime.today().strftime('%d-%m-%Y'), final_json)
    print final_json
    return final_json

def generate_dates():
    curr_date_num = datetime.today().weekday() # mon is 0, sun is 6
    look_back_days = (curr_date_num +1) + 21 # 3-weeks + this-week

    for day_num in range(0,curr_date_num+1):
        prevday = datetime.now() - timedelta(days=day_num)
        days_this_week[prevday.strftime('%Y-%m-%d')] = 0
        date_metric[prevday.strftime('%Y-%m-%d')] = 0
    print 'dates this week', days_this_week

    for day_num in range(curr_date_num+1,curr_date_num+8):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_1_week[prevday.strftime('%Y-%m-%d')] = 0
        date_metric[prevday.strftime('%Y-%m-%d')] = 0
    print 'days week ago', days_prev_1_week

    for day_num in range(curr_date_num+8,curr_date_num+15):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_2_week[prevday.strftime('%Y-%m-%d')] = 0
        date_metric[prevday.strftime('%Y-%m-%d')] = 0
    print 'days 2 weeks ago', days_prev_2_week

    for day_num in range(curr_date_num+15,curr_date_num+22):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_3_week[prevday.strftime('%Y-%m-%d')] = 0
        date_metric[prevday.strftime('%Y-%m-%d')] = 0
    print 'days 3 weeks ago', days_prev_3_week

    return look_back_days

if __name__ == '__main__':
    look_back_days = generate_dates()
    run(look_back_days)
