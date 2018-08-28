import datetime
import pytz
import singer

from dateutil.parser import parse
from tap_framework.streams import BaseStream
from tap_framework.config import get_config_start_date
from tap_framework.state import get_last_record_value_for_table, incorporate, \
    save_state

LOGGER = singer.get_logger()


class BasePlatformPurpleStream(BaseStream):

    def get_stream_data(self, data):
        return [self.transform_record(item) for item in data]

    def sync_data(self):
        table = self.TABLE
        done = False

        start_date = get_last_record_value_for_table(self.state, table)

        if start_date is None:
            start_date = get_config_start_date(self.config)

        end_date = start_date + datetime.timedelta(days=7)

        while not done:
            max_date = start_date

            LOGGER.info(
                "Querying {} starting at {}".format(table, start_date))

            response = self.client.make_request(
                self.get_url(),
                'POST',
                body={
                    'filters': {
                        'environment': self.config.get('environment')
                    },
                    'startMSeconds': int(start_date.timestamp() * 1000),
                    'endMSeconds': int(end_date.timestamp() * 1000)
                })

            to_write = self.get_stream_data(response)

            with singer.metrics.record_counter(endpoint=table) as ctr:
                singer.write_records(table, to_write)

                ctr.increment(amount=len(to_write))

                for item in to_write:
                    max_date = max(
                        max_date,
                        parse(item.get('dateTime'))
                    )

            self.state = incorporate(
                self.state, table, 'start_date', start_date)

            if start_date == max_date and len(to_write) == 1:
                done = True

            if len(to_write) == 0:
                start_date = end_date
            else:
                start_date = max_date

            end_date = start_date + datetime.timedelta(days=7)

            save_state(self.state)
