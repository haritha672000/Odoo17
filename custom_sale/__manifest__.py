{
    'name': "Custom Sales",
    'version': '17.0',
    'summary': "Custom Sales",
    'description': "custom sales",
    'category': 'Base',
    'depends': ['sale'],
    'data': [
        'security/sale_admin.xml',
        'views/sale_order_form.xml',
        'views/res_config_setting.xml',

    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}