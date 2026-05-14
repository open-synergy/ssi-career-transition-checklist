# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

_AUTO_DONE_TRIGGER_FIELDS = ["is_done"]


class CareerTransitionChecklistItem(models.Model):
    """
    Checklist item for a career transition checklist document.

    Supports two modes:
    - Manual: user manually marks the item as done.
    - Automatic: system evaluates completion via Python code.
    """

    _name = "career_transition_checklist.item"
    _description = "Career Transition Checklist - Item"
    _order = "checklist_id, sequence, id"

    checklist_id = fields.Many2one(
        string="# Career Transition Checklist",
        comodel_name="career_transition_checklist",
        required=True,
        ondelete="cascade",
        help="Parent career transition checklist document.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Display order of the checklist item.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Name or description of the checklist item.",
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
        help="Python code for automatic evaluation. Must assign result = True/False.",
    )
    is_done = fields.Boolean(
        string="Done",
        default=False,
        help="For manual items: tick when the item is completed.",
    )
    note = fields.Text(
        string="Note",
        help="Additional notes or remarks for this checklist item.",
    )

    @api.depends(
        "is_done",
        "checklist_method",
        "python_code",
        "checklist_id",
    )
    def _compute_status_ok(self):
        for record in self:
            if record.checklist_method == "manual":
                record.status_ok = record.is_done
            else:
                record.status_ok = record._evaluate_python_code()

    status_ok = fields.Boolean(
        string="Status OK",
        compute="_compute_status_ok",
        store=False,
        help="Whether this checklist item is completed.",
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self.checklist_id,
        }

    def _evaluate_python_code(self):
        self.ensure_one()
        if not self.python_code:
            return False
        localdict = self._get_localdict()
        try:
            safe_eval(self.python_code, localdict, mode="exec", nocopy=True)
            return bool(localdict.get("result", False))
        except Exception:
            return False

    def write(self, vals):
        res = super().write(vals)
        if any(f in vals for f in _AUTO_DONE_TRIGGER_FIELDS):
            self._check_and_auto_done_parent()
        return res

    def _check_and_auto_done_parent(self):
        for record in self:
            checklist = record.checklist_id
            if checklist.state == "open" and checklist.all_items_done:
                checklist.sudo().with_context(bypass_policy_check=True).action_done()
