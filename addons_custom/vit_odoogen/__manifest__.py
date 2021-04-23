{
	"name": "StarUML Odoo Addon Generator for Odoo version 10-14",
	"version": "1.8", 
	"depends": [
		"base",
	],
	"author": "Akhmad D. Sembiring [vitraining.com]",
	"category": "Utility",
	'website': 'http://vitraining.com',
	'images': ['static/description/images/main_screenshot.png'],
	'price': '199',
	'license': 'OPL-1',
	'currency': 'USD',
	'summary': 'Install this to download the StarUML Odoo addon generator script',
	"description": """\

Version 1.6 (19 April 2020)
======================================================================
 * - bug fix state readonly on 'state' field
 * - auto add button confirm if state exists
 * - auto create action button methods if state exists
 * - auto add global variabel STATES if states exists 
 
Version 1.5 (9 April 2020)
======================================================================
 * - add _description on every model 
 * - add readonly=True states={"draft" : [("readonly",False)]}  if state field exists 
 * - add static/description folder 
 * - add static/description/icon.png 
 * - add static/js folder 
 * - add static/xml folder 
 
Versions 1.0
======================================================================
* Odoo addon generator
* UML Diagram Odoo addon generator
* rapid application development (RAD)
* starUml
* UML generator
* generate addon from UML diagram
* base addons
* addon creator

""",
	"data": [
		"wizard/download.xml",
		"top_menu.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}