# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Author Management'

    first_name = fields.Char('First Name', size=20, required=True)
    last_name = fields.Char('Last Name', size=40, required=True)
    birthdate = fields.Date('Birthdate')
    deathdate = fields.Date('Deathdate')

    country_id = fields.Many2one('res.country', 'Citizenship', required=True)

    item_ids = fields.Many2many('library.item', 'library_author_item_rel', 'author_id', 'item_id', 'Authors', readonly=True)

    @api.constrains('death_date')
    def _check_death_date(self):
        for author in self:
            if author.birthdate != False and author.deathdate != False:
                if author.birthdate > author.deathdate:
                    raise ValidationError(_('Birthdate must be earlier than Deathdate.'))
                
    
class LibraryItem(models.Model):
    _name = 'library.item'
    _description = 'Exemplar Management'

    reference = fields.Char('Reference', size=10, required=True)
    title = fields.Char('Title', size=120, required=True)
    description = fields.Html('Description')
    date_in = fields.Date('Date In')
    date_out = fields.Date('Date out')
    reason = fields.Char('Reason', size=200)

    author_ids = fields.Many2many('library.author', 'library_author_item_rel', 'item_id', 'author_id', 'Authors', ondelete='restrict', readonly=True)

    category_id = fields.Many2one('library.item.category', 'Category', required=True)

    @api.depends('reference', 'title')
    def _compute_display_name(self):
        for item in self:
            if item.reference != False and item.title != False: # Els dos camps són required, però ho mirem igualment
                # display_name és un camp d'Odoo directament
                item.display_name = item.title + " - " + item.reference
            else:
                item.display_name = "New Item"

    @api.constrains('date_out')
    def _check_date_out(self):
        for item in self:
            if item.date_out == False:
                item.reason = ""



class LibraryItemCategory(models.Model):
    _name = 'library.item.category'
    _description = 'Item Category Management'

    name = fields.Char('Name', size=45, required=True)
    isbn = fields.Boolean('ISBN?', default=True) # Per a que com a mínim hi hagi un de premut
    issn = fields.Boolean('ISSN?')

    child_ids = fields.One2many('library.item.category', 'parent_id', 'Child Category', readonly=True)

    parent_id = fields.Many2one('library.item.category', 'Parent Category', ondelete='restrict')

    item_ids = fields.One2many('library.item', 'category_id', 'ItemCategory', readonly=True)

    @api.constrains('isbn', 'issn')
    def _check_isbn_issn(self):
        for category in self:
            if category.isbn == True and category.issn == True:
                raise ValidationError(_('A category cannot support ISBN and ISSN both activated.'))
            if category.isbn != False and category.issn != False:
                raise ValidationError(_('A category cannot support ISBN and ISSN both deactivated.'))