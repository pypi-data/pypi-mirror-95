# -*- coding: utf-8 -*-

from requests import post, get
from typing import Any, cast, Dict, List, Optional, Sequence, Union

DEFAULT_TESTRAIL_HEADERS = {'Content-Type': 'application/json'}
TESTRAIL_STATUS_ID_PASSED = 1

# custom types
JsonDict = Dict[str, Any]  # noqa: E993
JsonList = List[JsonDict]  # noqa: E993
Id = Union[str, int]  # noqa: E993


class TestRailAPIClient(object):
    """Library for working with [http://www.gurock.com/testrail/ | TestRail].

    == Dependencies ==
    | requests | https://pypi.python.org/pypi/requests |

    == Preconditions ==
    1. [ http://docs.gurock.com/testrail-api2/introduction | Enable TestRail API]
    """

    def __init__(self, server: str, user: str, password: str, run_id: Id, protocol: str = 'http') -> None:
        """Create TestRailAPIClient instance.

        *Args:*\n
            _server_ - name of TestRail server;\n
            _user_ - name of TestRail user;\n
            _password_ - password of TestRail user;\n
            _run_id_ - ID of the test run;\n
            _protocol_ - connecting protocol to TestRail server: http or https.
        """
        self._url = '{protocol}://{server}/index.php?/api/v2/'.format(protocol=protocol, server=server)
        self._user = user
        self._password = password
        self.run_id = run_id

    def _send_post(self, uri: str, data: Dict[str, Any]) -> Union[JsonList, JsonDict]:
        """Perform post request to TestRail.

        *Args:* \n
            _uri_ - URI for test case;\n
            _data_ - json with test result.

        *Returns:* \n
            Request result in json format.
        """
        url = self._url + uri
        response = post(url, json=data, auth=(self._user, self._password), verify=False)
        response.raise_for_status()
        return response.json()

    def _send_get(self, uri: str, headers: Dict[str, str] = None,
                  params: Dict[str, Any] = None) -> Union[JsonList, JsonDict]:
        """Perform get request to TestRail.

        *Args:* \n
            _uri_ - URI for test case;\n
            _headers_ - headers for http-request;\n
            _params_ - parameters for http-request.

        *Returns:* \n
            Request result in json format.
        """
        url = self._url + uri
        response = get(url, headers=headers, params=params, auth=(self._user, self._password), verify=False)
        response.raise_for_status()
        return response.json()

    def get_tests(self, run_id: Id, status_ids: Union[str, Sequence[int]] = None) -> JsonList:
        """Get tests from TestRail test run by run_id.

        *Args:* \n
            _run_id_ - ID of the test run;\n
            _status_ids_ - list of the required test statuses.

        *Returns:* \n
            Tests information in json format.
        """
        uri = 'get_tests/{run_id}'.format(run_id=run_id)
        if status_ids:
            status_ids = ','.join(str(status_id) for status_id in status_ids)
        params = {
            'status_id': status_ids
        }
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS, params=params)
        return cast(JsonList, response)

    def get_results_for_case(self, run_id: Id, case_id: Id, limit: int = None) -> JsonList:
        """Get results for case by run_id and case_id.

        *Args:* \n
            _run_id_ - ID of the test run;\n
            _case_id_ - ID of the test case;\n
            _limit_ - limit of case results.

        *Returns:* \n
            Cases results in json format.
        """
        uri = 'get_results_for_case/{run_id}/{case_id}'.format(run_id=run_id, case_id=case_id)
        params = {
            'limit': limit
        }
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS, params=params)
        return cast(JsonList, response)

    def add_result_for_case(self, run_id: Id, case_id: Id,
                            test_result_fields: Dict[str, Union[str, int]]) -> None:
        """Add results for case in TestRail test run by run_id and case_id.

        *Supported request fields for test result:*\n
        | *Name*        | *Type*   | *Description*                                                |
        | status_id     | int      | The ID of the test status                                    |
        | comment       | string   | The comment / description for the test result                |
        | version       | string   | The version or build you tested against                      |
        | elapsed       | timespan | The time it took to execute the test, e.g. "30s" or "1m 45s" |
        | defects       | string   | A comma-separated list of defects to link to the test result |
        | assignedto_id | int      | The ID of a user the test should be assigned to              |
        | Custom fields are supported as well and must be submitted with their system name, prefixed with 'custom_' |

        *Args:* \n
            _run_id_ - ID of the test run;\n
            _case_id_ - ID of the test case;\n
            _test_result_fields_ - result of the test fields dictionary.

        *Example:*\n
        | Add Result For Case | run_id=321 | case_id=123| test_result={'status_id': 3, 'comment': 'This test is untested', 'defects': 'DEF-123'} |
        """
        uri = 'add_result_for_case/{run_id}/{case_id}'.format(run_id=run_id, case_id=case_id)
        self._send_post(uri, test_result_fields)

    def get_statuses(self) -> JsonList:
        """Get test statuses information from TestRail.

        *Returns:* \n
            Statuses information in json format.
        """
        uri = 'get_statuses'
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS)
        return cast(JsonList, response)

    def update_case(self, case_id: Id, request_fields: Dict[str, Union[str, int, None]]) -> JsonDict:
        """Update an existing test case in TestRail.

        *Supported request fields:*\n
        | *Name*       | *Type*   | *Description*                                                          |
        | title        | string   | The title of the test case (required)                                  |
        | template_id  | int      | The ID of the template (field layout) (requires TestRail 5.2 or later) |
        | type_id      | int      | The ID of the case type                                                |
        | priority_id  | int      | The ID of the case priority                                            |
        | estimate     | timespan | The estimate, e.g. "30s" or "1m 45s"                                   |
        | milestone_id | int      | The ID of the milestone to link to the test case                       |
        | refs         | string   | A comma-separated list of references/requirements                      |
        | Custom fields are supported as well and must be submitted with their system name, prefixed with 'custom_' |

        *Args:* \n
            _case_id_ - ID of the test case;\n
            _request_fields_ - request fields dictionary.

        *Returns:* \n
            Case information in json format.

        *Example:*\n
        | Update Case | case_id=213 | request_fields={'title': name, 'type_id': 1, 'custom_case_description': description, 'refs': references} |
        """
        uri = 'update_case/{case_id}'.format(case_id=case_id)
        response = self._send_post(uri, request_fields)
        return cast(JsonDict, response)

    def get_status_id_by_status_label(self, status_label: str) -> int:
        """Get test status id by status label.

        *Args:* \n
            _status_label_ - status label of the tests.

        *Returns:* \n
            Test status ID.
        """
        statuses_info = self.get_statuses()
        for status in statuses_info:
            if status['label'].lower() == status_label.lower():
                return status['id']
        raise Exception(u"There is no status with label \'{}\' in TestRail".format(status_label))

    def get_test_status_id_by_case_id(self, run_id: Id, case_id: Id) -> Optional[int]:
        """Get test last status id by case id.
        If there is no last test result returns None.

        *Args:* \n
            _run_id_ - ID of the test run;\n
            _case_id_ - ID of the test case.

        *Returns:* \n
            Test status ID.
        """
        last_case_result = self.get_results_for_case(run_id=run_id, case_id=case_id, limit=1)
        return last_case_result[0]['status_id'] if last_case_result else None

    def get_project(self, project_id: Id) -> JsonDict:
        """Get project info by project id.

        *Args:* \n
            _project_id_ - ID of the project.

        *Returns:* \n
            Request result in json format.
        """
        uri = 'get_project/{project_id}'.format(project_id=project_id)
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS)
        return cast(JsonDict, response)

    def get_suite(self, suite_id: Id) -> JsonDict:
        """Get suite info by suite id.

        *Args:* \n
            _suite_id_ - ID of the test suite.

        *Returns:* \n
            Request result in json format.
        """
        uri = 'get_suite/{suite_id}'.format(suite_id=suite_id)
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS)
        return cast(JsonDict, response)

    def get_section(self, section_id: Id) -> JsonDict:
        """Get section info by section id.

        *Args:* \n
            _section_id_ - ID of the section.

        *Returns:* \n
            Request result in json format.
        """
        uri = 'get_section/{section_id}'.format(section_id=section_id)
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS)
        return cast(JsonDict, response)

    def add_section(self, project_id: Id, name: str, suite_id: Id = None, parent_id: Id = None,
                    description: str = None) -> JsonDict:
        """Creates a new section.

        *Args:* \n
            _project_id_ - ID of the project;\n
            _name_ - name of the section;\n
            _suite_id_ - ID of the test suite(ignored if the project is operating in single suite mode);\n
            _parent_id_ - ID of the parent section (to build section hierarchies);\n
            _description_ - description of the section.

        *Returns:* \n
            New section information.
        """
        uri = 'add_section/{project_id}'.format(project_id=project_id)
        data: Dict[str, Union[int, str]] = {'name': name}
        if suite_id is not None:
            data['suite_id'] = suite_id
        if parent_id is not None:
            data['parent_id'] = parent_id
        if description is not None:
            data['description'] = description

        response = self._send_post(uri=uri, data=data)
        return cast(JsonDict, response)

    def get_sections(self, project_id: Id, suite_id: Id) -> JsonList:
        """Returns existing sections.

        *Args:* \n
            _project_id_ - ID of the project;\n
            _suite_id_ - ID of the test suite.

        *Returns:* \n
            Information about section.
        """
        uri = 'get_sections/{project_id}&suite_id={suite_id}'.format(project_id=project_id, suite_id=suite_id)
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS)
        return cast(JsonList, response)

    def get_case(self, case_id: Id) -> JsonDict:
        """Get case info by case id.

        *Args:* \n
            _case_id_ - ID of the test case.

        *Returns:* \n
            Request result in json format.
        """
        uri = 'get_case/{case_id}'.format(case_id=case_id)
        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS)
        return cast(JsonDict, response)

    def get_cases(self, project_id: Id, suite_id: Id = None, section_id: Id = None) -> JsonList:
        """Returns a list of test cases for a test suite or specific section in a test suite.

        *Args:* \n
            _project_id_ - ID of the project;\n
            _suite_id_ - ID of the test suite (optional if the project is operating in single suite mode);\n
            _section_id_ - ID of the section (optional).

        *Returns:* \n
            Information about test cases in section.
        """
        uri = 'get_cases/{project_id}'.format(project_id=project_id)
        params = {'project_id': project_id}
        if suite_id is not None:
            params['suite_id'] = suite_id
        if section_id is not None:
            params['section_id'] = section_id

        response = self._send_get(uri=uri, headers=DEFAULT_TESTRAIL_HEADERS, params=params)
        return cast(JsonList, response)

    def add_case(self, section_id: Id, title: str, steps: List[Dict[str, str]], description: str, refs: str,
                 type_id: Id, priority_id: Id, **additional_data: Any) -> JsonDict:
        """Creates a new test case.

        *Args:* \n
            _section_id_ - ID of the section;\n
            _title_ - title of the test case;\n
            _steps_ - test steps;\n
            _description_ - test description;\n
            _refs_ - comma-separated list of references;\n
            _type_id_ - ID of the case type;\n
            _priority_id_ - ID of the case priority;\n
            _additional_data_ - additional parameters.

        *Returns:* \n
            Information about new test case.
        """
        uri = 'add_case/{section_id}'.format(section_id=section_id)
        data = {
            'title': title,
            'custom_case_description': description,
            'custom_steps_separated': steps,
            'refs': refs,
            'type_id': type_id,
            'priority_id': priority_id
        }
        for key in additional_data:
            data[key] = additional_data[key]

        response = self._send_post(uri=uri, data=data)
        return cast(JsonDict, response)
