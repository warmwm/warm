##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from __future__ import absolute_import

import os
import time
import sys
import logging

from keystoneauth1 import loading
from keystoneauth1 import session
from cinderclient import client as cinderclient
from novaclient import client as novaclient
from cinderclient import client as cinderclient
from glanceclient import client as glanceclient
from gnocchiclient import client as gnocchiclient
from neutronclient.neutron import client as neutronclient
from heatclient import client as heatclient

log = logging.getLogger(__name__)

DEFAULT_HEAT_API_VERSION = '1'
DEFAULT_GNOCCHI_API_VERSION = '1'
DEFAULT_API_VERSION = '2'


# *********************************************
#   CREDENTIALS
# *********************************************
def get_credentials():
    """Returns a creds dictionary filled with parsed from env"""
    creds = {}

    keystone_api_version = os.getenv('OS_IDENTITY_API_VERSION')

    if keystone_api_version is None or keystone_api_version == '2':
        keystone_v3 = False
        tenant_env = 'OS_TENANT_NAME'
        tenant = 'tenant_name'
    else:
        keystone_v3 = True
        tenant_env = 'OS_PROJECT_NAME'
        tenant = 'project_name'

    # The most common way to pass these info to the script is to do it
    # through environment variables.
    creds.update({
        "username": os.environ.get("OS_USERNAME"),
        "password": os.environ.get("OS_PASSWORD"),
        "auth_url": os.environ.get("OS_AUTH_URL"),
        tenant: os.environ.get(tenant_env)
    })

    if keystone_v3:
        if os.getenv('OS_USER_DOMAIN_NAME') is not None:
            creds.update({
                "user_domain_name": os.getenv('OS_USER_DOMAIN_NAME')
            })
        if os.getenv('OS_PROJECT_DOMAIN_NAME') is not None:
            creds.update({
                "project_domain_name": os.getenv('OS_PROJECT_DOMAIN_NAME')
            })

    return creds


def get_session_auth():
    loader = loading.get_plugin_loader('password')
    creds = get_credentials()
    auth = loader.load_from_options(**creds)
    return auth


def get_session():
    auth = get_session_auth()
    try:
        cacert = os.environ['OS_CACERT']
    except KeyError:
        return session.Session(auth=auth)
    else:
        cacert = False if cacert.lower() == "false" else cacert
        return session.Session(auth=auth, verify=cacert)


def get_endpoint(service_type, endpoint_type='publicURL'):
    auth = get_session_auth()
    return get_session().get_endpoint(auth=auth,
                                      service_type=service_type,
                                      endpoint_type=endpoint_type)


# *********************************************
#   CLIENTS
# *********************************************
def get_heat_api_version():     # pragma: no cover
    try:
        api_version = os.environ['HEAT_API_VERSION']
    except KeyError:
        return DEFAULT_HEAT_API_VERSION
    else:
        log.info("HEAT_API_VERSION is set in env as '%s'", api_version)
        return api_version

def get_heat_client():          #praga: no cover
    sess = get_session()
    heat_endpoint = get_endpoint(service_type='orchestration')
    return heatclient.Client(
        get_heat_api_version(),
        endpoint=heat_endpoint, session=sess)

def get_cinder_client_version():      # pragma: no cover
    try:
        api_version = os.environ['OS_VOLUME_API_VERSION']
    except KeyError:
        return DEFAULT_API_VERSION
    else:
        log.info("OS_VOLUME_API_VERSION is set in env as '%s'", api_version)
        return api_version


def get_cinder_client():      # pragma: no cover
    sess = get_session()
    return cinderclient.Client(get_cinder_client_version(), session=sess)


def get_nova_client_version():      # pragma: no cover
    try:
        api_version = os.environ['OS_COMPUTE_API_VERSION']
    except KeyError:
        return DEFAULT_API_VERSION
    else:
        log.info("OS_COMPUTE_API_VERSION is set in env as '%s'", api_version)
        return api_version


def get_nova_client():      # pragma: no cover
    sess = get_session()
    return novaclient.Client(get_nova_client_version(), session=sess)


def get_neutron_client_version():   # pragma: no cover
    try:
        api_version = os.environ['OS_NETWORK_API_VERSION']
    except KeyError:
        return DEFAULT_API_VERSION
    else:
        log.info("OS_NETWORK_API_VERSION is set in env as '%s'", api_version)
        return api_version


def get_neutron_client():   # pragma: no cover
    sess = get_session()
    return neutronclient.Client(get_neutron_client_version(), session=sess)


def get_glance_client_version():    # pragma: no cover
    try:
        api_version = os.environ['OS_IMAGE_API_VERSION']
    except KeyError:
        return DEFAULT_API_VERSION
    else:
        log.info("OS_IMAGE_API_VERSION is set in env as '%s'", api_version)
        return api_version


def get_glance_client():    # pragma: no cover
    sess = get_session()
    return glanceclient.Client(get_glance_client_version(), session=sess)


def get_cinder_client_version():
    try:
        api_version = os.environ['OS_VOLUME_API_VERSION']
    except KeyError:
        return DEFAULT_API_VERSION
    else:
        log.info("OS_VOLUME_API_VERSION is set in env as '%s'", api_version)
        return api_version


def get_cinder_client():
    sess = get_session()
    return cinderclient.Client(get_cinder_client_version(), session=sess)


def get_gnocchi_client_version():
    try:
        api_version = os.environ['OS_GNOCCHI_API_VERSION']
    except KeyError:
        return DEFAULT_GNOCCHI_API_VERSION
    else:
        log.info("OS_GNOCCHI_API_VERSION is set in env as '%s'", api_version)
        return api_version


def get_gnocchi_client():
    sess = get_session()
    return gnocchiclient.Client(get_gnocchi_client_version(), session=sess)


