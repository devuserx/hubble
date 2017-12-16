# -*- coding: utf-8 -*-
'''
Generate a unique uuid for this host, storing it on disk so it persists across
restarts
'''
import logging
import os
import uuid

log = logging.getLogger(__name__)


def host_uuid():
    '''
    Generate a unique uuid for this host, storing it on disk so it persists
    across restarts
    '''
    cached_uuid_path = os.path.join(os.path.dirname(__opts__['configfile']), 'hubble_cached_uuid')
    existing_uuid = __opts__.get('host_uuid', None)
    try:
        if os.path.isfile(cached_uuid_path):
            with open(cached_uuid_path, 'r') as f:
                cached_uuid = f.read()
                # Check if it's changed out from under us -- problem!
                if existing_uuid and cached_uuid != existing_uuid:
                    log.error('host_uuid changed on disk unexpectedly!'
                              '\nPrevious: {0}\nNew: {1}\nKeeping previous.'
                              .format(existing_uuid, cached_uuid))
                    return {'host_uuid': existing_uuid}
                return {'host_uuid': cached_uuid}
        elif existing_uuid:
            log.error('host_uuid was previously generated, but the cached '
                      'file is no longer present: {0}'.format(cached_uuid_path))
        else:
            # TODO: once we figure out how to get a custom log level for
            # non-error splunk logs, we should move this to that log level so
            # it doesn't look like an error.
            log.error('generating fresh uuid, no cache file found. '
                      '(probably not a problem)')
    except Exception:
        log.exception('Problem retrieving cached host uuid from file: {0}'
                      .format(cached_uuid_path))

    # Generate a fresh one if needed
    if not existing_uuid:
        existing_uuid = str(uuid.uuid4())

    # Cache the new (or old if it needs re-caching) uuid
    try:
        with open(cached_uuid_path, 'w') as f:
            f.write(existing_uuid)
    except Exception:
        log.exception('Problem writing cached host uuid to file: {0}'
                      .format(cached_uuid_path))

    return {'host_uuid': existing_uuid}
