import logging

from spaceone.core import config
from spaceone.core.manager import BaseManager
from spaceone.core.connector.space_connector import SpaceConnector
from spaceone.core import cache

_LOGGER = logging.getLogger(__name__)


class IdentityManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identity_connector: SpaceConnector = self.locator.get_connector('SpaceConnector', service='identity',
                                                                             token=config.get_global('TOKEN'))

    def list_projects(self, query, domain_id):
        return self.identity_connector.dispatch('Project.list', {'query': query, 'domain_id': domain_id})

    @cache.cacheable(key='project-name:{domain_id}:{project_id}', expire=300)
    def get_project_name(self, project_id, domain_id):
        try:
            project_info = self.get_project(project_id, domain_id)
            return f'{project_info["project_group_info"]["name"]} > {project_info["name"]}'
        except Exception as e:
            _LOGGER.error(f'[get_project_name] API Error: {e}')
            return project_id

    def get_project(self, project_id, domain_id):
        return self.identity_connector.dispatch('Project.get', {'project_id': project_id, 'domain_id': domain_id})

    def list_project_groups(self, query, domain_id):
        return self.identity_connector.dispatch('ProjectGroup.list', {'query': query, 'domain_id': domain_id})

    def get_project_group(self, project_group_id, domain_id):
        return self.identity_connector.dispatch('ProjectGroup.get', {'project_group_id': project_group_id,
                                                                     'domain_id': domain_id})

    def list_projects_in_project_group(self, project_group_id, domain_id, recursive=False, query=None):
        request = {
            'project_group_id': project_group_id,
            'domain_id': domain_id,
            'recursive': recursive
        }

        if query:
            request['query'] = query

        return self.identity_connector.dispatch('ProjectGroup.list_projects', request)

    def get_service_account(self, service_account_id, domain_id):
        return self.identity_connector.dispatch('ServiceAccount.get', {'service_account_id': service_account_id,
                                                                       'domain_id': domain_id})

    def list_service_accounts(self, query, domain_id):
        return self.identity_connector.dispatch('ServiceAccount.list', {'query': query, 'domain_id': domain_id})