# *********************************************
#   NOVA
# *********************************************
def get_host_list(av_zone=None):
    try:
        return get_nova_client().hosts.list(av_zone)
    except Exception:
        log.exception("Error [get_host_list(nova_client)]")


def get_instances(nova_client):     # pragma: no cover
    try:
        return nova_client.servers.list(search_opts={'all_tenants': 1})
    except Exception:
        log.exception("Error [get_instances(nova_client)]")


def get_server_status(nova_client, instance_id):     # pragma: no cover
    try:
        return nova_client.servers.get(instance_id).status
    except Exception:
        log.exception("Error [get_server_status(nova_client)]")


def get_instance_status(nova_client, instance):     # pragma: no cover
    try:
        return nova_client.servers.get(instance.id).status
    except Exception:
        log.exception("Error [get_instance_status(nova_client)]")


def get_instance_by_name(nova_client, instance_name):   # pragma: no cover
    try:
        return nova_client.servers.find(name=instance_name)
    except Exception:
        log.exception("Error [get_instance_by_name(nova_client, '%s')]",
                      instance_name)


def get_instance_by_id(nova_client, instance_id):   # pragma: no cover
    try:
        return nova_client.servers.find(id=instance_id)
    except Exception:
        log.exception("Error [get_instance_by_id(nova_client, '%s')]",
                      instance_id)


def get_aggregates(nova_client):    # pragma: no cover
    try:
        return nova_client.aggregates.list()
    except Exception:
        log.exception("Error [get_aggregates(nova_client)]")


def get_availability_zones(nova_client):    # pragma: no cover
    try:
        return nova_client.availability_zones.list()
    except Exception:
        log.exception("Error [get_availability_zones(nova_client)]")


def get_availability_zone_names(nova_client):   # pragma: no cover
    try:
        return [az.zoneName for az in get_availability_zones(nova_client)]
    except Exception:
        log.exception("Error [get_availability_zone_names(nova_client)]")



def create_aggregate(aggregate_name, av_zone):
    try:
        return get_nova_client().aggregates.create(aggregate_name, av_zone)
    except Exception:
        log.exception("Error [create_aggregate(nova_client, %s, %s)]",
                      aggregate_name, av_zone)
        return False


def update_aggregate_av_zone(aggregate_id, values):
    try:
        get_nova_client().aggregates.update(aggregate_id, values)
        return True
    except Exception:
        log.exception("Error [create_aggregate(nova_client, %s)]",
                      aggregate_id)
        return False


def delete_aggregate(aggregate_id):  # pragma: no cover
    try:
        get_nova_client().aggregates.delete(aggregate_id)
        return True
    except Exception:
        log.exception("Error [delete_aggregate(nova_client, %s)]",
                      aggregate_id)
        return False


def get_aggregate_id(nova_client, aggregate_name):      # pragma: no cover
    try:
        aggregates = get_aggregates(nova_client)
        _id = next((ag.id for ag in aggregates if ag.name == aggregate_name))
    except Exception:
        log.exception("Error [get_aggregate_id(nova_client, %s)]",
                      aggregate_name)
    else:
        return _id

'''
def add_host_to_aggregate(aggregate_name, compute_host):
    try:
        nova_client = get_nova_client()
        aggregate_id = get_aggregate_id(nova_client, aggregate_name)
        nova_client.aggregates.add_host(aggregate_id, compute_host)
        return True
    except Exception:
        log.exception("Error [add_host_to_aggregate(nova_client, %s, %s)]",
                      aggregate_name, compute_host)
        return False
'''


def add_host_to_aggregate(aggregate_id, host_name):
    try:
        get_nova_client().aggregates.add_host(aggregate_id, host_name)
        return True
    except Exception:
        log.exception("Error [add_host_to_aggregate(nova_client, %s, %s)]",
                      aggregate_id, host_name)
        return False

'''
def create_aggregate_with_host(nova_client, aggregate_name, av_zone,
                               compute_host):    # pragma: no cover
    try:
        create_aggregate(nova_client, aggregate_name, av_zone)
        add_host_to_aggregate(nova_client, aggregate_name, compute_host)
    except Exception:
        log.exception("Error [create_aggregate_with_host("
                      "nova_client, %s, %s, %s)]",
                      aggregate_name, av_zone, compute_host)
        return False
    else:
        return True
'''


def create_keypair(nova_client, name, key_path=None):    # pragma: no cover
    try:
        with open(key_path) as fpubkey:
            keypair = get_nova_client().keypairs.create(name=name, public_key=fpubkey.read())
            return keypair
    except Exception:
        log.exception("Error [create_keypair(nova_client)]")


def create_instance(json_body):    # pragma: no cover
    try:
        return get_nova_client().servers.create(**json_body)
    except Exception:
        log.exception("Error create instance failed")
        return None


def create_instance_and_wait_for_active(json_body):    # pragma: no cover
    SLEEP = 3
    VM_BOOT_TIMEOUT = 180
    nova_client = get_nova_client()
    instance = create_instance(json_body)
    count = VM_BOOT_TIMEOUT / SLEEP
    for n in range(count, -1, -1):
        status = get_instance_status(nova_client, instance)
        if status.lower() == "active":
            return instance
        elif status.lower() == "error":
            log.error("The instance went to ERROR status.")
            return None
        time.sleep(SLEEP)
    log.error("Timeout booting the instance.")
    return None


def add_secgroup_to_instance(nova_client, instance_id, secgroup_id):
    try:
        nova_client.servers.add_security_group(instance_id, secgroup_id)
        return True
    except Exception, e:
        log.error("Error [add_secgroup_to_instance(nova_client, '%s', "
                  "'%s')]: %s" % (instance_id, secgroup_id, e))
        return False


