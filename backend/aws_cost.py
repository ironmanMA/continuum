__author__ = 'mohammad'

import boto
from boto.s3.connection import OrdinaryCallingFormat

from dynamo_io import put_item

from datetime import datetime
import calendar

from collections import deque
from itertools import islice

import simplejson as json
import gzip
import csv
import os

AWS_ACCESS_KEY = 'AKIAJ6XUO5KUSL2ZQKSA'
AWS_SECRET_KEY = '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'

conn = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY, calling_format=OrdinaryCallingFormat())
# need to be used as BCUsages has Uppercase
aws_cost_bucket = conn.get_bucket('BCUsages')
date_dd_mm_yyyy = datetime.today().strftime('%Y-%m-%d')

months_lookback = 6

prev_months_cost_history = {}
predicted_costs = {}
system_costs = {}

def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month

def skip_last_n(iterator, n=1):
    it = iter(iterator)
    prev = deque(islice(it, n), n)
    for item in it:
        yield prev.popleft()
        prev.append(item)

def predict_total_cost(cost_tilldate, curr_year, curr_month):
    total_days_this_month = float(calendar.monthrange(curr_year, curr_month)[1])
    days_completed = float(datetime.today().day)
    cost = float(cost_tilldate)
    return cost*(total_days_this_month/days_completed)

def month_total_cost (date, file_name):
    final_cost = 0
    if str(date) not in prev_months_cost_history:
        prev_months_cost_history[str(date)] = {}
    with open(file_name, 'rb') as file_data:
        reader = csv.reader(file_data)
        for row in reader:
            if row[12] =='AmazonEC2':
                ec2_cost = row[len(row)-1]
                if 'ec2' not in prev_months_cost_history[str(date)]:
                    prev_months_cost_history[str(date)]['ec2'] = float(ec2_cost)
                else:
                    prev_months_cost_history[str(date)]['ec2'] += float(ec2_cost)

            elif row[12] == 'AmazonRDS':
                rds_cost = row[len(row)-1]
                if 'rds' not in prev_months_cost_history[str(date)]:
                    prev_months_cost_history[str(date)]['rds'] = float(rds_cost)
                else:
                    prev_months_cost_history[str(date)]['rds'] += float(rds_cost)

            elif row[12] == 'AmazonRedshift':
                redshift_cost = row[len(row)-1]
                if 'redshift' not in prev_months_cost_history[str(date)]:
                    prev_months_cost_history[str(date)]['redshift'] = float(redshift_cost)
                else:
                    prev_months_cost_history[str(date)]['redshift'] += float(redshift_cost)

            elif row[12] == 'ElasticMapReduce':
                emr_cost = row[len(row)-1]
                if 'emr' not in prev_months_cost_history[str(date)]:
                    prev_months_cost_history[str(date)]['emr'] = float(emr_cost)
                else:
                    prev_months_cost_history[str(date)]['emr'] += float(emr_cost)

            if row[3]=='StatementTotal':
                # find the totals cost
                final_cost = row[len(row)-1]
                prev_months_cost_history[str(date)]['total'] = float(final_cost)

    # now predict for last month
    if diff_month(datetime.strptime(str(date_dd_mm_yyyy), "%Y-%m-%d").date(), date) ==0:
        predicted_costs['total'] = predict_total_cost(final_cost, date.year,date.month)
        predicted_costs['ec2'] = predict_total_cost(prev_months_cost_history[str(date)]['ec2'], date.year,date.month)
        predicted_costs['rds'] = predict_total_cost(prev_months_cost_history[str(date)]['rds'], date.year,date.month)
        predicted_costs['redshift'] = predict_total_cost(prev_months_cost_history[str(date)]['redshift'], date.year,date.month)
        predicted_costs['emr'] = predict_total_cost(prev_months_cost_history[str(date)]['emr'], date.year,date.month)
    os.remove(file_name)
    return "Done"

