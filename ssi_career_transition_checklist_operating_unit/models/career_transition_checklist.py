# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CareerTransitionChecklist(models.Model):  # pylint: disable=too-few-public-methods
    _name = "career_transition_checklist"
    _inherit = [
        "career_transition_checklist",
        "mixin.single_operating_unit",
    ]