def attach_server_volume(server_id, volume_id, device=None):    # pragma: no cover
    try:
        get_nova_client().volumes.create_server_volume(server_id, volume_id, device)
    except Exception:
        log.exception("Error [attach_server_volume(nova_client, '%s', '%s')]",
                      server_id, volume_id)
        return False
    else:
        return True


def attach_server_volume(nova_client, server_id, volume_id):
    try:
        nova_client.volumes.create_server_volume(server_id, volume_id)
    except Exception:
        log.exception("Error [attach_server_volume(nova_client, '%s', '%s')]",
                      server_id, volume_id)
        return False
    else:
        return True


def attach_volume(server_id, volume_id, device=None):
    try:
        get_nova_client().volumes.create_server_volume(server_id, volume_id, device)
        return True
    except Exception:
        log.exception("Error [attach_server_volume(nova_client, '%s', '%s')]",
                      server_id, volume_id)
        return False


def detach_server_volume(nova_client, server_id, volume_id):
    try:
        nova_client.volumes.delete_server_volume(server_id, volume_id)
    except Exception:
        log.exception("Error [detach_server_volume(nova_client, '%s', '%s')]",
                      server_id, volume_id)
        return False
    else:
        return True


def shelve_server(nova_client, server_id):      # pragma: no cover
    try:
        nova_client.servers.shelve(server_id)
    except Exception:
        log.exception("Error [shelve_server(nova_client, '%s')]", server_id)
        return False
    else:
        return True


def wait_server_process_finish(nova_client, server_id, status,  \
                check_count=60, sleep_seconds=3):
    for n in range(check_count, -1, -1):
        ret_code = get_server_status(nova_client, server_id).lower()
        if ret_code == status:
            return True
        elif ret_code == "error":
            log.error("The instance went to ERROR status.")
            return False
        time.sleep(sleep_seconds)

    log.error("Timeout booting the instance.")
    return False


def delete_server(server_id):
    try:
        get_nova_client().servers.force_delete(server_id)
        return True
    except Exception:
        log.exception("Error [delete_instance(nova_client, '%s')]",
                      server_id)
        return False


def start_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.start(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'active')
        return result
    except Exception:
        log.exception("Error [start_instance(nova_client, '%s')]",
                      server_id)
        return False


def stop_server(server_id, should_wait=True):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.stop(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'shutoff')
        return result
    except Exception:
        log.exception("Error [stop_server(nova_client, '%s')]",
                      server_id)
        return False


def suspend_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.suspend(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'suspended')
        return result
    except Exception:
        log.exception("Error [suspend_server(nova_client, '%s')]",
                      server_id)
        return False


def resume_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.resume(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'active')
        return result
    except Exception:
        log.exception("Error [resume_server(nova_client, '%s')]",
                      server_id)
        return False


def pause_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.pause(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'paused')
        return result
    except Exception:
        log.exception("Error [pause_server(nova_client, '%s')]",
                      server_id)
        return False


def unpause_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.unpause(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'active')
        return result
    except Exception:
        log.exception("Error [unpause_server(nova_client, '%s')]",
                      server_id)
        return False


def lock_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.lock(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'active')
        return result
    except Exception:
        log.exception("Error [lock_server(nova_client, '%s')]",
                      server_id)
        return False


def unlock_server(server_id, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.unlock(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'active')
        return result
    except Exception:
        log.exception("Error [unlock_server(nova_client, '%s')]",
                      server_id)
        return False


def reboot_server(server_id, reboot_type, should_wait=False):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.reboot(server_id, reboot_type)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'active')
        return result
    except Exception:
        log.exception("Error [reboot_server(nova_client, '%s')]",
                      server_id)
        return False


def resize_server(server_id, flavor_id, disk_config, should_wait, **kwargs):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.resize(server_id, flavor_id, disk_config, **kwargs)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, 'verify_resize')
        return result
    except Exception:
        log.exception("Error [resize_server(nova_client, '%s')]",
                      server_id)
        return False


def confirm_resize(server_id, status, should_wait=True):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.confirm_resize(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, status)
        return result
    except Exception:
        log.exception("Error [confirm_resize(nova_client, '%s')]",
                      server_id)
        return False


def revert_resize(server_id, status, should_wait=True):
    result = True
    try:
        nova_client = get_nova_client()
        nova_client.servers.revert_resize(server_id)
        if should_wait:
            result = wait_server_process_finish(nova_client, server_id, status)
        return result
    except Exception:
        log.exception("Error [revert_resize(nova_client, '%s')]",
                      server_id)
        return False


def delete_instance(nova_client, instance_id):  # pragma: no cover
    try:
        nova_client.servers.force_delete(instance_id)
    except Exception:
        log.exception("Error [delete_instance(nova_client, '%s')]",
                      instance_id)
        return False
    else:
        return True


def remove_host_from_aggregate(aggregate_id, host):
    try:
        get_nova_client().aggregates.remove_host(aggregate_id, host)
    except Exception:
        log.exception("Error remove_host_from_aggregate(nova_client, %s, %s)",
                      aggregate_id, host)
        return False
    else:
        return True


def remove_hosts_from_aggregate(aggregate_id):   # pragma: no cover
    #aggregate_id = get_aggregate_id(nova_client, aggregate_name)
    hosts = get_nova_client().aggregates.get(aggregate_id).hosts
    assert(
        all(remove_host_from_aggregate(aggregate_id, host)
            for host in hosts))


def get_server_by_name(name):   # pragma: no cover
    try:
        return get_nova_client().servers.list(search_opts={'name': name})[0]
    except IndexError:
        log.exception('Failed to get nova client')
        raise


def create_flavor(name, ram, vcpus, disk, **kwargs):   # pragma: no cover
    try:
        return get_nova_client().flavors.create(name, ram, vcpus, disk, **kwargs)
    except Exception:
        log.exception("Error [create_flavor(nova_client, %s, %s, %s, %s, %s)]",
                      name, ram, disk, vcpus, kwargs['is_public'])
        return None


