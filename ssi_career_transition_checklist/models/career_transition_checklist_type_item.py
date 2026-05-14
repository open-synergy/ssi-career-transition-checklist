# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CareerTransitionChecklistTypeItem(models.Model):
    """
    Template checklist item belonging to a career transition checklist type.

    Each type can contain multiple item templates. When a checklist document
    loads items from a type, these templates are instantiated into actual
    checklist items on the document.
    """

    _name = "career_transition_checklist_type.item"
    _description = "Career Transition Checklist Type - Item"
    _order = "type_id, sequence, id"

    _DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: career_transition_checklist record.
#  - result: set to True if the check passes, False otherwise.
result = False"""

    type_id = fields.Many2one(
        string="# Checklist Type",
        comodel_name="career_transition_checklist_type",
        required=True,
        ondelete="cascade",
        help="Parent checklist type that owns this template item.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Display order of this template item.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Name or description of this checklist item template.",
    )
    checklist_method = fields.Selection(
        string="Method",
        selection=[
            ("manual", "Manual"),
            ("automatic", "Automatic"),
        ],
        required=True,
        default="manual",
        help="Manual: user checks this item. Automatic: evaluated via Python code.",
    )
    python_code = fields.Text(
        string="Python Code",
        default=_DEFAULT_PYTHON_CODE,
        help="Python code for automatic evaluation. Must assign result = True/False.",
    )
