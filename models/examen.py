# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

# _sql_constraints = [('name_uniq', 'unique(name)', 'Error!')]