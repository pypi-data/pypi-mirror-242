# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    type_id = fields.Many2one(
        comodel_name="mrp_production_type",
        string="Type",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    date_backdating = fields.Datetime(
        string="Actual Movement Date",
    )

    @api.constrains("date_backdating")
    def _check_date_backdating(self):
        now = fields.Datetime.now()
        for move in self:
            if move.date_backdating and move.date_backdating > now:
                raise UserError(
                    _("You can not process an actual " "movement date in the future.")
                )

    def button_mark_done(self):
        for rec in self:
            rec.move_finished_ids.write(
                {
                    "date_backdating": rec.date_backdating,
                }
            )
        return super(MrpProduction, self).button_mark_done()
