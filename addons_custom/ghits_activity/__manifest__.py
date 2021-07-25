#-*- coding: utf-8 -*-

{
	"name": "Activities",
	"version": "1.0", 
	"depends": [
		'base','mail'
	],
	"author": "Abdelrazek Badr",
	"category": "Utility",
	"website": "",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "0",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "This is the Activities to review from one place ",
	"description": """

Information
======================================================================

* created menus
* created objects
* created views
* logics

""",
	"data": [
		"security/groups.xml",
		"security/ir.model.access.csv",
	    "view/mail_activity.xml",
		"report/mail_activity.xml",

		"view/menu.xml",
	],
	"installable": True,
	"auto_install": False,
	"application": True,
}