def get_image_by_name(name):    # pragma: no cover
    images = get_nova_client().images.list()
    try:
        return next((a for a in images if a.name == name))
    except StopIteration:
        log.exception('No image matched')


def get_flavor_id(nova_client, flavor_name):    # pragma: no cover
    flavors = nova_client.flavors.list(detailed=True)
    flavor_id = ''
    for f in flavors:
        if f.name == flavor_name:
            flavor_id = f.id
            break
    return flavor_id


def get_flavor_by_name(name):   # pragma: no cover
    flavors = get_nova_client().flavors.list()
    return next((a for a in flavors if a.name == name), None)


def get_flavor_by_id(flavor_id):
    return get_nova_client().flavors.get(flavor_id)


def get_flavor_by_instance_id(instance_id):
    nova_client = get_nova_client()
    instance = nova_client.servers.get(instance_id)
    return get_flavor_by_id(instance.flavor['id'])


def check_status(status, name, iterations, interval):   # pragma: no cover
    for i in range(iterations):
        try:
            server = get_server_by_name(name)
        except IndexError:
            log.error('Cannot found %s server', name)
            raise

        if server.status == status:
            return True

        time.sleep(interval)
    return False


def reset_server_state(server_id, state):
    try:
        return get_nova_client().servers.reset_state(server_id, state=state)
    except Exception:
        log.exception('Failed to reset server state.')
        raise


def create_keypair(nova_client, name, key_path=None):
    try:
        with open(key_path) as fpubkey:
            keypair = nova_client.keypairs.create(name=name,
                                                  public_key=fpubkey.read())
            return keypair
    except Exception:
        log.exception("Error [create_keypair(nova_client)]")


def delete_keypair(nova_client, key):     # pragma: no cover
    try:
        nova_client.keypairs.delete(key=key)
        return True
    except Exception:
        log.exception("Error [delete_keypair(nova_client)]")
        return False


def delete_flavor(flavor_id):    # pragma: no cover
    try:
        get_nova_client().flavors.delete(flavor_id)
    except Exception:
        log.exception("Error [delete_flavor(nova_client, %s)]", flavor_id)
        return False
    else:
        return True


def delete_keypair(nova_client, key):     # pragma: no cover
    try:
        nova_client.keypairs.delete(key=key)
        return True
    except Exception:
        log.exception("Error [delete_keypair(nova_client)]")
        return False


def update_server_name(server_id, new_server_name):    # pragma: no cover
    try:
        get_nova_client().servers.update(server_id, new_server_name)
    except Exception:
        log.exception("Error [update_server_name(nova_client, %s)]", server_id)
        return False
    else:
        return True


def update_flavor_name(nova_client, flavor_name_before, flavor_name, vcpus, ram, disk):
    try:
        flavor = get_flavor_by_name(flavor_name_before)
        delete_flavor(get_flavor_id(nova_client, flavor_name_before))
        create_flavor(flavor_name,ram,vcpus,disk)
    except Exception:
        log.exception("Error [update_flavor_name(flavor_name)]")
        return False
    else:
        return True


# *********************************************
#   NEUTRON
# *********************************************


def get_network_id(neutron_client, network_name):       # pragma: no cover
    networks = neutron_client.list_networks()['networks']
    return next((n['id'] for n in networks if n['name'] == network_name), None)


def get_network_id2(network_name):       # pragma: no cover
    try:
        networks = get_neutron_client().list_networks()['networks']
        return next((n['id'] for n in networks if n['name'] == network_name), None)
    except Exception, e:
        log.error("Error [get_network_id2(neutron_client)]: %s" % e)
        return None


def create_neutron_net(neutron_client, json_body):
    try:
        network = neutron_client.create_network(body=json_body)
        return network['network']['id']
    except Exception, e:
        log.error("Error [create_neutron_net(neutron_client)]: %s"
                  % (e))
        raise Exception("operation error")
        return None


def create_neutron_subnet(neutron_client, json_body):
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except Exception, e:
        log.error("Error [create_neutron_subnet , %s" % (e))
        raise Exception("operation error")
        return None

def update_neutron_subnet(subnet_id, json_body):
    try:
        get_neutron_client().update_subnet(subnet_id,json_body)
        return True
    except Exception:
        log.exception("Error [update_subnet(neutron_clent, %s)]",
                      subnet_id)
        return False

def update_neutron_network(network_id, json_body):
    try:
        get_neutron_client().update_network(network_id,json_body)
        return True
    except Exception:
        log.exception("Error [update_network(neutron_clent, %s)]",
                      network_id)
        return False

def create_neutron_router(neutron_client, json_body):
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except Exception, e:
        log.error("Error [create_neutron_router(neutron_client)]: %s"
                  % (e))
        raise Exception("operation error")
        return None


def add_interface_router(neutron_client, router_id, json_body):
    try:
        neutron_client.add_interface_router(router=router_id, body=json_body)
        return True
    except Exception, e:
        log.error("Error [add_interface_router(neutron_client)]: %s" % (e))
        return False


def add_gateway_router(neutron_client, ext_net_id, router_id, **json_body):
    json_body.update({'network_id': ext_net_id})
    try:
        neutron_client.add_gateway_router(router_id, json_body)
        return True
    except Exception, e:
        log.error("Error [add_gateway_router(neutron_client, '%s')]: %s"
                  % (router_id, e))
        return False


def remove_interface_router(neutron_client, router_id, subnet_id, **json_body):
    json_body.update({"subnet_id": subnet_id})
    try:
        neutron_client.remove_interface_router(router=router_id,
                                               body=json_body)
        return True
    except Exception, e:
        log.error("Error [remove_interface_router(neutron_client, '%s', "
                  "'%s')]: %s" % (router_id, subnet_id, e))
        return False


