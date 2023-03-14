import pandas
import pytest

from kowalski.tools.tns_watcher import get_tns
from kowalski.utils import Mongo
from kowalski.config import load_config
from kowalski.log import log


""" load config and secrets """
config = load_config(config_files=["config.yaml"])["kowalski"]


class TestTNSWatcher:
    """
    Test TNS monitoring
    """

    @pytest.mark.xfail(raises=pandas.errors.ParserError)
    def test_tns_watcher(self):
        log("Connecting to DB")
        mongo = Mongo(
            host=config["database"]["host"],
            port=config["database"]["port"],
            replica_set=config["database"]["replica_set"],
            username=config["database"]["username"],
            password=config["database"]["password"],
            db=config["database"]["db"],
            srv=config["database"]["srv"],
            verbose=True,
        )
        log("Successfully connected")

        collection = config["database"]["collections"]["tns"]

        log(
            "Grabbing most recent object from the TNS and ingesting that into the database"
        )
        get_tns(
            grab_all=False,
            test=True,
        )
        log("Done")

        fetched_entries = list(mongo.db[collection].find({}, {"_id": 1}))

        assert len(fetched_entries) > 0
