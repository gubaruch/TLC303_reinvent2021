import argparse
import logging
import warnings
import sys
import os
import inspect
two_up = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
sys.path.insert(0, two_up)

import test.test_utils as test_utils
from data_mesh_util.lib.constants import *
from data_mesh_util import DataMeshConsumer as dmc
import data_mesh_util.lib.utils as utils

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)


class Step4():
    '''
    Consumer functionality to finalize a subscription request.
    '''
    _region, _clients, _account_ids, _creds = test_utils.load_client_info_from_file()

    _mgr = dmc.DataMeshConsumer(data_mesh_account_id=_account_ids.get(MESH),
                                log_level=logging.DEBUG,
                                region_name=_region,
                                use_credentials=_creds.get(CONSUMER))

    def setUp(self) -> None:
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def finalize_subscription(self, subscription_id):
        # finalize the subscription
        self._mgr.finalize_subscription(subscription_id=subscription_id)

        # confirm that the consumer can see that it's status is now Active
        subscription = self._mgr.get_subscription(request_id=subscription_id)
        if subscription.get('Status') != 'Active':
            raise Exception(f"Subscription {subscription_id} is not Active")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--subscription_id', dest='subscription_id', required=True)

    args = parser.parse_args()
    print(Step4().finalize_subscription(subscription_id=args.subscription_id))
