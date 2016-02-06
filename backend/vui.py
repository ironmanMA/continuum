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
bb_bucket = conn.get_bucket('adhoc-matching')

# look_back_days = 7
date_dd_mm_yyyy = datetime.today().strftime('%Y-%m-%d')

user_metric = {}
client_complete_metric = {}
client_daily_metric = {}

date_metric = {}

days_this_week ={}
days_prev_1_week = {}
days_prev_2_week = {}
days_prev_3_week = {}

metrics_this_week = {"validations": 0, "users": 0, "clients": 0, "users_dist": {}, "clients_dist": {}}
metrics_prev_1_week = {"validations": 0, "users": 0, "clients": 0, "users_dist": {}, "clients_dist": {}}
metrics_prev_2_week = {"validations": 0, "users": 0, "clients": 0, "users_dist": {}, "clients_dist": {}}
metrics_prev_3_week = {"validations": 0, "users": 0, "clients": 0, "users_dist": {}, "clients_dist": {}}

def generate_stats(data, hit_date):
    # only process submit_skus
    if "submit_skus" in data[0].split('=')[1]:
        if hit_date in client_daily_metric:
            client_daily_metric[hit_date]['total'] += 1
        else:
            client_daily_metric[hit_date] = {}
            client_daily_metric[hit_date]['total'] = 1
            client_daily_metric[hit_date]['clients'] = {}
            client_daily_metric[hit_date]['users'] = {}

        for metric_pos in range(0, len(data)):
            metric = data[metric_pos].split('=')
            metric_name = metric[0]
            metric_variant = metric[1]
            if metric_name == 'client':
                if metric_variant in client_daily_metric[hit_date]['clients']:
                    client_daily_metric[hit_date]['clients'][metric_variant] += 1
                else:
                    client_daily_metric[hit_date]['clients'][metric_variant] = 1
                if metric_variant in client_complete_metric:
                    client_complete_metric[metric_variant] += 1
                else:
                    client_complete_metric[metric_variant] = 1
            elif metric_name == 'username':
                if metric_variant.split('@')[0] in client_daily_metric[hit_date]['users']:
                    client_daily_metric[hit_date]['users'][metric_variant.split('@')[0]] += 1
                else:
                    client_daily_metric[hit_date]['users'][metric_variant.split('@')[0]] = 1
                if metric_variant.split('@')[0] in user_metric:
                    user_metric[metric_variant.split('@')[0]] += 1
                else:
                    user_metric[metric_variant.split('@')[0]] = 1

    return "done"

def total_validations( repo_structure ):
    commit_count = 0
    for repo_name in repo_structure:
        commit_count += repo_structure[repo_name]
    return commit_count

def etl_metrics():

    for date in client_daily_metric:
        date_metric[date] = {"validations": client_daily_metric[date]["total"], "users": len(client_daily_metric[date]["users"]), "clients": len(client_daily_metric[date]["clients"])}

        if date in days_this_week:
            for user in client_daily_metric[date]["users"]:
                if user in metrics_this_week["users_dist"]:
                    metrics_this_week["users_dist"][user] += client_daily_metric[date]["users"][user]
                else:
                    metrics_this_week["users_dist"][user] = client_daily_metric[date]["users"][user]
            for client in client_daily_metric[date]["clients"]:
                if client in metrics_this_week["clients_dist"]:
                    metrics_this_week["clients_dist"][client] += client_daily_metric[date]["clients"][client]
                else:
                    metrics_this_week["clients_dist"][client] = client_daily_metric[date]["clients"][client]
        elif date in days_prev_1_week:
            for user in client_daily_metric[date]["users"]:
                if user in metrics_prev_1_week["users_dist"]:
                    metrics_prev_1_week["users_dist"][user] += client_daily_metric[date]["users"][user]
                else:
                    metrics_prev_1_week["users_dist"][user] = client_daily_metric[date]["users"][user]
            for client in client_daily_metric[date]["clients"]:
                if client in metrics_prev_1_week["clients_dist"]:
                    metrics_prev_1_week["clients_dist"][client] += client_daily_metric[date]["clients"][client]
                else:
                    metrics_prev_1_week["clients_dist"][client] = client_daily_metric[date]["clients"][client]
        elif date in days_prev_2_week:
            for user in client_daily_metric[date]["users"]:
                if user in metrics_prev_2_week["users_dist"]:
                    metrics_prev_2_week["users_dist"][user] += client_daily_metric[date]["users"][user]
                else:
                    metrics_prev_2_week["users_dist"][user] = client_daily_metric[date]["users"][user]
            for client in client_daily_metric[date]["clients"]:
                if client in metrics_prev_2_week["clients_dist"]:
                    metrics_prev_2_week["clients_dist"][client] += client_daily_metric[date]["clients"][client]
                else:
                    metrics_prev_2_week["clients_dist"][client] = client_daily_metric[date]["clients"][client]
        elif date in days_prev_3_week:
            for user in client_daily_metric[date]["users"]:
                if user in metrics_prev_3_week["users_dist"]:
                    metrics_prev_3_week["users_dist"][user] += client_daily_metric[date]["users"][user]
                else:
                    metrics_prev_3_week["users_dist"][user] = client_daily_metric[date]["users"][user]
            for client in client_daily_metric[date]["clients"]:
                if client in metrics_prev_3_week["clients_dist"]:
                    metrics_prev_3_week["clients_dist"][client] += client_daily_metric[date]["clients"][client]
                else:
                    metrics_prev_3_week["clients_dist"][client] = client_daily_metric[date]["clients"][client]

    metrics_this_week["validations"] = total_validations(metrics_this_week["clients_dist"])
    metrics_this_week["users"] = len(metrics_this_week["users_dist"])
    metrics_this_week["clients"] = len(metrics_this_week["clients_dist"])

    metrics_prev_1_week["validations"] = total_validations(metrics_prev_1_week["clients_dist"])
    metrics_prev_1_week["users"] = len(metrics_prev_1_week["users_dist"])
    metrics_prev_1_week["clients"] = len(metrics_prev_1_week["clients_dist"])

    metrics_prev_2_week["validations"] = total_validations(metrics_prev_2_week["clients_dist"])
    metrics_prev_2_week["users"] = len(metrics_prev_2_week["users_dist"])
    metrics_prev_2_week["clients"] = len(metrics_prev_2_week["clients_dist"])

    metrics_prev_3_week["validations"] = total_validations(metrics_prev_3_week["clients_dist"])
    metrics_prev_3_week["users"] = len(metrics_prev_3_week["users_dist"])
    metrics_prev_3_week["clients"] = len(metrics_prev_3_week["clients_dist"])