def remove_gateway_router(neutron_client, router_id):
    try:
        neutron_client.remove_gateway_router(router_id)
        return True
    except Exception, e:
        log.error("Error [remove_gateway_router(neutron_client, '%s')]: %s"
                  % (router_id, e))
        return False


def delete_neutron_router(neutron_client, router_id):
    try:
        neutron_client.delete_router(router=router_id)
        return True
    except Exception, e:
        log.error("Error [delete_neutron_router(neutron_client, '%s')]: %s"
                  % (router_id, e))
        return False


def delete_neutron_subnet(neutron_client, subnet_id):
    try:
        neutron_client.delete_subnet(subnet_id)
        return True
    except Exception, e:
        log.error("Error [delete_neutron_subnet(neutron_client, '%s')]: %s"
                  % (subnet_id, e))
        return False


def delete_neutron_net(neutron_client, network_id):
    try:
        neutron_client.delete_network(network_id)
        return True
    except Exception, e:
        log.error("Error [delete_neutron_net(neutron_client, '%s')]: %s"
                  % (network_id, e))
        return False


def delete_neutron_port(neutron_client, port_id):
    try:
        neutron_client.delete_port(port_id)
        return True
    except Exception, e:
        log.error("Error [delete_neutron_port(neutron_client, '%s')]: %s"
                  % (port_id, e))
        return False


def create_floating_ip(neutron_client, extnet_id):
    props = {'floating_network_id': extnet_id}
    try:
        ip_json = neutron_client.create_floatingip({'floatingip': props})
        fip_addr = ip_json['floatingip']['floating_ip_address']
        fip_id = ip_json['floatingip']['id']
    except Exception, e:
        log.error("Error [create_floating_ip(neutron_client)]: %s" % e)
        return None
    return {'fip_addr': fip_addr, 'fip_id': fip_id}


def add_floating_ip(nova_client, server_id, floatingip_addr):
    try:
        nova_client.servers.add_floating_ip(server_id, floatingip_addr)
        return True
    except Exception, e:
        log.error("Error [add_floating_ip(nova_client, '%s', '%s')]: %s"
                  % (server_id, floatingip_addr, e))
        return False


def delete_floating_ip(neutron_client, floatingip_id):
    try:
        #nova_client.floating_ips.delete(floatingip_id)
        neutron_client.delete_floatingip(floatingip_id)
        return True
    except Exception, e:
        log.error("Error [delete_floating_ip(nova_client, '%s')]: %s"
                  % (floatingip_id, e))
        return False


def create_network_association(neutron_client, bgpvpn_id,
                               neutron_network_id, **json_body):
    json_body.update({"network_association":
                     {"network_id": neutron_network_id}})
    return neutron_client.create_network_association(bgpvpn_id, json_body)


def create_router_association(neutron_client, bgpvpn_id,
                              router_id, **json_body):
    json_body.update({"router_association": {"router_id": router_id}})
    return neutron_client.create_router_association(bgpvpn_id, json_body)


def get_security_groups(neutron_client):
    try:
        security_groups = neutron_client.list_security_groups()[
            'security_groups']
        return security_groups
    except Exception, e:
        log.error("Error [get_security_groups(neutron_client)]: %s" % e)
        return None


def get_security_group_id(neutron_client, sg_name):
    security_groups = get_security_groups(neutron_client)
    id = ''
    for sg in security_groups:
        if sg['name'] == sg_name:
            id = sg['id']
            break
    return id


def create_security_group(neutron_client, sg_name, sg_description):
    json_body = {'security_group': {'name': sg_name,
                                    'description': sg_description}}
    try:
        secgroup = neutron_client.create_security_group(json_body)
        return secgroup['security_group']
    except Exception, e:
        log.error("Error [create_security_group(neutron_client, '%s', "
                  "'%s')]: %s" % (sg_name, sg_description, e))
        return None


def create_secgroup_rule(neutron_client, sg_id, direction, protocol,
                         port_range_min=None, port_range_max=None,
                         **json_body):
    # We create a security group in 2 steps
    # 1 - we check the format and set the json body accordingly
    # 2 - we call neturon client to create the security group

    # Format check
    json_body.update({'security_group_rule': {'direction': direction,
                     'security_group_id': sg_id, 'protocol': protocol}})
    # parameters may be
    # - both None => we do nothing
    # - both Not None => we add them to the json description
    # but one cannot be None is the other is not None
    if (port_range_min is not None and port_range_max is not None):
        # add port_range in json description
        json_body['security_group_rule']['port_range_min'] = port_range_min
        json_body['security_group_rule']['port_range_max'] = port_range_max
        log.debug("Security_group format set (port range included)")
    else:
        # either both port range are set to None => do nothing
        # or one is set but not the other => log it and return False
        if port_range_min is None and port_range_max is None:
            log.debug("Security_group format set (no port range mentioned)")
        else:
            log.error("Bad security group format."
                      "One of the port range is not properly set:"
                      "range min: {},"
                      "range max: {}".format(port_range_min,
                                             port_range_max))
            return False

    # Create security group using neutron client
    try:
        neutron_client.create_security_group_rule(json_body)
        return True
    except Exception:
        log.exception("Impossible to create_security_group_rule,"
                      "security group rule probably already exists")
        return False


