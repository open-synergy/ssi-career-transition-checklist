# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Career Transition Checklist",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_hr_career_transition",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_employee_document_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir_model_access/career_transition_checklist_type.xml",
        "security/ir_model_access/career_transition_checklist.xml",
        "security/ir_rule/career_transition_checklist.xml",
        "ir_sequence/career_transition_checklist.xml",
        "sequence_template/career_transition_checklist.xml",
        "approval_template/career_transition_checklist.xml",
        "policy_template/career_transition_checklist.xml",
        "data/ir_actions_server_data.xml",
        "views/career_transition_checklist_type_views.xml",
        "views/career_transition_checklist_views.xml",
    ],
    "demo": [],
}
