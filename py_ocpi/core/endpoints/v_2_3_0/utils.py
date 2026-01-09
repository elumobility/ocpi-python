"""Endpoint generators for OCPI 2.3.0."""

from py_ocpi.core.data_types import URL
from py_ocpi.core.endpoints.utils import BaseEndpointGenerator
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.modules.versions.v_2_3_0.schemas import (
    Endpoint,
    InterfaceRole,
    VersionNumber,
)


class BaseEndpointGenerator230(BaseEndpointGenerator):
    def __init__(self, role: RoleEnum) -> None:
        self.version = VersionNumber.v_2_3_0
        super().__init__(version=self.version, role=role)

    def generate_endpoint(
        self,
        module: ModuleID,
        interface_role: InterfaceRole,
        *args,
        **kwargs,
    ) -> Endpoint:
        """
        Return generated Endpoint schema.

        :param module: Module type.
        :param interface_role: Interface role of endpoint.
        """
        url = self.format_url(self.version, self.role, module)
        return Endpoint(
            identifier=module,
            role=interface_role,
            url=URL(url),
        )


class CPOEndpointGenerator230(BaseEndpointGenerator230):
    """Endpoint generator for CPO role using Endpoint schema v2.3.0."""

    def __init__(self):
        self.role = RoleEnum.cpo
        super().__init__(role=self.role)


class EMSPEndpointGenerator230(BaseEndpointGenerator230):
    """Endpoint generator for EMSP role using Endpoint schema v2.3.0."""

    def __init__(self):
        self.role = RoleEnum.emsp
        super().__init__(role=self.role)


cpo_generator = CPOEndpointGenerator230()
emsp_generator = EMSPEndpointGenerator230()