def create_security_group_full(neutron_client,
                               sg_name, sg_description):
    sg_id = get_security_group_id(neutron_client, sg_name)
    if sg_id != '':
        log.info("Using existing security group '%s'..." % sg_name)
    else:
        log.info("Creating security group  '%s'..." % sg_name)
        SECGROUP = create_security_group(neutron_client,
                                         sg_name,
                                         sg_description)
        if not SECGROUP:
            log.error("Failed to create the security group...")
            return None

        sg_id = SECGROUP['id']

        log.debug("Security group '%s' with ID=%s created successfully."
                  % (SECGROUP['name'], sg_id))

        log.debug("Adding ICMP rules in security group '%s'..."
                  % sg_name)
        if not create_secgroup_rule(neutron_client, sg_id,
                                    'ingress', 'icmp'):
            log.error("Failed to create the security group rule...")
            return None

        log.debug("Adding SSH rules in security group '%s'..."
                  % sg_name)
        if not create_secgroup_rule(
                neutron_client, sg_id, 'ingress', 'tcp', '22', '22'):
            log.error("Failed to create the security group rule...")
            return None

        if not create_secgroup_rule(
                neutron_client, sg_id, 'egress', 'tcp', '22', '22'):
            log.error("Failed to create the security group rule...")
            return None
    return sg_id


def delete_security_group(neutron_client, secgroup_id):
    try:
        neutron_client.delete_security_group(secgroup_id)
        return True
    except Exception, e:
        log.error("Error [delete_security_group(neutron_client, '%s')]: %s"
                  % (secgroup_id, e))
        return False


def get_port_id_by_ip(neutron_client, ip_address):      # pragma: no cover
    ports = neutron_client.list_ports()['ports']
    return next((i['id'] for i in ports for j in i.get(
        'fixed_ips') if j['ip_address'] == ip_address), None)


def create_neutron_net(neutron_client, json_body):      # pragma: no cover
    try:
        network = neutron_client.create_network(body=json_body)
        return network['network']['id']
    except Exception:
        log.error("Error [create_neutron_net(neutron_client)]")
        raise Exception("operation error")
        return None


def delete_neutron_net(neutron_client, network_id):      # pragma: no cover
    try:
        neutron_client.delete_network(network_id)
        return True
    except Exception:
        log.error("Error [delete_neutron_net(neutron_client, '%s')]" % network_id)
        return False


def create_neutron_subnet(neutron_client, json_body):      # pragma: no cover
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except Exception:
        log.error("Error [create_neutron_subnet")
        raise Exception("operation error")
        return None


def create_neutron_router(neutron_client, json_body):      # pragma: no cover
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except Exception:
        log.error("Error [create_neutron_router(neutron_client)]")
        raise Exception("operation error")
        return None


def delete_neutron_router(neutron_client, router_id):      # pragma: no cover
    try:
        neutron_client.delete_router(router=router_id)
        return True
    except Exception:
        log.error("Error [delete_neutron_router(neutron_client, '%s')]" % router_id)
        return False


def remove_gateway_router(neutron_client, router_id):      # pragma: no cover
    try:
        neutron_client.remove_gateway_router(router_id)
        return True
    except Exception:
        log.error("Error [remove_gateway_router(neutron_client, '%s')]" % router_id)
        return False


def remove_interface_router(neutron_client, router_id, subnet_id,
                            **json_body):      # pragma: no cover
    json_body.update({"subnet_id": subnet_id})
    try:
        neutron_client.remove_interface_router(router=router_id,
                                               body=json_body)
        return True
    except Exception:
        log.error("Error [remove_interface_router(neutron_client, '%s', "
                  "'%s')]" % (router_id, subnet_id))
        return False


def create_floating_ip(neutron_client, extnet_id):      # pragma: no cover
    props = {'floating_network_id': extnet_id}
    try:
        ip_json = neutron_client.create_floatingip({'floatingip': props})
        fip_addr = ip_json['floatingip']['floating_ip_address']
        fip_id = ip_json['floatingip']['id']
    except Exception:
        log.error("Error [create_floating_ip(neutron_client)]")
        return None
    return {'fip_addr': fip_addr, 'fip_id': fip_id}


def get_security_groups(neutron_client):      # pragma: no cover
    try:
        security_groups = neutron_client.list_security_groups()[
            'security_groups']
        return security_groups
    except Exception:
        log.error("Error [get_security_groups(neutron_client)]")
        return None


def get_security_group_id(neutron_client, sg_name):      # pragma: no cover
    security_groups = get_security_groups(neutron_client)
    id = ''
    for sg in security_groups:
        if sg['name'] == sg_name:
            id = sg['id']
            break
    return id


def create_security_group(neutron_client, sg_name, sg_description):      # pragma: no cover
    json_body = {'security_group': {'name': sg_name,
                                    'description': sg_description}}
    try:
        secgroup = neutron_client.create_security_group(json_body)
        return secgroup['security_group']
    except Exception:
        log.error("Error [create_security_group(neutron_client, '%s', "
                  "'%s')]" % (sg_name, sg_description))
        return None


def create_secgroup_rule(neutron_client, sg_id, direction, protocol,
                         port_range_min=None, port_range_max=None,
                         **json_body):      # pragma: no cover
    # We create a security group in 2 steps
    # 1 - we check the format and set the json body accordingly
    # 2 - we call neturon client to create the security group

    # Format check
    json_body.update({'security_group_rule': {'direction': direction,
                     'security_group_id': sg_id, 'protocol': protocol}})
    # parameters may be
    # - both None => we do nothing
    # - both Not None => we add them to the json description
    # but one cannot be None is the other is not None
    if (port_range_min is not None and port_range_max is not None):
        # add port_range in json description
        json_body['security_group_rule']['port_range_min'] = port_range_min
        json_body['security_group_rule']['port_range_max'] = port_range_max
        log.debug("Security_group format set (port range included)")
    else:
        # either both port range are set to None => do nothing
        # or one is set but not the other => log it and return False
        if port_range_min is None and port_range_max is None:
            log.debug("Security_group format set (no port range mentioned)")
        else:
            log.error("Bad security group format."
                      "One of the port range is not properly set:"
                      "range min: {},"
                      "range max: {}".format(port_range_min,
                                             port_range_max))
            return False

    # Create security group using neutron client
    try:
        neutron_client.create_security_group_rule(json_body)
        return True
    except Exception:
        log.exception("Impossible to create_security_group_rule,"
                      "security group rule probably already exists")
        return False


