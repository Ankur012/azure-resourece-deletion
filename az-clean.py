#!/usr/bin/python
import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient


def get_credentials(client_id, secret, tenant):
    credentials = ServicePrincipalCredentials(
        client_id=client_id,
        secret=secret,
        tenant=tenant
    )

    return credentials, subscription_id


def get_vm_list(component, rg_location):
    delete_vm_list = []
    print(vms)
    try:
        for i in vms:
            vm_state = compute_client.virtual_machines.instance_view(resource_group_name=resource_group, vm_name=i.name)
            x = i.tags
            if 'tags_key' in x and x['tags_key'] == 'True' and x['component'] == component and vm_state.statuses[1].code == 'PowerState/deallocated':
                delete_vm_list.append(i.name)
    except Exception as e:
        print(e)

    return delete_vm_list
def get_snapshots_list(component, rg_location):
    delete_snap_list = []
    try:
        for disk in snaps:
            y = disk.tags
            if y is not None and 'tags_key' in y and y['tags_key'] == 'True' and y['component'] == component:
                delete_snap_list.append(disk.name)
    except Exception as e:
        print(e)
    return delete_snap_list


def get_nic_list(component, rg_location):
    delete_nic_list = []
    try:
        for nic in nics:
            z = nic.tags
            if z is not None and 'tags_key' in z and z['tags_key'] == 'True' and z['component'] == component:
                delete_nic_list.append(nic.name)

    except Exception as e:
        print(e)
    return delete_nic_list


def get_disk_list(component, rg_location):
    delete_disk_list = []
    try:
        for disk in disks:
            d = disk.tags
            if d is not None and 'tags_key' in d and d['tags_key'] == 'True' and  d['component'] == component:
                delete_disk_list.append(disk.name)
    except Exception as e:
        print(e)
    return delete_disk_list


def delete_vm(get_vm_list):
    vm_delete_result = []
    try:
        for i in get_vm_list:
            print(i)
            async_vm_deletion = compute_client.virtual_machines.delete(resource_group_name=resource_group, vm_name=i)
            async_vm_deletion.wait()
            print(async_vm_deletion.result())
            vm_delete_result.append(async_vm_deletion.result())
    except Exception as e:
        print(e)
    return vm_delete_result


def delete_snapshots(get_snapshots_list):
    snapshots_delete_result = []
    try:
        for i in get_snapshots_list:
            print(i)
            async_snapshots_deletion = compute_client.snapshots.delete(resource_group_name=resource_group,
                                                                       snapshot_name=i)
#            async_snapshots_deletion.wait()
            print(async_snapshots_deletion.result())
            snapshots_delete_result.append(async_snapshots_deletion.result())
    except Exception as e:
        print(e)
    return snapshots_delete_result


def delete_nic(get_nic_list):
    nic_delete_result = []
    try:
        for i in get_nic_list:
            print(i)
            async_nic_deletion = network_client.network_interfaces.delete(resource_group_name=resource_group,
                                                                          network_interface_name=i)
#            async_nic_deletion.wait()
            print(async_nic_deletion.result())
            nic_delete_result.append(async_nic_deletion.result())
    except Exception as e:
        print(e)
    return nic_delete_result


def delete_disk(disk_list):
    disk_delete_result = []
    try:
        for i in disk_list:
            print(i)
            async_disk_deletion = compute_client.disks.delete(resource_group_name=resource_group, disk_name=i)
#            async_disk_deletion.wait()
            print(async_disk_deletion.result())
            disk_delete_result.append(async_disk_deletion.result())
    except Exception as e:
        print(e)
    return disk_delete_result


if __name__ == "__main__":
    # module = AnsibleModule(
    #     argument_spec=dict(
    #         subscription_id=dict(required=True),
    #         resource_group=dict(required=True),
    #         client_id=dict(required=True),
    #         client_secret=dict(required=True),
    #         tenant_id=dict(required=True),
    #         action=dict(required=True),
    #         component_name=dict(required=True)
    #     )
    # )

    # subscription_id = 'abcd'
    # resource_group = 'abcd'
    # client_id = 'abcd'
    # secret = 'abcd'
    # tenant = 'abcd'
    # component = 'abcd'
    # status = ""
    # action = "clean"



    credentials, subscription_id = get_credentials(client_id, secret, tenant)
    compute_client = ComputeManagementClient(credentials, subscription_id)
    network_client = NetworkManagementClient(credentials, subscription_id)
    resource_client = ResourceManagementClient(credentials, subscription_id)
    snaps = compute_client.snapshots.list_by_resource_group(resource_group)
    disks = compute_client.disks.list_by_resource_group(resource_group)
    vms = compute_client.virtual_machines.list(resource_group)
    nics = network_client.network_interfaces.list(resource_group)
    rg = resource_client.resource_groups.get(resource_group)
    rg_location = rg.location

    status = ""
    vm_list = ""
    msg_vm_name = ""
    snapshots_list = ""
    msg_snap_name = ""
    nic_list = ""
    msg_nic_name = ""
    disk_list = ""
    msg_disk_name = ""

    vm_list = get_vm_list(component, rg_location)
    msg_vm_name = ' '.join([str(elem) for elem in vm_list])
    print(len(vm_list))
    if len(vm_list) != '0':
        snapshots_list = get_snapshots_list(component, rg_location)
        nic_list = get_nic_list(component, rg_location)
        disk_list = get_disk_list(component, rg_location)
    if action == 'clean':
        if len(vm_list) != '0':
            delete_vm(vm_list)
            delete_disk(disk_list)
            delete_snapshots(snapshots_list)
            delete_nic(nic_list)






