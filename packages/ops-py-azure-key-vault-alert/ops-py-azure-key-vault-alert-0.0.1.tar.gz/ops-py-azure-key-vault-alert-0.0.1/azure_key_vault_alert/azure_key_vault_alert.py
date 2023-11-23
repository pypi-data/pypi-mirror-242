#!/usr/bin/env python

import os
import logging
import argparse
from azure_key_vault_report import azure_key_vault_report
from slack_alert import slack_alert


########################################################################################################################


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    SLACK_WEBHOOK_REPORT = os.getenv("SLACK_WEBHOOK_REPORT")
    SLACK_WEBHOOK_NOTIFY = os.getenv("SLACK_WEBHOOK_NOTIFY")

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vaults", nargs='+',
                        help="List of key vaults to check. E.g. kv-dev kv-test")
    args = parser.parse_args()
    vaults = args.vaults
    if not vaults:
        logging.error("No vaults specified.")
        exit(2)

    if isinstance(vaults, str):
        vaults = [vaults]

    # 'success' variable initially set to False.
    # It will only be set to True if one more report POST to the specified 'SLACK_WEBHOOK_REPORT' webhook
    # has return code 200
    # Only if True, the additional 'SLACK_WEBHOOK_NOTIFY' will be triggered.
    success = False

    # Post each report to the specified SLACK_WEBHOOK_REPORT
    for vault in vaults:
        kv_report = azure_key_vault_report.AzureKeyVaultReport(vault)
        kv_report.az_cmd()
        kv_report.parse_results()
        report = kv_report.plaintext_report()

        if not SLACK_WEBHOOK_REPORT:
            logging.warning("'SLACK_WEBHOOK_REPORT' not provided. "
                            f"'{vault}' report not be sent to Slack.")
        alert = slack_alert.SlackAlert(SLACK_WEBHOOK_REPORT)
        alert.set_payload(heading=vault, msg=report)
        alert.post_payload()
        response_code = alert.get_response_code()

        if isinstance(response_code, int) and response_code == 200:
            success = True

    # If success and 'SLACK_WEBHOOK_NOTIFY' provided
    # an additional notify will be posted to the 'SLACK_WEBHOOK_NOTIFY' webhook
    if success and SLACK_WEBHOOK_NOTIFY:
        logging.info(f"Trigger alert about new slack message(s)...")
        alert = slack_alert.SlackAlert(SLACK_WEBHOOK_NOTIFY)
        alert.post_payload()
