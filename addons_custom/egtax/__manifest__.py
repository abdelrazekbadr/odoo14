#-*- coding: utf-8 -*-

{
	"name": "EG Tax",
	"version": "1.0", 
	"depends": [
		'base','account',
	],
	"author": "laplacesoftware",
	"category": 'Accounting/Accounting',
	"website": "https:www.laplacesoftware.com",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "OPL-1",
	"currency": "EGP",
	"summary": "Invoices & Tax integration with egyptian e-Invoicing ",
   'description': """
Invoicing & Tax integration 
====================
The specific and easy-to-use EG-Tax integration  in Odoo allows you to keep track of your invoice posting to egyptian e-invoice ,
.   """,
	"data": [
		"security/groups.xml",
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/res_config_settings_views.xml",
		 "view/account_move_tax.xml",
		 #"view/invoice.xml",
		 #"view/creditnote.xml",
		 #"view/bill.xml",
		 #"view/depitnote.xml",
		"view/error.xml",
		"report/account_move_tax.xml",
		"report/invoice.xml",
		"report/creditnote.xml",
		"report/bill.xml",
		"report/depitnote.xml",
		"report/error.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}