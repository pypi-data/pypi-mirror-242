import json
import logging

import requests
import xmltodict

DEFAULT_TRUNCATION = 1000
DEFAULT_SCAN_OUTPUT_FORMAT = "json_extended"
DEFAULT_SCAN_MODE = "extended"
ATTRIBUTES_LIST = "ALL"  # Show attributes for each asset group along with
# the ID. Specify ALL or a comm-separated list of attribute
# names. Attribute names: ID, TITLE, OWNER_USER_NAME,
# OWNER_USER_ID, OWNER_UNIT_ID, NETWORK_IDS,
# LAST_UPDATE, IP_SET, APPLIANCE_LIST, DOMAIN_LIST,
# DNS_LIST, NETBIOS_LIST, EC2_ID_LIST, asset_group_IDS,
# ASSIGNED_USER_IDS, ASSIGNED_UNIT_IDS,
# BUSINESS_IMPACT, CVSS, COMMENTS.


_LOGGER = logging.getLogger(__name__)


class Client:
    def __init__(self, user, password, url):
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.session.headers.update(
            {
                "X-Requested-With": "Python.requests",
                "Content-Type": "text/xml",
                "Cache-Control": "no-cache",
            }
        )
        self.url = url

    def close(self):
        self.session.close()
        self.session = None

    def _handle_request(self, request):
        try:
            request.raise_for_status()
        except Exception:
            _LOGGER.error(f"Status: [{request.status_code}] {request.text}")
            raise

        _LOGGER.debug(f"Status: [{request.status_code}]")
        return request

    def _make_list_request(
        self,
        endpoint,
        key,
        force_list=None,
        title=None,
        truncation_limit=None,
        show_attributes=None,
    ):
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )
        request_url = self.url + endpoint
        params = {"action": "list"}
        if key != "SCHEDULE_SCAN":
            params["output_format"] = "xml"
        if truncation_limit:
            params["truncation_limit"] = truncation_limit
        if show_attributes:
            params["show_attributes"] = show_attributes
        if title:
            params["title"] = title
        req_data = []
        while request_url:
            _LOGGER.debug(f"Request URL: {request_url}")
            _LOGGER.debug(f"Request params: {params}")
            resp = self._handle_request(self.session.get(request_url, params=params))

            resp_json = xmltodict.parse(
                resp.text,
                attr_prefix="",
                cdata_key="text",
                comment_key="comment",
                force_list=force_list,
            )

            # handle special case of final key being different
            final_key = key
            if key == "SCHEDULE_SCAN":
                final_key = "SCAN"

            resp_json_data = resp_json[f"{key}_LIST_OUTPUT"]["RESPONSE"][f"{key}_LIST"][
                final_key
            ]
            _LOGGER.debug(f"Extending list of type {key} by {len(resp_json_data)}...")
            req_data.extend(resp_json_data)
            try:
                params = None
                request_url = resp_json[f"{key}_LIST_OUTPUT"]["RESPONSE"]["WARNING"][
                    "URL"
                ]
            except KeyError:
                request_url = None
        return req_data

    def list_asset_groups(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ATTRIBUTES_LIST,
        asset_group_title=None,
        force_list=["IP", "IP_RANGE", "DOMAIN_LIST", "DNS"],
        clean_data=True,
    ):
        _LOGGER.info("Requesting asset group data from Qualys...")
        _LOGGER.debug(
            f"Args: force_list={force_list} clean_data=[{clean_data}] "
            f"asset_group_title=[{asset_group_title}] "
            f"truncation_limit=[{truncation_limit}] show_attributes=[{show_attributes}]"
        )
        req_data = self._make_list_request(
            "/api/2.0/fo/asset/group/",
            "ASSET_GROUP",
            truncation_limit=truncation_limit,
            show_attributes=show_attributes,
            title=asset_group_title,
            force_list=force_list,
        )
        if clean_data:
            _LOGGER.info("Cleaning data...")
            for i in range(len(req_data)):
                # Instead of a string of CSV, seperate into a list of values
                if "HOST_IDS" in req_data[i]:
                    req_data[i]["HOST_IDS"] = req_data[i]["HOST_IDS"].split(", ")
                # Instead of a string of CSV, seperate into a list of values
                if "ASSIGNED_USER_IDS" in req_data[i]:
                    req_data[i]["ASSIGNED_USER_IDS"] = req_data[i][
                        "ASSIGNED_USER_IDS"
                    ].split(", ")
                # Ensure each domain list is a string, rather than an non-standard dict
                if "DOMAIN_LIST" in req_data[i]:
                    for j in range(len(req_data[i]["DOMAIN_LIST"])):
                        if isinstance(req_data[i]["DOMAIN_LIST"][j]["DOMAIN"], dict):
                            req_data[i]["DOMAIN_LIST"][j]["DOMAIN"] = json.dumps(
                                req_data[i]["DOMAIN_LIST"][j]["DOMAIN"]
                            )

        _LOGGER.info(f"Returning data for {len(req_data)} asset groups...")
        return req_data

    def list_hosts(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ATTRIBUTES_LIST,
        force_list=None,
        clean_data=True,
    ):
        _LOGGER.info("Requesting asset group data from Qualys...")
        _LOGGER.debug(
            f"Args: force_list={force_list} clean_data=[{clean_data}] "
            f"truncation_limit=[{truncation_limit}] show_attributes=[{show_attributes}]"
        )
        req_data = self._make_list_request(
            "/api/2.0/fo/asset/host/",
            "HOST",
            truncation_limit=truncation_limit,
            show_attributes=show_attributes,
            force_list=force_list,
        )

        if clean_data:
            _LOGGER.info("Cleaning data...")
            pass

        _LOGGER.info(f"Returning data for {len(req_data)} hosts...")
        return req_data

    def list_scan_schedules(self, force_list=["ASSET_GROUP_TITLE"], clean_data=True):
        _LOGGER.info("Requesting scan schedule data from Qualys...")
        _LOGGER.debug(f"Args: force_list=[{force_list}] clean_data=[{clean_data}]")
        scan_schedules = self._make_list_request(
            "/api/2.0/fo/schedule/scan/", "SCHEDULE_SCAN", force_list=force_list
        )

        _LOGGER.info(f"Returning data for {len(scan_schedules)} scan schedules...")
        return scan_schedules

    def list_scans(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ATTRIBUTES_LIST,
        force_list=None,
        clean_data=True,
    ):
        _LOGGER.info("Requesting scan data from Qualys...")
        _LOGGER.debug(
            f"Args: force_list={force_list} clean_data=[{clean_data}] "
            f"truncation_limit=[{truncation_limit}] show_attributes=[{show_attributes}]"
        )
        scan_data = self._make_list_request(
            "/api/2.0/fo/scan/",
            "SCAN",
            truncation_limit=truncation_limit,
            show_attributes=show_attributes,
            force_list=force_list,
        )
        _LOGGER.info(f"Returning data for {len(scan_data)} scan schedules...")
        return scan_data

    def _get_scanref_result(
        self, scan_ref, output_format=DEFAULT_SCAN_OUTPUT_FORMAT, mode=DEFAULT_SCAN_MODE
    ):
        request_url = self.url + "/api/2.0/fo/scan/"
        params = {
            "action": "fetch",
            "scan_ref": scan_ref,
            "output_format": output_format,
            "mode": mode,
        }
        req_data = self._handle_request(self.session.get(request_url, params=params))
        if output_format in ["json", "json_extended"]:
            return req_data.json()
        else:
            return req_data.text

    def get_scan_result(
        self,
        scan_title,
        output_format=DEFAULT_SCAN_OUTPUT_FORMAT,
        mode=DEFAULT_SCAN_MODE,
    ):
        _LOGGER.info(f"Getting scan result for scan [{scan_title}]...")
        _LOGGER.debug(
            f"Args: scan_title=[{scan_title}] "
            f"output_format=[{output_format}] mode=[{mode}]"
        )
        all_scans = self.list_scans()
        scan_ref = None
        for scan in all_scans:
            if scan["TITLE"] == scan_title:
                scan_ref = scan["REF"]
                break

        if not scan_ref:
            raise Exception(f"No scan found for title: [{scan_title}]")

        return self._get_scanref_result(
            scan_ref, output_format=output_format, mode=mode
        )

    # def get_report(self, report_title):
    # def get_kb(self)

    def search_hostassets(self, data, clean_data=True):
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )

        _LOGGER.info("Requesting host asset data from Qualys...")
        request_url = self.url + "/qps/rest/2.0/search/am/hostasset"
        _LOGGER.debug(f"Request url: {request_url}")
        req_data = self._handle_request(
            self.session.post(
                request_url, headers={"Accept": "application/json"}, data=data
            )
        )
        _LOGGER.debug(req_data.text)
        resp_json = req_data.json()["ServiceResponse"]["data"]
        host_assets = []
        for host_asset in resp_json:
            if clean_data:
                _LOGGER.info("Cleaning data...")
                pass
                # host_asset_data = json.dumps(host_asset["HostAsset"])
                # try:
                #     bq_values_of_death = [": {}", ": []"]
                #     for val in bq_values_of_death:
                #         if val in host_asset_data:
                #             host_asset_data = (
                #                 str(host_asset_data)
                #                 .replace(": {}", ": null")
                #                 .replace(": []", ": null")
                #             )
                # except Exception as e:
                #     logging.info(
                #         f"Replacing the BQ values of death failed with error: {e}"
                #     )
            host_assets.append(host_asset["HostAsset"])
        _LOGGER.info(f"Returning data for {len(host_assets)} host assets...")
        return host_assets
