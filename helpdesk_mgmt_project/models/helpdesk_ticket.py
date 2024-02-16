from odoo import api, fields, models


class HelpdeskTicket(models.Model):

    _inherit = "helpdesk.ticket"

    project_id = fields.Many2one(string="Project", comodel_name="project.project")

    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
        compute="_compute_task_id",
        readonly=False,
        store=True,
    )

    # Override field
    company_id = fields.Many2one(
        default=lambda self: self.env["project.project"]
        .browse(self._context["default_project_id"])
        .company_id
        if self._context.get("default_project_id")
        else self.env.company
    )

    @api.depends("project_id")
    def _compute_task_id(self):
        for record in self:
            if record.task_id.project_id != record.project_id:
                record.task_id = False
