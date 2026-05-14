# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class CareerTransitionChecklist(models.Model):
    """
    Career transition checklist document.

    Tracks onboarding, offboarding, or other checklist tasks linked to an employee
    career transition. Supports both automatic (Python-evaluated) and manual checklist
    items. Transition from Open to Done requires all checklist items to be completed.
    """

    _name = "career_transition_checklist"
    _description = "Career Transition Checklist"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.employee_document",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    career_transition_id = fields.Many2one(
        string="Career Transition",
        comodel_name="employee_career_transition",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="The career transition document this checklist is associated with.",
    )
    checklist_item_ids = fields.One2many(
        string="Checklist Items",
        comodel_name="career_transition_checklist.item",
        inverse_name="checklist_id",
        states={"done": [("readonly", True)], "cancel": [("readonly", True)]},
        help="List of checklist items to be completed.",
    )

    @api.depends(
        "checklist_item_ids",
        "checklist_item_ids.status_ok",
    )
    def _compute_all_items_done(self):
        for record in self:
            items = record.checklist_item_ids
            if not items:
                record.all_items_done = True
            else:
                record.all_items_done = all(item.status_ok for item in items)

    all_items_done = fields.Boolean(
        string="All Items Done",
        compute="_compute_all_items_done",
        store=False,
        help="True when all checklist items are completed.",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.pre_done_check()
    def _check_all_items_done(self):
        self.ensure_one()
        if not self.all_items_done:
            raise UserError(
                _(
                    """Document: %(description)s
Context: Action done
Database ID: %(id)s
Problem: Not all checklist items are completed.
Solution: Complete all checklist items before marking as done."""
                )
                % {
                    "description": self._description.lower(),
                    "id": self.id,
                }
            )

    def action_load_checklist(self):
        for record in self.sudo():
            record._load_checklist()

    def _get_checklist_type_criteria(self, transition_type):
        return [
            "|",
            ("career_transition_type_ids", "=", False),
            ("career_transition_type_ids", "in", [transition_type.id]),
        ]

    def _prepare_checklist_item_vals(self, type_item):
        return {
            "checklist_id": self.id,
            "type_id": type_item.id,
            "name": type_item.name,
            "checklist_method": type_item.checklist_method,
            "python_code": type_item.python_code,
            "sequence": type_item.sequence or 5,
        }

    def _load_checklist(self):
        self.ensure_one()
        if not self.career_transition_id:
            return
        obj_type = self.env["career_transition_checklist_type"]
        transition_type = self.career_transition_id.type_id
        criteria = self._get_checklist_type_criteria(transition_type)
        types = obj_type.search(criteria)
        existing_type_item_ids = (
            self.checklist_item_ids.filtered(lambda i: i.type_id)
            .mapped("type_id")
            .ids
        )
        obj_item = self.env["career_transition_checklist.item"]
        for checklist_type in types:
            for type_item in checklist_type.checklist_item_ids:
                if type_item.id not in existing_type_item_ids:
                    obj_item.create(self._prepare_checklist_item_vals(type_item))

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
