__author__ = 'mohammad'

import time
from datetime import datetime, timedelta

import simplejson as json

import requests
from requests.utils import quote

from dynamo_io import put_item


# getting prev days data
history_limit = 1  # this is x
unfuddle_url = "https://mohammad:bismillah2235@athena.unfuddle.com/api/v1/account/activity.json?only=repositories"

time_h_m_s = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
date_dd_mm_yyyy = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')

commit_repo = {}
commit_repo_by_day = {}
commit_repo_this_week = {}
commit_user = {}
commit_user_this_week = {}
commit_user_by_day = {}

date_metric = {}

days_this_week ={}
days_prev_1_week = {}
days_prev_2_week = {}
days_prev_3_week = {}

metrics_this_week = {"commits": 0, "users": 0, "repos": 0, "user_names": {}, "repo_titles": {}}
metrics_prev_1_week = {"commits": 0, "users": 0, "repos": 0, "user_names": {}, "repo_titles": {}}
metrics_prev_2_week = {"commits": 0, "users": 0, "repos": 0, "user_names": {}, "repo_titles": {}}
metrics_prev_3_week = {"commits": 0, "users": 0, "repos": 0, "user_names": {}, "repo_titles": {}}

def dump_json():
    return ""

def etl_json( json_data, date_mdfy , this_week):
    commit_repo_by_day[date_mdfy] = {}
    commit_user_by_day[date_mdfy] = {}
    if this_week == 1:
        commit_repo_this_week[date_mdfy] = {}
        commit_user_this_week[date_mdfy] = {}

    for curr_index in range(0,len(json_data)):
        # check for repo and update
        repo_title = json_data[curr_index]['repository_title']
        repo_author = json_data[curr_index]['record']['changeset']['author_name']
        if repo_title in commit_repo_by_day[date_mdfy]:
            commit_repo_by_day[date_mdfy][repo_title] += 1
        else:
            commit_repo_by_day[date_mdfy][repo_title] = 1

        if repo_author in commit_user_by_day[date_mdfy]:
            commit_user_by_day[date_mdfy][repo_author] += 1
        else:
            commit_user_by_day[date_mdfy][repo_author] = 1

        if this_week > 0:
            if repo_title in commit_repo_this_week[date_mdfy]:
                commit_repo_this_week [date_mdfy][repo_title] += 1
            else:
                commit_repo_this_week[date_mdfy][repo_title] = 1
            if repo_author in commit_user_this_week [date_mdfy]:
                commit_user_this_week[date_mdfy][repo_author] += 1
            else:
                commit_user_this_week[date_mdfy][repo_author] = 1


        if repo_title in commit_repo:
            commit_repo[repo_title] += 1
        else:
            commit_repo[repo_title] = 1

        if repo_author in commit_user:
            commit_user[repo_author] += 1
        else:
            commit_user[repo_author] = 1

def total_commits( repo_structure ):
    commit_count = 0
    for repo_name in repo_structure:
        commit_count += repo_structure[repo_name]

    return commit_count

def modify_json():
    for day in commit_repo_by_day:
        # print day, commit_repo_by_day[day]
        total_commits_this_day = total_commits(commit_repo_by_day[day])
        total_users_this_day = len(commit_user_by_day[day])
        total_repos_this_day = len(commit_repo_by_day[day])

        if day in days_this_week:
            for user in commit_user_by_day[day]:
                if user in metrics_this_week["user_names"]:
                    metrics_this_week["user_names"][user] += commit_user_by_day[day][user]
                else:
                    metrics_this_week["user_names"][user] = commit_user_by_day[day][user]

            for repo in commit_repo_by_day[day]:
                if repo in metrics_this_week["repo_titles"]:
                    metrics_this_week["repo_titles"][repo] += commit_repo_by_day[day][repo]
                else:
                    metrics_this_week["repo_titles"][repo] = commit_repo_by_day[day][repo]
        elif day in days_prev_1_week:
            for user in commit_user_by_day[day]:
                if user in metrics_prev_1_week["user_names"]:
                    metrics_prev_1_week["user_names"][user] += commit_user_by_day[day][user]
                else:
                    metrics_prev_1_week["user_names"][user] = commit_user_by_day[day][user]

            for repo in commit_repo_by_day[day]:
                if repo in metrics_prev_1_week["repo_titles"]:
                    metrics_prev_1_week["repo_titles"][repo] += commit_repo_by_day[day][repo]
                else:
                    metrics_prev_1_week["repo_titles"][repo] = commit_repo_by_day[day][repo]
        elif day in days_prev_2_week:
            for user in commit_user_by_day[day]:
                if user in metrics_prev_2_week["user_names"]:
                    metrics_prev_2_week["user_names"][user] += commit_user_by_day[day][user]
                else:
                    metrics_prev_2_week["user_names"][user] = commit_user_by_day[day][user]

            for repo in commit_repo_by_day[day]:
                if repo in metrics_prev_2_week["repo_titles"]:
                    metrics_prev_2_week["repo_titles"][repo] += commit_repo_by_day[day][repo]
                else:
                    metrics_prev_2_week["repo_titles"][repo] = commit_repo_by_day[day][repo]
        elif day in days_prev_3_week:
            for user in commit_user_by_day[day]:
                print user, commit_user_by_day[day][user]
                if user in metrics_prev_3_week["user_names"]:
                    metrics_prev_3_week["user_names"][user] += commit_user_by_day[day][user]
                else:
                    metrics_prev_3_week["user_names"][user] = commit_user_by_day[day][user]

            for repo in commit_repo_by_day[day]:
                if repo in metrics_prev_3_week["repo_titles"]:
                    metrics_prev_3_week["repo_titles"][repo] += commit_repo_by_day[day][repo]
                else:
                    metrics_prev_3_week["repo_titles"][repo] = commit_repo_by_day[day][repo]

        date_metric[day] = {"users": total_users_this_day, "repos": total_repos_this_day, "total_commits": total_commits_this_day}

    metrics_this_week["commits"] = total_commits(metrics_this_week["repo_titles"]);
    metrics_this_week["repos"] = len(metrics_this_week["repo_titles"]);
    metrics_this_week["users"] = len(metrics_this_week["user_names"])

    metrics_prev_1_week["commits"] = total_commits(metrics_prev_1_week["repo_titles"]);
    metrics_prev_1_week["repos"] = len(metrics_prev_1_week["repo_titles"]);
    metrics_prev_1_week["users"] = len(metrics_prev_1_week["user_names"])

    metrics_prev_2_week["commits"] = total_commits(metrics_prev_2_week["repo_titles"]);
    metrics_prev_2_week["repos"] = len(metrics_prev_2_week["repo_titles"]);
    metrics_prev_2_week["users"] = len(metrics_prev_2_week["user_names"])

    metrics_prev_3_week["commits"] = total_commits(metrics_prev_3_week["repo_titles"]);
    metrics_prev_3_week["repos"] = len(metrics_prev_3_week["repo_titles"]);
    metrics_prev_3_week["users"] = len(metrics_prev_3_week["user_names"])

