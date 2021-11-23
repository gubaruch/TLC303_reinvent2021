import logging
import unittest
import sys
import os
import warnings
import boto3
import test_utils
from data_mesh_util.lib.constants import *

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../src/resource"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../src/lib"))

from data_mesh_util import DataMeshProducer as dmp
from data_mesh_util.lib.SubscriberTracker import *

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)


class DataMeshProducerAccountTests(unittest.TestCase):
    '''
    Class to test the functionality of a data producer. Should be run using credentials for a principal who can assume
    the DataMeshAdminProducer role in the data mesh. Requires environment variables:

    AWS_REGION
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_SESSION_TOKEN (Optional)
    '''
    _region, _clients, _account_ids, _creds = test_utils.load_client_info_from_file()

    _mgr = dmp.DataMeshProducer(data_mesh_account_id=_account_ids.get(MESH),
                                log_level=logging.DEBUG,
                                region_name=_region,
                                use_credentials=_creds.get(PRODUCER))
    _subscription_tracker = SubscriberTracker(data_mesh_account_id=_account_ids.get(MESH),
                                              credentials=_creds.get(MESH),
                                              region_name=_region,
                                              log_level=logging.DEBUG)

    def setUp(self) -> None:
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def test_create_data_product(self):
        self._mgr.create_data_products(
            source_database_name='tpcds',
            table_name_regex='customer',
            domain=None,
            data_product_name=None,
            create_public_metadata=True
            # sync_mesh_catalog_schedule="cron(0 */2 * * ? *)",
            # sync_mesh_crawler_role_arn=f"arn:aws:iam::{self._account_ids.get(PRODUCER)}:role/service-role/AWSGlueServiceRole-Crawler"
            # expose_data_mesh_db_name=None,
            # expose_table_references_with_suffix=None
        )