def run(look_back_days):
    for key in bb_bucket.list('validation-ui/prod_logs/'):
        act_date = datetime.strptime(str(date_dd_mm_yyyy), "%Y-%m-%d").date()
        log_date = datetime.strptime(key.last_modified.split('T')[0], "%Y-%m-%d").date()
        file_name = key.name.split('/')[2]
        if abs((act_date - log_date).days) < look_back_days and len(file_name)>0:
            print "[VUI LOG]", log_date, file_name, len(file_name), key.name,len(key.name)
            key.get_contents_to_filename(file_name)
            # process this
            with gzip.open(file_name, 'rb') as fin:
                next(fin)
                next(fin)
                for line in fin:
                    line_data = line.split('\t')
                    try:
                        generate_stats(line_data[11].split('&'), line_data[0])
                    except Exception:
                        pass

            os.remove(file_name)
    update_time = datetime.today().strftime('%H:%M:%S %d-%m-%Y')+" UTC"
    etl_metrics()
    final_json = json.dumps({
                            # 'users': user_metric,
                            #  'clients': client_complete_metric,
                            #  'clients_by_date': client_daily_metric,
                                'stats_by_day': date_metric,
                                'stats_by_week': {
                                            "week-0": metrics_this_week,
                                               "week-1": {"validations": metrics_prev_1_week["validations"],
                                                          "users": metrics_prev_1_week["users"],
                                                          "clients": metrics_prev_1_week["clients"]},
                                               "week-2": {"validations": metrics_prev_2_week["validations"],
                                                          "users": metrics_prev_2_week["users"],
                                                          "clients": metrics_prev_2_week["clients"]},
                                               "week-3": {"validations": metrics_prev_3_week["validations"],
                                                          "users": metrics_prev_3_week["users"],
                                                          "clients": metrics_prev_3_week["clients"]}
                                               },
                                'update_time': update_time})
    print final_json
    put_item('vui', datetime.today().strftime('%d-%m-%Y'), final_json)
    return "Done"

def generate_dates():
    curr_date_num = datetime.today().weekday() # mon is 0, sun is 6
    look_back_days = (curr_date_num +1) + 21 # 3-weeks + this-week
    date_format = '%Y-%m-%d'
    for day_num in range(0,curr_date_num+1):
        prevday = datetime.now() - timedelta(days=day_num)
        days_this_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {"validations": 0, "users": 0, "clients": 0}
    # print 'dates this week', days_this_week

    for day_num in range(curr_date_num+1,curr_date_num+8):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_1_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {"validations": 0, "users": 0, "clients": 0}
    # print 'days week ago', days_prev_1_week

    for day_num in range(curr_date_num+8,curr_date_num+15):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_2_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {"validations": 0, "users": 0, "clients": 0}
    # print 'days 2 weeks ago', days_prev_2_week

    for day_num in range(curr_date_num+15,curr_date_num+22):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_3_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {"validations": 0, "users": 0, "clients": 0}
    # print 'days 3 weeks ago', days_prev_3_week

    # print  date_metric
    return look_back_days

if __name__ == '__main__':
    look_back_days = generate_dates()
    run(look_back_days)
