from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

@api.model
class ProductPlan(models.Model):
    _name = "product.plan"
    _description = "Product plan"
    
    name = fields.Char(
        "Name", readonly=True, select=True, copy=False, default="New"
    )
    revision = fields.Integer(
        string="Revision", default=1, tracking=True
    )    
    attachment = fields.Binary(
        string="Attachment",
        attachment=True,
        required=True,
        tracking=True,
    )
    store_fname = fields.Char(string="File Name")

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("eng.sequence") or "New"
            )
        result = super(ProductPlan, self).create(vals)
        return result

class Prodcut(models.Model):
    _inherit = ["product.template"]
    plan = fields.Many2one(
        "product.plan",
        string="Product plan",
        tracking=True,
    )
    product_plan = fields.Binary(
        string="Worksheet", related="plan.attachment", store=False
    )
