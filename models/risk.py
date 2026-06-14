from odoo import models, fields, api


class RiskManagement(models.Model):
    _name = 'risk.management'
    _description = 'Risk Management'
    _rec_name = 'title'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    risk_id = fields.Char(
        string='Risk ID',
        readonly=True,
        copy=False,
        default='New'
    )

    title = fields.Char(
        string='Title',
        required=True
    )

    description = fields.Text(
        string='Description'
    )

    category_id = fields.Many2one(
        'risk.management.category',
        string='Category'
    )

    owner_id = fields.Many2one(
        'hr.employee',
        string='Risk Owner'
    )

    impact = fields.Integer(
        string='Impact',
        default=1
    )

    likelihood = fields.Integer(
        string='Likelihood',
        default=1
    )

    risk_score = fields.Integer(
        string='Risk Score',
        compute='_compute_risk_score',
        store=True
    )

    priority = fields.Selection(
        [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical')
        ],
        string='Priority',
        compute='_compute_priority',
        store=True
    )

    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('review', 'Under Review'),
            ('mitigated', 'Mitigated'),
            ('closed', 'Closed')
        ],
        string='Status',
        default='draft'
    )

    mitigation_plan = fields.Text(
        string='Mitigation Plan'
    )

    due_date = fields.Date(
        string='Due Date'
    )

    treatment_strategy = fields.Selection(
        [
            ('accept', 'Accept'),
            ('mitigate', 'Mitigate'),
            ('transfer', 'Transfer'),
            ('avoid', 'Avoid')
        ],
        string='Treatment Strategy'
    )

    residual_risk_score = fields.Integer(
        string='Residual Risk Score'
    )

    approval_status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        string='Approval Status',
        default='pending'
    )

    review_date = fields.Date(
        string='Review Date'
    )

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Evidence Attachments'
    )

    @api.model
    def create(self, vals):
        if vals.get('risk_id', 'New') == 'New':
           vals['risk_id'] = self.env['ir.sequence'].next_by_code(
              'risk.management'
           ) or 'New'

        return super().create(vals)

    @api.depends('impact', 'likelihood')
    def _compute_risk_score(self):
        for rec in self:
            rec.risk_score = rec.impact * rec.likelihood

    @api.depends('risk_score')
    def _compute_priority(self):
        for rec in self:
            if rec.risk_score <= 5:
                rec.priority = 'low'
            elif rec.risk_score <= 10:
                rec.priority = 'medium'
            elif rec.risk_score <= 15:
                rec.priority = 'high'
            else:
                rec.priority = 'critical'
    
    def action_print_risk_report(self):
        return self.env.ref(
            'risk_management.action_risk_summary_report'
        ).report_action(self)

    def action_open(self):
        self.status = 'open'

    def action_review(self):
        self.status = 'review'
        self._create_review_activity()

    def action_mitigate(self):
        self.status = 'mitigated'

    def action_close(self):
        self.status = 'closed'

    def action_reset_to_draft(self):
        self.status = 'draft'  
        
    def _create_review_activity(self):
        
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.activity_schedule(
            activity_type_id=activity_type.id,
            summary='Risk Review Required',
            note=f'Review risk: {self.title}',
            user_id=self.env.user.id,
            date_deadline=self.due_date
        )
    def action_approve(self):
        self.approval_status = 'approved'

    def action_reject(self):
        self.approval_status = 'rejected'    