def create_security_group_full(neutron_client,
                               sg_name, sg_description):      # pragma: no cover
    sg_id = get_security_group_id(neutron_client, sg_name)
    if sg_id != '':
        log.info("Using existing security group '%s'..." % sg_name)
    else:
        log.info("Creating security group  '%s'..." % sg_name)
        SECGROUP = create_security_group(neutron_client,
                                         sg_name,
                                         sg_description)
        if not SECGROUP:
            log.error("Failed to create the security group...")
            return None

        sg_id = SECGROUP['id']

        log.debug("Security group '%s' with ID=%s created successfully."
                  % (SECGROUP['name'], sg_id))

        log.debug("Adding ICMP rules in security group '%s'..."
                  % sg_name)
        if not create_secgroup_rule(neutron_client, sg_id,
                                    'ingress', 'icmp'):
            log.error("Failed to create the security group rule...")
            return None

        log.debug("Adding SSH rules in security group '%s'..."
                  % sg_name)
        if not create_secgroup_rule(
                neutron_client, sg_id, 'ingress', 'tcp', '22', '22'):
            log.error("Failed to create the security group rule...")
            return None

        if not create_secgroup_rule(
                neutron_client, sg_id, 'egress', 'tcp', '22', '22'):
            log.error("Failed to create the security group rule...")
            return None
    return sg_id


# *********************************************
#   GLANCE
# *********************************************
def get_image_by_name(glance_client, image_name):    # pragma: no cover
    images = glance_client.images.list()
    return next((i for i in images if i.name == image_name), None)


def get_image_by_name2(image_name):
    images = get_glance_client().images.list()
    return next((i for i in images if i.name == image_name), None)


def get_image_id(glance_client, image_name):    # pragma: no cover
    images = glance_client.images.list()
    return next((i.id for i in images if i.name == image_name), None)


def update_image(glance_client, image_id, **kwargs):
    for key, value in kwargs.items():
        try:
            glance_client.images.update(image_id, **{key: value})
        except Exception:
            log.exception("Error updating image with %s: %s", key, value)
            return False
    return True


def create_image_from_instance(server_id, image_name):
    try:
        get_nova_client().servers.create_image(server_id, image_name, metadata=None)
    except Exception:
        log.exception("Error [create_image_from_instance(nova_client, %s)]", server_id)
        return False
    else:
        return True


def create_image(glance_client, image_name, file_path, disk_format,
                 container_format, min_disk, min_ram, protected, tag,
                 public, **kwargs):    # pragma: no cover
    if not os.path.isfile(file_path):
        log.error("Error: file %s does not exist." % file_path)
        return None
    try:
        image_id = get_image_id(glance_client, image_name)
        if image_id is not None:
            log.info("Image %s already exists." % image_name)
        else:
            log.info("Creating image '%s' from '%s'...", image_name, file_path)

            image = glance_client.images.create(name=image_name,
                                                visibility=public,
                                                disk_format=disk_format,
                                                container_format=container_format,
                                                min_disk=min_disk,
                                                min_ram=min_ram,
                                                tags=tag,
                                                protected=protected,
                                                **kwargs)
            image_id = image.id
            with open(file_path) as image_data:
                glance_client.images.upload(image_id, image_data)
        return image_id
    except Exception:
        log.error("Error [create_glance_image(glance_client, '%s', '%s', '%s')]",
                  image_name, file_path, public)
        return None


def delete_image(glance_client, image_id):    # pragma: no cover
    try:
        glance_client.images.delete(image_id)

    except Exception:
        log.exception("Error [delete_flavor(glance_client, %s)]", image_id)
        return False
    else:
        return True


# *********************************************
#   CINDER
# *********************************************
def get_volume_status(cinder_client, volume_id):     # pragma: no cover
    try:
        return cinder_client.volumes.get(volume_id).status
    except Exception:
        log.exception("Error [get_server_status(nova_client)]")


def wait_volume_process_finish(cinder_client, volume_id, status,  \
                check_count=60, sleep_seconds=3):
    for n in range(check_count, -1, -1):
        ret_code = get_volume_status(cinder_client, volume_id).lower()
        if ret_code == status:
            return True
        elif ret_code == "error":
            log.error("The volume went to ERROR status.")
            return False
        time.sleep(sleep_seconds)

    log.error("Timeout process the volume.")
    return False


def get_volume_id(volume_name):    # pragma: no cover
    volumes = get_cinder_client().volumes.list()
    return next((v.id for v in volumes if v.name == volume_name), None)


def create_volume(cinder_client, volume_name, volume_size,
                  volume_image=False):    # pragma: no cover
    try:
        if volume_image:
            volume = cinder_client.volumes.create(name=volume_name,
                                                  size=volume_size,
                                                  imageRef=volume_image)
        else:
            volume = cinder_client.volumes.create(name=volume_name,
                                                  size=volume_size)
        return volume
    except Exception:
        log.exception("Error [create_volume(cinder_client, %s)]",
                      (volume_name, volume_size))
        return None

def create_volume1(cinder_client, volume_name, volume_size, volume_type,
                  volume_image=False):    # pragma: no cover
    try:
        if volume_image:
            volume = cinder_client.volumes.create(name=volume_name,
                                                  size=volume_size,
                                                  volume_type=volume_type,
                                                  imageRef=volume_image)
        else:
            volume = cinder_client.volumes.create(name=volume_name,
                                                  size=volume_size,
                                                  volume_type=volume_type)
        return volume
    except Exception:
        log.exception("Error [create_volume(cinder_client, %s)]",
                      (volume_name, volume_size))
        return None

