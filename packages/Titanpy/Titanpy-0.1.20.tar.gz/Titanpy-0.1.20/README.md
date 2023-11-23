# Titanpy V0.1.19

Python class for interacting with all Servicetitan's api endpoints

Windows install:
py -m pip install --upgrade Titanpy

## Purpose

I created this library to catalog and create handlers for all ServiceTitan API endpoints. With handlers and defaults created, autogeneration of an entire database will be as simple as requesting from specific endpoint's defaults and generating an ETL schema creating data marts for Data Analysts to create dashboards from.

Titanpy Atlas will be the service to do this, by configuring simple parameters is will use SQLAlchemy, Pandas, and DBT to create an entire data warehouse from Servicetitan data so major common datasets between organizations can be created without the need of costly Data Engineers and professional development.

Titanpy was heavily inspired by [ServicePytan](https://github.com/elliotpalmer/servicepytan), which was the basis of the general implementation of Titanpy and Atlas.


## Tutorials

### Making a get request to Servicetitan APIs

```
from Titanpy import Titanpy

tp = Titanpy("path/to/credentials")
tp.Get(endpoint, query, id, category, url)
```

Above is the general usage of the Titanpy api library. You first create the Titanpy class object which contains all the general api call methods, such as connect and get. 

Then you must connect to your ServiceTitan api developer account by getting credentials. These credentials can be requests at the [ServiceTitan Developer Request Portal](https://developer.servicetitan.io/request-access/). The path to these credentials in json format must be entered as a string. The json must follow the following format:
```
{
    "CLIENT_ID": "{client id}",
    "CLIENT_SECRET": "{client secret}",
    "APP_ID": "{app id}",
    "APP_KEY": "{app key}",
    "TENANT_ID": "{tenant id}",
    "TIMEZONE": "{timezone}"
}
```
After you are succesfully connected, you can make a get request to any endpoint currently integrated into the library. You can find all endpoints at the bottom of this page. Following that, you must put in a query. If you do not enter a query, a default query will be provided. Next you may enter ID(s) and Categories(s) depending on the endpoint you are using. For documentation on how to use these endpoints, please visit [ServiceTitan Developer API Reference](https://developer.servicetitan.io/apis/). In addition to finding documentation on how to create your own queries, you can also find endpoints that have been yet to be integrated. You can skip the endpoint list and simply enter the url and query if you wish to do so.

And you're done! This simple three step process will return a request object from the requests library.

### Creating the Default Atlas Schema

Generally, all you have to do is run the following script with your own parameters per database and servicetitan tenant you want to have data for in your Atlas schema.

```
from Titanpy import Atlas

Atlas().Build({path to sql credentials}, {path to servicetitan credentials}, type = 'Default', start_date = {'yyyy-mm-dd' or none})
```

Servicetitan credentials should be in the following format:

```
{
    "CLIENT_ID": "{client id}",
    "CLIENT_SECRET": "{client secret}",
    "APP_ID": "{app id}",
    "APP_KEY": "{app key}",
    "TENANT_ID": "{tenant id}",
    "TIMEZONE": "{timezone}"
}
```

SQL Credentials should be in the following format:

```
{
    "host": "{host}",
    "port": "{port}",
    "dbname": "{database name}",
    "user": "{username}",
    "pass": "{password}",
    "db_type": "postgresql15",
    "schema": "atlas"
}
```

Currently, the only database type acceptable is postgresql v15. In addition, all schemas default to atlas schema. We plan to update this is the future to have more connectors.

### Adding get endpoints

First add an endpoint to an endpoint group. This is accomplished by either adding to an existing group or creating a new one. For example, I want to add an exports endpoint for activity-codes. First I would go to the Payroll endpoint group, pick whether I want to add an ID/category endpoint or a normal endpoint. Since the export endpoint does not require an ID, I would add it to the latter. The naming scheme goes as follow:

> {first part of url}-{second part of url}{/ if id, no / if not id}

For the example: 'export/activity-codes'
For an id endpoint from activity-codes: 'activity-codes/'

This was done this way because for more complicated endpoints, they must has specific url formats that can be generated in the handlers/endpoint tests section. However, simple endpoints such as export activity-codes can simply be the format they would be in the url. The slash is added for simple id endpoints because they can simply be in the format {endpoint}/{id}.

Next the endpoint must be added to the available endpoints group list, most of the endpoint groups are already added but if a new group is made feel free to add it. Endpoint group names can be found at [Servicetitan Developer Apis](https://developer.servicetitan.io/apis/) and are based entirely off servicetitan's naming scheme.

The last step before creating a handler/endpoint test is adding the general url if it hasn't already. Please use the following structure when adding to this dictionary:

> "{endpoint group name}_url{_tenant if tenant included}": f"{url(with tenant inserted in the f-string if needed)}",

For more guidance use context clues with the previous general urls.

Finally, you can add the handler/endpoint test.

This section is split up based on endpoint groups with comments designating each endpoint group. You will find most have a handler for id endpoints and standard groups, with id groups being split between simple first then complicated following. Most of these can be copy pasted and then have specific parts replaced based on the current endpoint you are trying to integrate. Please study the general formatting and follow according, they are mostly the same.

And you're done! You've added a get endpoint. Send a pull request to the main branch and it'll be added after a short review.

## Endpoint Groups
```
# --------- ENDPOINT GROUPS --------- #

# Accounting
accounting_endpoints = [
    'export/inventory-bills',
    'export/invoice-items',
    'export/invoices',
    'export/payments',
    'ap-credits',
    'ap-payments',
    'inventory-bills',
    'invoices',
    'journal-entries',
    'payments',
    'payment-terms',
    'tax-zones',
]
accounting_id_endpoints = [
    'journal-entries-details/',
    'journal-entries-summary/',
    'payment-types/',
]

# CRM
crm_endpoints = [
    'export/bookings',
    'export/customers',
    'export/customers/contacts',
    'export/leads',
    'export/locations',
    'export/locations/contacts',
    'booking-provider-tags',
    'bookings',
    'customers',
    'customers/contacts',
    'leads',
    'locations',
    'locations/contacts',
]
crm_id_endpoints = [
    'booking-provider-tags/',
    '/bookings',
    '/bookings/',
    '/bookings-contacts/',
    'bookings/',
    'bookings-contacts/',
    'customers/',
    'customers-contacts/',
    'customers-notes/',
    'leads/',
    'leads-notes/',
    'locations/',
    'locations-contacts/',
    'locations-notes/',
]

# Dispatch
dispatch_endpoints = [
    'export/appointment-assignments',
    'appointment_assignments',
    'non-job-appointments',
    'teams',
    'technician-shifts',
    'zones',
]
dispatch_id_endpoints = [
    'non-job-appointments/',
    'teams/',
    'technician-shifts/',
    'zones/',
]

# Installed Systems
installed_systems_endpoints = [
    'installed-equipment',
]
installed_systems_id_endpoints = [
    'installed-equipment/',
]

# Forms
forms_endpoints = [
    'forms',
    'submissions',
]

# Inventory
inventory_endpoints = [
    'export/purchase-orders',
    'adjustments',
    'purchase-orders',
    'purchase-order-markups',
    'purchase-order-types',
    'receipts',
    'returns',
    'transfers',
    'trucks',
    'vendors',
    'warehouses',
]
inventory_id_endpoints = [
    'purchase-orders/',
    'purchase-order-markups/',
    'vendors/',
]

# Job Booking
job_booking_endpoints = [
    'call-reasons',
]

# Job Planning and Management
job_planning_endpoints = [
    'export/appointments',
    'export/job-canceled-logs',
    'export/jobs',
    'export/projects',
    'appointments',
    'job-cancel-reasons',
    'job-hold-reasons',
    'jobs',
    'job-types',
    'projects',
    'project-statuses',
    'project-substatuses',
]
job_planning_id_endpoints = [
    'appointments/',
    'jobs-cancel-reasons//',
    'jobs/',
    'jobs-history/',
    'jobs-notes/',
    'job-types/',
    'projects/',
    'projects-notes/',
    'project-statuses/',
    'project-substatuses/',
]

# Marketing
marketing_endpoints = [
    'categories',
    'costs',
    'campaigns',
    'suppressions',
]
marketing_id_endpoints = [
    'categories/',
    'costs/',
    'campaigns/',
    'campaigns-costs/',
    'suppressions/',
]

# Marketing Reputation
marketing_reputation_endpoints = [
    'reviews',
]

# Memberships Endpoints
memberships_endpoints = [
    'export/invoice-templates',
    'export/membership-types',
    'export/memberships',
    'export/recurring-service-events',
    'export/recurring-service-types',
    'export/recurring-services',
    'memberships',
    'recurring-service-events',
    'recurring-services',
    'membership-types',
    'recurring-service-types',

]
memberships_id_endpoints = [
    'memberships/',
    'memberships-status-changes/',
    'invoice-templates/',
    'invoice-templates//',
    'recurring-services/',
    'membership-types/',
    'membership-types-discounts/',
    'membership-types-duration-billing-items/',
    'membership-types-recurring-service-items/',
    'recurring-service-types/',
]

# Payroll
payroll_endpoints = [
    'export/activity-codes',
    'export/gross-pay-items',
    'export/jobs/splits',
    'export/jobs/timesheets',
    'export/payroll-adjustments',
    'export/timesheet-codes',
    'activity-codes',
    'gross-pay-items',
    'jobs/splits',
    'locations/rates',
    'payroll-adjustments',
    'payrolls',
    'timesheet-codes',
    'jobs/timesheets',
    'non-job-timesheets',
]
payroll_id_endpoints = [
    'activity-codes/',
    'jobs-splits/',
    'payroll-adjustments/',
    'employees-payrolls/',
    'technicians-payrolls/',
    'timesheet-codes/',
    'jobs-timesheets/',
]

# Pricebook
pricebook_endpoints = [
    'categories',
    'discounts-and-fees',
    'equipment',
    'images',
    'materials',
    'materialsmarkup',
    'services',
]
pricebook_id_endpoints = [
    'categories/',
    'discounts-and-fees/',
    'equipment/',
    'materials/',
    'materialsmarkup/',
    'services/',
]

# Reporting
reporting_endpoints = [
    'report-categories',
]
reporting_id_endpoints = [
    'dynamic-value-sets/',
    '/reports',
    '/reports/',
]

# Sales/Estimates
estimates_endpoints = [
    'estimates/export',
    'estimates',
    'estimates/items',
]
estimates_id_endpoints = [
    'estimates/',
]

# Service Agreements
service_agreements_endpoints = [
    'export/service-agreements',
    'service-agreements',
]
service_agreements_id_endpoints = [
    'service-agreements/',
]

# Settings
settings_endpoints = [
    'export/business-units',
    'export/employees',
    'export/tag-types',
    'export/technicians',
    'business_units',
    'employees',
    'tag-types',
    'technicians',
    'user-roles',
]
settings_id_endpoints = [
    'business_units/',
    'employees/',
    'technicians/',
]

# Task Management
task_management_endpoints = [
    'data',
]

# Telecom
telecom_endpoints = [
    'export/calls',
]
telecom_v3_endpoints = [
    'calls',
]
telecom_id_endpoints = [
    'calls/',
    'calls-recording/',
    'calls-voicemail/',
]
```