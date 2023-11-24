# Copyright 2018, Radware LTD. All rights reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from threading import Thread

from oslo_log import log as logging

from octavia.common import utils as common_utils
from octavia_lib.api.drivers import exceptions
from octavia_lib.api.drivers import provider_base as driver_base
from octavia_lib.api.drivers import driver_lib
from octavia_lib.api.drivers import data_models
from octavia.network.drivers.neutron.allowed_address_pairs import AllowedAddressPairsDriver

from . import config
from . import dm_utils
from . import feedback
from . import radware_provider_exceptions
from . import vdirect_adc_wf_driver
from . import monitoring

LOG = logging.getLogger(__name__)

AGENT_PROCESS_STARTED = False


def exception_transformator(f):
    def transformator(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
        except vdirect_adc_wf_driver.VDirectADCWorkflowDriverException as e:
            if isinstance(e, vdirect_adc_wf_driver.ConfigurationConflict):
                raise radware_provider_exceptions.ConfigurationConflict(
                conflict_description=e.conflict_description)
            elif isinstance(e, vdirect_adc_wf_driver.RESTRequestFailure):
                raise radware_provider_exceptions.RESTRequestFailure(
                    status=e.status, reason=e.reason,
                    description=e.description, success_codes=e.success_codes)
            elif isinstance(e, vdirect_adc_wf_driver.WorkflowTemplateMissing):
                raise radware_provider_exceptions.WorkflowTemplateMissing(
                    workflow_template=e.template_name)
        return r
    return transformator


class RadwareOctaviaProviderDriver(driver_base.ProviderDriver):
    @exception_transformator
    def __init__(self, **kwargs):

        super(RadwareOctaviaProviderDriver, self).__init__()

        self.service_consumer = 'Octavia'
        self.config = config.RadwareConfFileConfig(
            '/etc/radware/octavia_driver.conf',
            kwargs.get('name'))

        self.wf_driver = vdirect_adc_wf_driver.VDirectADCWorkflowDriver(
            self.service_consumer, self.config)

        if self.config.enable_monitoring:
            self._start_monitoring_process ()

    def create_vip_port(self, loadbalancer_id, project_id, vip_dictionary):
        raise exceptions.NotImplementedError()

    def _start_monitoring_process (self):
        global AGENT_PROCESS_STARTED
        if not AGENT_PROCESS_STARTED:
            p = monitoring.Monitor(self,
                                   status_feedback=feedback.update_operating_status,
                                   stats_feedback=feedback.update_statistics)
            p.name = "Monitoring"
            p.daemon = True
            p.start()
            AGENT_PROCESS_STARTED = True

    @exception_transformator
    def _create_lb(self, lb_pdm):
        neutron_driver = AllowedAddressPairsDriver()
        subnet_db = neutron_driver.get_subnet(lb_pdm.vip_subnet_id)
        params = {'vip_network_id': lb_pdm.vip_network_id,
                  'vip_subnet_id': lb_pdm.vip_subnet_id,
                  'vip_subnet_cidr': subnet_db.cidr}

        result = self.wf_driver.create_lb_workflow(
            lb_pdm.loadbalancer_id, params, lb_pdm.project_id)
        print('EVG:_create_lb:result')
        print(result)
        t = Thread(target=feedback.post_lb_create,
                   kwargs=dict(lb_id=lb_pdm.loadbalancer_id, result=result))
        t.start()

    @exception_transformator
    def _configure_lb(self, dm, create=False, delete=False):
        lb_pdm, statuses, payload = dm_utils.get_lb_and_graph(dm, create=create, delete=delete)

        if not self.wf_driver.lb_workflow_exists(lb_pdm.loadbalancer_id):
            self._create_lb(lb_pdm)

        deleted_id = None if not delete else dm_utils.get_pdm_id(dm)
        params = payload

        result = self.wf_driver.run_workflow_action(
            lb_pdm.loadbalancer_id, self.config.configure_action_name, params)
        t = Thread(target=feedback.post_lb_configure,
                   kwargs=dict(deleted_id=deleted_id, statuses=statuses, result=result))
        t.start()

    @exception_transformator
    def _delete_member(self, dm):
        lb_pdm, statuses, payload = dm_utils.get_lb_and_graph(dm, delete=True)
        n_driver = common_utils.get_network_driver()
        member_subnet = n_driver.get_subnet(dm.subnet_id)
        data = {'id': dm.member_id,
                'pool_id': dm.pool_id,
                'address': dm.address,
                'protocol_port': dm.protocol_port,
                'weight': 1 + int(dm.weight / 5),
                'admin_state_up': dm.admin_state_up,
                'subnet_id': dm.subnet_id,
                'subnet_cidr': member_subnet.cidr,
                'network_id': member_subnet.network_id}

        if not self.wf_driver.lb_workflow_exists(lb_pdm.loadbalancer_id):
            self._create_lb(lb_pdm)

        result = self.wf_driver.run_workflow_action(
            lb_pdm.loadbalancer_id, 'remove_real_server', {'member': data})
        t = Thread(target=feedback.post_lb_configure,
                   kwargs=dict(deleted_id=dm_utils.get_pdm_id(dm), statuses=statuses, result=result))
        t.start()

    @exception_transformator
    def _delete_pool(self, dm):
        lb_pdm, statuses, payload = dm_utils.get_lb_and_graph(dm, delete=True)

        members = dm_utils.get_pool_members(dm.pool_id, False, None, None)
        listeners = dm_utils.get_pool_listeners(dm.pool_id, False, None, None)

        if not self.wf_driver.lb_workflow_exists(lb_pdm.loadbalancer_id):
            self._create_lb(lb_pdm)

        result = self.wf_driver.run_workflow_action(
            lb_pdm.loadbalancer_id, 'delete_pool', {'pool_id': dm.pool_id, 'members': members, 'listeners': listeners})
        t = Thread(target=feedback.post_lb_configure,
                   kwargs=dict(deleted_id=dm_utils.get_pdm_id(dm), statuses=statuses, result=result))
        t.start()

    def loadbalancer_create(self, lb_provider_dm):
        lb_pdm, statuses, payload = dm_utils.get_lb_and_graph(lb_provider_dm, create=True)

        n_driver = common_utils.get_network_driver()
        port = n_driver.get_port(lb_provider_dm.vip_port_id)
        port_update_data = {'port': {'port_security_enabled': False, 'security_groups': []}}

        n_driver.neutron_client.update_port(port.id, port_update_data)

        self._create_lb(lb_pdm)

    def loadbalancer_update(self, old_loadbalancer_provider_dm,
                            loadbalancer_provider_dm):

        # Merging and using merged object is not performed
        # as a result of Octavia bug. https://review.openstack.org/#/c/605376
        #merged = dm_utils.merge_updated(old_loadbalancer_provider_dm, loadbalancer_provider_dm)

        self._configure_lb(loadbalancer_provider_dm)

    def loadbalancer_delete(self, lb_provider_dm, cascade):
        result = self.wf_driver.remove_lb_workflow(lb_provider_dm.loadbalancer_id)
        t = Thread(target=feedback.post_lb_delete,
                   kwargs=dict(lb_id=lb_provider_dm.loadbalancer_id, result=result))
        t.start()

    def loadbalancer_failover(self, loadbalancer_id):
        raise exceptions.NotImplementedError()

    @exception_transformator
    def listener_create(self, listener_provider_dm):
        self.wf_driver.validate_listener(
            listener_provider_dm.protocol,
            listener_provider_dm.protocol_port)
        self._configure_lb(listener_provider_dm, create=True)

    def listener_update(self, old_listener_provider_dm,
                        listener_provider_dm):
        merged = dm_utils.merge_updated(old_listener_provider_dm, listener_provider_dm)
        self._configure_lb(merged)

    def listener_delete(self, listener_provider_dm):
        self._configure_lb(listener_provider_dm, delete=True)

    def pool_create(self, pool_provider_dm):
        self._configure_lb(pool_provider_dm, create=True)

    def pool_update(self, old_pool_provider_dm,
                    pool_provider_dm):
        merged = dm_utils.merge_updated(old_pool_provider_dm, pool_provider_dm)
        self._configure_lb(merged)

    def pool_delete(self, pool_provider_dm):
        self._delete_pool(pool_provider_dm)

    def member_create(self, member_provider_dm):
        self.wf_driver.validate_member(member_provider_dm)
        self._configure_lb(member_provider_dm, create=True)

    def member_update(self, old_member_provider_dm,
                      member_provider_dm):
        self.wf_driver.validate_member(member_provider_dm)
        merged = dm_utils.merge_updated(old_member_provider_dm, member_provider_dm)
        self._configure_lb(merged)

    def member_delete(self, member_provider_dm):
        self._delete_member(member_provider_dm)

    def member_batch_update(self, members):
        raise exceptions.NotImplementedError()

    def health_monitor_create(self, hm_provider_dm):
        self.wf_driver.validate_hm(hm_provider_dm)
        self._configure_lb(hm_provider_dm, create=True)

    def health_monitor_update(self, old_hm_provider_dm,
                              hm_provider_dm):
        self.wf_driver.validate_hm(hm_provider_dm)
        merged = dm_utils.merge_updated(old_hm_provider_dm, hm_provider_dm)
        self._configure_lb(merged)

    def health_monitor_delete(self, hm_provider_dm):
        self._configure_lb(hm_provider_dm, delete=True)

    def l7policy_create(self, l7policy_provider_dm):
        self._configure_lb(l7policy_provider_dm, create=True)

    def l7policy_update(self, old_l7policy_provider_dm,
                        l7policy_provider_dm):
        merged = dm_utils.merge_updated(old_l7policy_provider_dm, l7policy_provider_dm)
        self._configure_lb(merged)

    def l7policy_delete(self, l7policy_provider_dm):
        self._configure_lb(l7policy_provider_dm, delete=True)

    def l7rule_create(self, l7rule_provider_dm):
        self._configure_lb(l7rule_provider_dm, create=True)

    def l7rule_update(self, old_l7rule_provider_dm,
                      l7rule_provider_dm):
        merged = dm_utils.merge_updated(old_l7rule_provider_dm, l7rule_provider_dm)
        self._configure_lb(merged)

    def l7rule_delete(self, l7rule_provider_dm):
        self._configure_lb(l7rule_provider_dm, delete=True)
