# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from urllib.parse import unquote

from contrast.agent.agent_lib import does_file_path_bypass_security
from contrast.utils.decorators import cached_property
from contrast.utils.stack_trace_utils import in_custom_code

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


CUSTOM_CODE_ACCESSING_SYSTEM_FILES_REP_CODE = 0
CUSTOM_CODE_CONFIG_KEY = "detect_custom_code_accessing_system_files"

COMMON_FILE_EXPLOITS_REP_CODE = 1
COMMON_FILE_EXPLOITS_KEY = "detect_common_file_exploits"

KNOWN_SECURITY_BYPASS_MARKERS = ["::$DATA", "::$Index", "" + "\x00"]
KNOWN_SYSTEM_FILES = [
    "/proc/self",
    "etc/passwd",
    "etc/shadow",
    "etc/hosts",
    "etc/groups",
    "etc/gshadow",
    "ntuser.dat",
    "/Windows/win.ini",
    "/windows/system32/",
    "/windows/repair/",
]


class PathTraversalSinkFeatures(object):
    def check_sink_features(self, attack_vector, attack):
        is_custom_code = self._check_custom_code_accessing_system_files(attack_vector)
        new_sample = is_custom_code or self._check_file_security_bypass(
            attack_vector, is_custom_code
        )

        if new_sample:
            if attack is None:
                attack = self.build_base_attack()

            attack.add_sample(new_sample)
            attack.set_response(self.response_from_mode(self.mode))
            self.log_rule_matched(None, attack.response)

        return attack

    def _check_custom_code_accessing_system_files(self, attack_vector):
        if (
            self._is_custom_code_access_sysfile_enabled
            and PathTraversalSinkFeatures._is_custom_code_accessing_file_system(
                attack_vector
            )
        ):
            logger.debug(
                "Found custom code trying to access system file: %s", attack_vector
            )
            return self._create_path_traversal_sample(
                attack_vector,
                CUSTOM_CODE_ACCESSING_SYSTEM_FILES_REP_CODE,
            )

        return None

    def _check_file_security_bypass(self, attack_vector, is_custom_code):
        file_bypass_security = does_file_path_bypass_security(
            attack_vector, is_custom_code
        )

        if (
            self._is_common_file_exploits_enabled
            and PathTraversalSinkFeatures._contains_known_attack_signatures(
                attack_vector
            )
            and file_bypass_security
        ):
            logger.debug(
                "Found attempt to bypass file security checks: %s", attack_vector
            )
            return self._create_path_traversal_sample(
                attack_vector,
                COMMON_FILE_EXPLOITS_REP_CODE,
            )

        return None

    def _create_path_traversal_sample(self, attack_vector, rep_code):
        sample = self.build_sample(None, attack_vector)
        sample.details["path"] = attack_vector
        sample.details["path_traversal_semantic"] = {}
        sample.details["path_traversal_semantic"]["path"] = attack_vector
        sample.details["path_traversal_semantic"]["findings"] = [rep_code]
        return sample

    @cached_property
    def _is_custom_code_access_sysfile_enabled(self):
        return self.settings.is_rep_feature_enabled_for_rule(
            self.name, CUSTOM_CODE_CONFIG_KEY
        )

    @cached_property
    def _is_common_file_exploits_enabled(self):
        return self.settings.is_rep_feature_enabled_for_rule(
            self.name, COMMON_FILE_EXPLOITS_KEY
        )

    @staticmethod
    def _is_custom_code_accessing_file_system(path):
        return PathTraversalSinkFeatures._is_system_file(path) and in_custom_code()

    @staticmethod
    def _contains_known_attack_signatures(path):
        unescaped = unquoted = unquote(path)

        try:
            unescaped = unquoted.encode("utf-8").decode("unicode-escape")
        except LookupError as e:
            logger.debug(
                f"Failed to unescape attack vector path {path} with the error {e}"
            )
            return False

        try:
            realpath = os.path.realpath(unescaped).lower().rstrip("/")
        except ValueError as e:
            return str(e) == "embedded null byte"
        except TypeError as e:
            return (
                "NUL" in str(e)
                or "null byte" in str(e)
                or str(e) == "embedded NUL character"
            )
        except Exception as e:
            return "null byte" in str(e).lower()

        return any(
            [
                bypass_markers.lower().rstrip("/") in realpath
                for bypass_markers in KNOWN_SECURITY_BYPASS_MARKERS
            ]
        )

    @staticmethod
    def _is_system_file(path):
        if not path:
            return False
        unquoted = unquote(path)
        realpath = os.path.realpath(unquoted).lower().rstrip("/")

        return any(
            [
                sys_file.lower().rstrip("/") in realpath
                for sys_file in KNOWN_SYSTEM_FILES
            ]
        )
