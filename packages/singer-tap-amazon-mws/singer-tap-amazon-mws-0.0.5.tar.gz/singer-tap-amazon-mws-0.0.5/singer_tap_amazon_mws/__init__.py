#!/usr/bin/env python3

import singer

from singer_tap_amazon_mws.tap_framework import Runner

from singer_tap_amazon_mws.client import AmazonMWSClient
from singer_tap_amazon_mws.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


class AmazonMWSRunner(Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(
        required_config_keys=['access_key', 'secret_key', 'seller_id',
                              'region', 'marketplace_ids', 'start_date'])

    client = AmazonMWSClient(args.config)
    runner = AmazonMWSRunner(
        args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()
