import os
import time
import json

from cvdastwrapper.runconfig import dlogrespdname

def get_priority_for_response(response, severity):
    pri = 4
    if response and response.startswith("200-->"):
        if len(response) > len("200-->[]") and (not response == "200-->null"):
            if severity.lower().startswith("c") or severity.lower().startswith("h"):
                pri = 1
            else:
                pri = 2
    if severity.lower().startswith("c") or severity.lower().startswith("h"):
        if pri > 3:
            pri = 3
    return pri


def generate_test_report(api_test_report, spec, test):
    #print(api_test_report, spec, test, "In Genereate test report atgs")
    failed_test = test['tested'].get("failed", [])

    api_test_report['total_failed'] += len(failed_test)
    api_test_report['total_tests'] += len(failed_test)
    api_test_report[spec]['total_tests_count'] += len(failed_test)
    api_test_report[spec]['total_failed_count'] += len(failed_test)
    spec_report = api_test_report[spec]

    # parse failed resport
    for each_failed_test in failed_test:
        api = each_failed_test.get('api', '')
        # method = each_failed_test.get('method', '')
        attack = each_failed_test.get('attack', '')
        severity = each_failed_test.get('severity', '')
        attack_info = each_failed_test.get('attackinfo', {})
        response = each_failed_test.get('resp', '')
        testinput = each_failed_test.get('testinput', '')

        #print(each_failed_test,attack_info, "\n\n\n")
        api_test_report['all_failed_apis'].add(api)
        api_test_report['all_apis'].add(api)
        api_test_report[spec]['all_spec_apis'].add(api)
        api_test_report[spec]['all_failed_apis'].add(api)

        # Compute the counts
        api_test_report['total_count'] += 1
        if severity.lower() == 'critical':
            api_test_report['failed_cc'] += 1
            api_test_report['critical_count'] += 1
            # api_test_report['attack_severity']['critical'].add(api)
        if severity.lower() == 'high':
            api_test_report['failed_hc'] += 1
            api_test_report['high_count'] += 1
            # api_test_report['attack_severity']['high'].add(api)
        if severity.lower() == 'medium':
            api_test_report['failed_mc'] += 1
            api_test_report['medium_count'] += 1
            # api_test_report['attack_severity']['medium'].add(api)
        if severity.lower() == 'low':
            api_test_report['failed_lc'] += 1
            api_test_report['low_count'] += 1
            # api_test_report['attack_severity']['low'].add(api)

        # Compute priority
        pri = get_priority_for_response(response, severity)

        spec_report['priority_count']['p'+str(pri)+'_count'] += 1
        spec_report['apis_by_priority']['p'+str(pri)].add(api)

        # Compute count by attack category,
        if attack in api_test_report['attack_category']:
            api_test_report['attack_category'][attack]['count'] += 1
            api_test_report['attack_category'][attack]['all_apis'].add(api)
            api_test_report['attack_category'][attack]['p'+str(pri)+'_apis'].add(
                api)
        else:
            api_test_report['attack_category'][attack] = {
                'all_apis': set([api]),
                'count': 1
            }
            api_test_report['attack_category'][attack]['p1_apis'] = set()
            api_test_report['attack_category'][attack]['p2_apis'] = set()
            api_test_report['attack_category'][attack]['p3_apis'] = set()
            api_test_report['attack_category'][attack]['p4_apis'] = set()

            api_test_report['attack_category'][attack].update(
                {'p'+str(pri)+'_apis': set([api])}
            )

        api_details = api_test_report.get(
            spec, {}).get(api, {})
        if attack in api_details:
            if 'count' in api_details[attack]:
                api_details[attack]['count'] += 1
            else:
                api_details[attack]['count'] = 1
        else:
            api_details[attack] = {
                'count': 1
            }
        api_details[attack]['pri'] = 'p'+str(pri)
        api_details[attack]['classification'] = attack_info[attack][1]['classification']
        api_details[attack]['severity'] = severity
        api_details[attack]['attack'] = attack

        req_text = ''
        if not os.path.exists(dlogrespdname):
            os.mkdir(dlogrespdname)
        req_file_name = dlogrespdname + "/request_"+str(time.time())+".txt"
        with open(req_file_name, "w+") as f:
            f.write(testinput)
        req_text = "<a href=\"" + req_file_name + "\">Request Input</a>"

        res_text = ''
        if len(response) > 20:
            if not os.path.exists(dlogrespdname):
                os.mkdir(dlogrespdname)
            fname = dlogrespdname + "/resp"+str(time.time())+".txt"
            with open(fname, "w+") as f:
                f.write(response)
            res_text = "<a href=\"" + fname + "\">Response Message</a>"
        else:
            res_text = response

        api_details[attack]['testinput'] = req_text
        api_details[attack]['response'] = res_text
        #api_details[attack]['api'] = api
        if api in spec_report:
            spec_report[api].update(api_details)
        else:
            spec_report[api] = api_details
        api_test_report[spec] = spec_report

    # Parse passed result
    passed_test = test['tested'].get("passed", [])

    api_test_report['total_passed'] += len(passed_test)
    api_test_report['total_tests'] += len(passed_test)
    api_test_report[spec]['total_tests_count'] += len(passed_test)
    api_test_report[spec]['total_passed_count'] += len(passed_test)
    for each_passed_test in passed_test:
        api = each_passed_test.get('api', '')
        severity = each_passed_test.get('severity', '')

        api_test_report['all_apis'].add(api)
        api_test_report[spec]['all_spec_apis'].add(api)

        # Compute the counts
        api_test_report['total_count'] += 1
        if severity.lower() == 'critical':
            api_test_report['critical_count'] += 1
        if severity.lower() == 'high':
            api_test_report['high_count'] += 1
        if severity.lower() == 'medium':
            api_test_report['medium_count'] += 1
        if severity.lower() == 'low':
            api_test_report['low_count'] += 1

    # Parse skipped result
    skipped_test = test['tested'].get("skipped", [])
    api_test_report[spec]['total_tests_count'] += len(skipped_test)
    api_test_report[spec]['skipped_tests_count'] = len(skipped_test)
    for each_skipped_test in skipped_test:
        api = each_skipped_test.get('api', '')
        api_test_report['all_apis'].add(api)
        api_test_report[spec]['all_spec_apis'].add(api)

    return