def create_volume2(volume_name, volume_size, should_wait=True, **kwargs):
    try:
        cinder_client = get_cinder_client()
        volume = cinder_client.volumes.create(volume_size, name=volume_name, **kwargs)
        if should_wait:
            wait_volume_process_finish(cinder_client, volume.id, 'available')
        return volume
    except Exception:
        log.exception("Error [create_volume(cinder_client, %s, %s)]",
                      (volume_name, volume_size))
        return None

def get_snapshot_status(cinder_client, snapshot_id):     # pragma: no cover
    try:
        return cinder_client.volume_snapshots.get(snapshot_id).status
    except Exception:
        log.exception("Error [get_snapshot_status(nova_client)]")

def wait_snapshot_process_finish(cinder_client, snapshot_id, status, \
                check_count=60, sleep_seconds=3):
    for n in range(check_count, -1, -1):
        ret_code = get_snapshot_status(cinder_client, snapshot_id).lower()
        if ret_code == status:
            return True
        elif ret_code == "error":
            log.error("The snapshot went to ERROR status.")
            return False
        time.sleep(sleep_seconds)

    log.error("Timeout process the volume.")
    return False

def create_snapshot(volume_id, snapshot_name, force, should_wait=True, **kwargs):
    try:
        cinder_client = get_cinder_client()
        snapshot = cinder_client.volume_snapshots.create(volume_id,
                                                         name=snapshot_name,
                                                         force=force,
                                                         **kwargs)

        if should_wait:
            wait_snapshot_process_finish(cinder_client, snapshot.id, 'available')
        return snapshot

    except Exception:
        log.exception("Error [create_snapshot(cinder_client, %s, %s)]",
                      (volume_id, snapshot_name))
        return None

def get_snapshot_by_name(name):   # pragma: no cover
    try:
        return get_cinder_client().volume_snapshots.list(search_opts={'name': name})[0]
    except IndexError:
        log.exception('Failed to get snapshot.')
        raise

def create_volume_from_snapshot(volume_size, snapshot_id, volume_name, should_wait=True, **kwargs):
    try:
        cinder_client = get_cinder_client()
        volume = cinder_client.volumes.create(volume_size,
                                                   snapshot_id=snapshot_id,
                                                   name=volume_name,
                                                   **kwargs)
        if should_wait:
            wait_volume_process_finish(cinder_client, volume.id, 'available')
        return volume

    except Exception:
        log.exception("Error [create_volume(cinder_client, %s, %s)]",
                      (snapshot_id, volume_name))
        return None

def create_volume_from_volume(volume_name, volume_size, volume_id, should_wait=True, **kwargs):
    try:
        cinder_client = get_cinder_client()
        volume = cinder_client.volumes.create(name=volume_name,
                                                  size=volume_size,
                                                  source_volid=volume_id,
                                                  **kwargs)
        if should_wait:
            wait_volume_process_finish(cinder_client, volume.id, 'available')
        return volume

    except Exception:
        log.exception("Error [create_volume(cinder_client, %s, %s)]",
                     (volume_name, volume_size))
        return None

def delete_snapshot(cinder_client, snapshot_id, forced=False):

    try:
        cinder_client.volume_snapshots.delete(snapshot_id, force=forced)
        return True
    except Exception:
        log.exception("Error [delete_snapshot(cinder_client, '%s')]" % snapshot_id)
        return False

def extend_volume(volume_id, new_size):
    try:
        cinder_client = get_cinder_client()
        cinder_client.volumes.extend(volume_id, new_size)
        wait_volume_process_finish(cinder_client, volume_id, 'available')
        return True
    except Exception:
        log.exception("Error [extend_volume(cinder_client, %s, %s)]",
                      (volume_id, new_size))
        return False


def get_volume_by_name(name):   # pragma: no cover
    try:
        return get_cinder_client().volumes.list(search_opts={'name': name})[0]
    except IndexError:
        log.exception('Failed to get nova client')
        raise


def check_volumestatus(status, name, iterations, interval):
    for i in range(iterations):
        try:
            volume = get_volume_by_name(name)
        except IndexError:
            log.error('Cannot found %s volume', name)
            raise

        if volume.status == status:
            return True

        time.sleep(interval)
    return False


def get_volume_by_id(cinder_client, volume_id):
    volumes = cinder_client.volumes.list(search_opts={'all_tenants': 1})
    return next((v for v in volumes if v.id == volume_id), None)


def delete_volume(cinder_client, volume_id, forced=False):      # pragma: no cover
    try:
        if forced:
            try:
                cinder_client.volumes.detach(volume_id)
            except:
                log.error(sys.exc_info()[0])
            cinder_client.volumes.force_delete(volume_id)
        else:
            while True:
                volume = get_cinder_client().volumes.get(volume_id)
                if volume.status.lower() == 'available':
                    break
            cinder_client.volumes.delete(volume_id)
        return True
    except Exception:
        log.exception("Error [delete_volume(cinder_client, '%s')]" % volume_id)
        return False


def delete_volume2(volume_id):
    try:
        get_cinder_client().volumes.delete(volume_id)
        return True
    except Exception:
        log.exception("Error [delete_volume(cinder_client, '%s')]" % volume_id)
        return False,


def cinder_get_prj_usage(tenant_id, usage=False):
    try:
        return get_cinder_client().quotas.get(tenant_id, usage)
    except Exception:
        log.exception("Error [delete_volume(cinder_client, '%s')]" % tenant_id)
        return None
def detach_volume(server_id, volume_id):      # pragma: no cover
    try:
        get_nova_client().volumes.delete_server_volume(server_id, volume_id)
        return True
    except Exception:
        log.exception("Error [detach_server_volume(nova_client, '%s', '%s')]",
                      server_id, volume_id)
        return False