def run_totalCosts():
    for key in aws_cost_bucket.list('208876916689-aws-billing-csv-'):
        act_date = datetime.strptime(str(date_dd_mm_yyyy), "%Y-%m-%d").date()
        log_date = datetime.strptime(key.name.split('208876916689-aws-billing-csv-')[1][:-4]+"-01", "%Y-%m-%d").date()
        if diff_month(act_date, log_date) < months_lookback:
            print key.name, key.size, key.last_modified
            key.get_contents_to_filename(key.name)
            month_total_cost(log_date, key.name)

    # print json.dumps({'cost_history': prev_months_cost_history, 'predicted_costs': predicted_costs})
    return "Done"

def add_system_product_date_cost (system_tag, product_code, log_date, total_cost):

    system_tag = system_tag if len(system_tag) >0 else "untagged"

    if system_tag not in system_costs:
        system_costs[system_tag] = {}
        system_costs[system_tag][product_code] = {}
        system_costs[system_tag]['total']={}
        system_costs[system_tag]['total'][str(log_date)] = total_cost
        system_costs[system_tag][product_code][str(log_date)] = total_cost
    else:
        if str(log_date) not in system_costs[system_tag]['total']:
            system_costs[system_tag]['total'][str(log_date)] = total_cost
        else:
            system_costs[system_tag]['total'][str(log_date)] += total_cost

        if product_code not in system_costs[system_tag]:
            system_costs[system_tag][product_code] = {}
            system_costs[system_tag][product_code][str(log_date)] = total_cost
        else:
            if str(log_date) not in system_costs[system_tag][product_code]:
                system_costs[system_tag][product_code][str(log_date)] = total_cost
            else:
                system_costs[system_tag][product_code][str(log_date)] += total_cost

    if diff_month(datetime.strptime(str(date_dd_mm_yyyy), "%Y-%m-%d").date(), log_date) ==0:
        system_costs[system_tag]['predicted_cost'] = predict_total_cost(system_costs[system_tag]['total'][str(log_date)],
                                                                    log_date.year, log_date.month)


def run_system_costs(file_name, log_date):
    with open(file_name, 'rb') as file_data:
            reader = csv.reader(file_data)
            next(file_data)
            headers = reader.next()
            for row in skip_last_n(reader,3):
                product_code = row[headers.index('ProductCode')]
                system_tag = row[headers.index('user:system')]
                total_cost = float(row[headers.index('TotalCost')]) #total instance cost

                # print product_code,system_tag,total_cost

                if product_code =='AmazonEC2':
                    add_system_product_date_cost(system_tag, 'ec2', log_date, total_cost)

                elif product_code == 'AmazonRDS':
                    add_system_product_date_cost(system_tag, 'rds', log_date, total_cost)

                elif product_code == 'AmazonRedshift':
                    add_system_product_date_cost(system_tag, 'redshift', log_date, total_cost)

                elif product_code == 'ElasticMapReduce':
                    add_system_product_date_cost(system_tag, 'emr', log_date, total_cost)

                else:
                    add_system_product_date_cost(system_tag, 'other', log_date, total_cost)
    os.remove(file_name)
    return "Done"

def run_particulars():
    for key in aws_cost_bucket.list('208876916689-aws-cost-allocation-'):
        act_date = datetime.strptime(str(date_dd_mm_yyyy), "%Y-%m-%d").date()
        log_date = datetime.strptime(key.name.split('208876916689-aws-cost-allocation-')[1][:-4]+"-01", "%Y-%m-%d").date()
        if diff_month(act_date, log_date) < 2:
            print key.name, key.size, key.last_modified
            key.get_contents_to_filename(key.name)
            run_system_costs(key.name, log_date)
    # calculate total, predicted for all
    # print json.dumps({'system_costs': system_costs})
    return "Done"

if __name__ == '__main__':
    run_totalCosts()
    run_particulars()
    update_time = datetime.today().strftime('%H:%M:%S %d-%m-%Y')+" UTC"
    final_json = json.dumps({'cost_history': prev_months_cost_history,
                             'predicted_costs': predicted_costs,
                             'system_costs': system_costs,
                             'update_time': update_time})
    put_item('aws-cost', datetime.today().strftime('%d-%m-%Y'), final_json)
    print final_json
