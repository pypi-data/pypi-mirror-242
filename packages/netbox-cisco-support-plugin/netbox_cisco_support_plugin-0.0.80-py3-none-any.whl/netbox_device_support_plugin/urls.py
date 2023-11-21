from django.urls import path
from . import views


app_name = "netbox_device_support_plugin"

urlpatterns = (
    # Cisco Device Support
    path(
        "device-support/",
        views.CiscoDeviceSupportListView.as_view(),
        name="ciscodevicesupport_list",
    ),
    path(
        "device-support/delete/",
        views.CiscoDeviceSupportBulkDeleteView.as_view(),
        name="ciscodevicesupport_bulk_delete",
    ),
    path(
        "device-support/<int:pk>/delete/",
        views.CiscoDeviceSupportDeleteView.as_view(),
        name="ciscodevicesupport_delete",
    ),
    # Cisco Device Type Support
    path(
        "device-type-support/",
        views.CiscoDeviceTypeSupportListView.as_view(),
        name="ciscodevicetypesupport_list",
    ),
    path(
        "device-type-support/delete/",
        views.CiscoDeviceTypeSupportBulkDeleteView.as_view(),
        name="ciscodevicetypesupport_bulk_delete",
    ),
    path(
        "device-type-support/<int:pk>/delete/",
        views.CiscoDeviceTypeSupportDeleteView.as_view(),
        name="ciscodevicetypesupport_delete",
    ),
    # Fortnet Support
    path(
        "fortinet-support/",
        views.FortinetSupportListView.as_view(),
        name="fortinetsupport_list",
    ),
    path(
        "fortinet-support/delete/",
        views.FortinetSupportBulkDeleteView.as_view(),
        name="fortinetsupport_bulk_delete",
    ),
    path(
        "fortinet-support/<int:pk>/delete/",
        views.FortinetSupportDeleteView.as_view(),
        name="fortinetsupport_delete",
    ),
)