def run(look_back_limit):
    for day in range(0, look_back_limit):
        date_start = (datetime.now() - timedelta(days=(day +1))).strftime('%a, %d %b %Y ') +time_h_m_s+" GMT"
        date_mdfy = (datetime.now() - timedelta(days=(day))).strftime('%d-%m-%Y')
        date_end = (datetime.now() - timedelta(days=(day))).strftime('%a, %d %b %Y ') +time_h_m_s+" GMT"
        start_param = quote(date_start, safe='')
        end_param = quote(date_end, safe='')
        final_unfuddle_url = unfuddle_url+"&start_date="+start_param+"&end_date="+end_param
        json_content = requests.get(final_unfuddle_url).content
        json_data = json.loads(json_content)
        # print date_mdfy, final_unfuddle_url, json_data
        if day < 7:
            etl_json(json_data, date_mdfy, 1)
        else:
            etl_json(json_data, date_mdfy, 0)
        # print date_start, date_end

    modify_json()

    update_time = time_h_m_s+" "+date_dd_mm_yyyy+" UTC"
    final_json = json.dumps({'stats_by_date': date_metric,
                             'stats_by_week': {
                                            "week-0": metrics_this_week,
                                               "week-1": {"commits": metrics_prev_1_week["commits"],
                                                          "users": metrics_prev_1_week["users"],
                                                          "repos": metrics_prev_1_week["repos"]},
                                               "week-2": {"commits": metrics_prev_2_week["commits"],
                                                          "users": metrics_prev_2_week["users"],
                                                          "repos": metrics_prev_2_week["repos"]},
                                               "week-3": {"commits": metrics_prev_3_week["commits"],
                                                          "users": metrics_prev_3_week["users"],
                                                          "repos": metrics_prev_3_week["repos"]}
                                               },
                             'update_time': update_time})
    print final_json
    put_item('code_commit', date_dd_mm_yyyy, final_json)
    return json.dumps(final_json)

def generate_dates():
    curr_date_num = datetime.today().weekday() # mon is 0, sun is 6
    look_back_days = (curr_date_num +1) + 21 # 3-weeks + this-week
    date_format = '%d-%m-%Y'
    for day_num in range(0,curr_date_num+1):
        prevday = datetime.now() - timedelta(days=day_num)
        days_this_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {}
    # print 'dates this week', days_this_week

    for day_num in range(curr_date_num+1,curr_date_num+8):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_1_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {}
    # print 'days week ago', days_prev_1_week

    for day_num in range(curr_date_num+8,curr_date_num+15):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_2_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {}
    # print 'days 2 weeks ago', days_prev_2_week

    for day_num in range(curr_date_num+15,curr_date_num+22):
        prevday = datetime.now() - timedelta(days=day_num)
        days_prev_3_week[prevday.strftime(date_format)] = {}
        date_metric[prevday.strftime(date_format)] = {}
    # print 'days 3 weeks ago', days_prev_3_week

    # print  date_metric
    return look_back_days

if __name__ == '__main__':
    look_back_days = generate_dates()
    run(look_back_days)