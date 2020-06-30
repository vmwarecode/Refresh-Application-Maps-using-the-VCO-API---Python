#!/usr/bin/env python3
#
# Update Application Map IP and port mappings for select applications to ensure they are consistent with the current
# authoritative mappings maintained by application providers (e.g. Microsoft Office).
#
# This script assumes the user is an OPERATOR admin.
#
# Usage: VC_USERNAME='user@velocloud.net' VC_PASSWORD=s3cret python3 refresh_application_maps.py
#

import os
from client import *

# EDIT THESE
VCO_HOSTNAME = os.environ.get('VCO_HOSTNAME', 'vcoX.velocloud.net')
TARGET_APPLICATION_MAP_NAMES = ['Default Application Map']

def main():

    client = VcoRequestManager(VCO_HOSTNAME)
    client.authenticate(os.environ['VC_USERNAME'], os.environ['VC_PASSWORD'])

    application_maps = client.call_api('configuration/getApplicationMaps', {})

    target_app_maps = []
    for app_map in application_maps:
        if app_map['name'] in TARGET_APPLICATION_MAP_NAMES:
            target_app_maps.append(app_map)

    if len(target_app_maps) == 0:
        print('No application maps were found with the specified names.')

    print(f'Updating {len(target_app_maps)} application maps...')
    for app_map in target_app_maps:
            print(f'\t- {app_map["name"]}')

    target_app_map_ids = [am['id'] for am in target_app_maps]

    updated_profiles = client.call_api('/configuration/updateApplicationMapContent', {
        'ids': target_app_map_ids,
        'updateProfiles': True
    })

    print(f'Successfully updated {len(updated_profiles)} application maps.')

if __name__ == '__main__':
    main()