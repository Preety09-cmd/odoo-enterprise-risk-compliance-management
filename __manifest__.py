{
    'name': 'Enterprise Risk and Compliance Management',
    'version': '1.0',
    'summary': 'Manage enterprise risks, categories, ownership, scoring, and workflow',
    'author': 'Preety Prasad',
    'category': 'Risk Management',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/risk_sequence.xml',
        'views/category_views.xml',
        'views/risk_views.xml',
        'views/risk_heatmap_views.xml',
        'views/menu_views.xml',
        'reports/risk_report.xml'
    ],
    'installable': True,
    'application': True,
}
