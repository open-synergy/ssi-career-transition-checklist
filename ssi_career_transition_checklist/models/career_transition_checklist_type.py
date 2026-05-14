# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CareerTransitionChecklistType(models.Model):
    """
    Master data for career transition checklist types.

    Groups related checklist item templates. When a checklist document loads
    items, all item templates from matching types are instantiated.
    Types can be restricted to specific career transition types.

    Each type can have its own scheduled action (ir.cron) that periodically
    evaluates automatic checklist items for all open checklists.
    """

    _name = "career_transition_checklist_type"
    _inherit = ["mixin.master_data"]
    _description = "Career Transition Checklist Type"

    career_transition_type_ids = fields.Many2many(
        string="Applicable Transition Types",
        comodel_name="employee_career_transition_type",
        relation="rel_checklist_type_2_transition_type",
        column1="checklist_type_id",
        column2="transition_type_id",
        help="Restrict this checklist type to specific career transition types. "
        "Leave empty to make it applicable to all transition types.",
    )
    checklist_item_ids = fields.One2many(
        string="Checklist Items",
        comodel_name="career_transition_checklist_type.item",
        inverse_name="type_id",
        help="Template checklist items that will be loaded into checklist documents.",
    )
    cron_id = fields.Many2one(
        string="Scheduled Action",
        comodel_name="ir.cron",
        ondelete="set null",
        copy=False,
        readonly=True,
        help="Scheduled action that periodically evaluates automatic checklist items "
        "for all open checklists of this type.",
    )

    def _get_cron_model_criteria(self):
        return [("model", "=", self._name)]

    def _prepare_cron_vals(self, cron_model):
        cron_code = "env['%s'].browse(%d)._run_cron_evaluate()" % (self._name, self.id)
        return {
            "name": "Checklist Evaluate: %s" % self.name,
            "model_id": cron_model.id,
            "code": cron_code,
            "interval_number": 1,
            "interval_type": "days",
            "numbercall": -1,
            "active": True,
        }

    def _get_evaluate_item_criteria(self):
        return [
            ("type_id", "=", self.id),
            ("checklist_method", "=", "automatic"),
            ("checklist_id.state", "=", "open"),
            ("is_done", "=", False),
        ]

    def action_create_cron(self):
        self.ensure_one()
        cron_model = self.env["ir.model"].search(
            self._get_cron_model_criteria(), limit=1
        )
        cron = self.env["ir.cron"].sudo().create(self._prepare_cron_vals(cron_model))
        self.cron_id = cron.id

    def action_delete_cron(self):
        self.ensure_one()
        if self.cron_id:
            self.cron_id.sudo().unlink()

    def _run_cron_evaluate(self):
        self.ensure_one()
        Item = self.env["career_transition_checklist.item"]
        items = Item.search(self._get_evaluate_item_criteria())
        for item in items:
            if item._evaluate_python_code():
                item.write({"is_done": True})
