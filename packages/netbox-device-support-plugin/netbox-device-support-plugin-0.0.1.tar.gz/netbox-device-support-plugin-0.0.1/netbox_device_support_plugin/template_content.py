from datetime import datetime

from django.shortcuts import get_object_or_404
from django.conf import settings
from extras.plugins import PluginTemplateExtension
from .models import CiscoDeviceTypeSupport, CiscoDeviceSupport, FortinetSupport


PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_device_support_plugin", dict())
TEMPLATE_EXTENSION_PLACEMENT = PLUGIN_SETTINGS.get("TEMPLATE_EXTENSION_PLACEMENT", "right")


#### Cisco Support ##########################################################################################


class CiscoDeviceTypeSupportInformation(PluginTemplateExtension):
    model = "dcim.devicetype"

    if TEMPLATE_EXTENSION_PLACEMENT == "left":

        def left_page(self):
            try:
                cisco_device_type_support = CiscoDeviceTypeSupport.objects.get(
                    device_type=self.context["object"]
                )
            except CiscoDeviceTypeSupport.DoesNotExist:
                print("No Cisco Device Type Support Entry found")
                cisco_device_type_support = None

            return self.render(
                "netbox_device_support_plugin/cisco_support_device_type.html",
                {"cisco_device_type_support": cisco_device_type_support},
            )

    def right_page(self):
        try:
            cisco_device_type_support = CiscoDeviceTypeSupport.objects.get(device_type=self.context["object"])
        except CiscoDeviceTypeSupport.DoesNotExist:
            print("No Cisco Device Type Support Entry found")
            cisco_device_type_support = None

        return self.render(
            "netbox_device_support_plugin/cisco_support_device_type.html",
            {"cisco_device_type_support": cisco_device_type_support},
        )


class CiscoDeviceSupportInformation(PluginTemplateExtension):
    model = "dcim.device"

    if TEMPLATE_EXTENSION_PLACEMENT == "left":

        def left_page(self):
            try:
                cisco_device_support = CiscoDeviceSupport.objects.get(device=self.context["object"])
            except CiscoDeviceSupport.DoesNotExist:
                print("No Cisco Device Support Entry found")
                cisco_device_support = None

            try:
                cisco_device_type_support = CiscoDeviceTypeSupport.objects.get(
                    device_type=self.context["object"].device_type
                )
            except CiscoDeviceTypeSupport.DoesNotExist:
                print("No Cisco Device Type Support Entry found")
                cisco_device_type_support = None

            return self.render(
                "netbox_device_support_plugin/cisco_support_device.html",
                {
                    "cisco_device_support": cisco_device_support,
                    "cisco_device_type_support": cisco_device_type_support,
                },
            )

    def right_page(self):
        try:
            cisco_device_support = CiscoDeviceSupport.objects.get(device=self.context["object"])
        except CiscoDeviceSupport.DoesNotExist:
            print("No Cisco Device Support Entry found")
            cisco_device_support = None

        try:
            cisco_device_type_support = CiscoDeviceTypeSupport.objects.get(
                device_type=self.context["object"].device_type
            )
        except CiscoDeviceTypeSupport.DoesNotExist:
            print("No Cisco Device Type Support Entry found")
            cisco_device_type_support = None

        return self.render(
            "netbox_device_support_plugin/cisco_support_device.html",
            {
                "cisco_device_support": cisco_device_support,
                "cisco_device_type_support": cisco_device_type_support,
            },
        )


#### Fortinet Support #######################################################################################


class FortinetSupportInformation(PluginTemplateExtension):
    model = "dcim.device"

    if TEMPLATE_EXTENSION_PLACEMENT == "left":

        def left_page(self):
            try:
                fortinet_support = FortinetSupport.objects.get(device=self.context["object"])
            except FortinetSupport.DoesNotExist:
                print("No Fortinet Device Support Entry found")
                fortinet_support = None

            return self.render(
                "fortinet/fortinet_support.html",
                {"fortinet_support": fortinet_support},
            )

    def right_page(self):
        try:
            fortinet_support = FortinetSupport.objects.get(device=self.context["object"])
        except FortinetSupport.DoesNotExist:
            print("No Fortinet Device Support Entry found")
            fortinet_support = None

        return self.render(
            "fortinet/fortinet_support.html",
            {"fortinet_support": fortinet_support},
        )


#### Template Extensions ####################################################################################

# Template extensions to be loaded when the plugin is loaded
template_extensions = [
    CiscoDeviceTypeSupportInformation,
    CiscoDeviceSupportInformation,
    FortinetSupportInformation,
]
