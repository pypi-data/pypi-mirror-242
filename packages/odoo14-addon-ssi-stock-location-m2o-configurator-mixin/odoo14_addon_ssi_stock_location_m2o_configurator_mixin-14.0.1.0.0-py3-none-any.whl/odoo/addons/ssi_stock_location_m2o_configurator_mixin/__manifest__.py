# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "stock.location Many2one Configurator Mixin",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["stock", "ssi_decorator"],
    "data": [
        "templates/stock_location_m2_configurator_templates.xml",
        "templates/inbound_stock_location_m2_configurator_templates.xml",
        "templates/outbound_stock_location_m2_configurator_templates.xml",
    ],
}
