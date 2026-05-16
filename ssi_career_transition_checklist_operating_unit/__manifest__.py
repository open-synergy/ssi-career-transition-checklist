# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Career Transition Checklist + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_career_transition_checklist",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/career_transition_checklist.xml",
        "security/ir_rule/career_transition_checklist.xml",
        "views/career_transition_checklist_views.xml",
    ],
}
