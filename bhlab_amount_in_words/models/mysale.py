# -*- coding: utf-8 -*-

from num2words import num2words
from odoo import api, models,fields
from odoo.exceptions import UserError 
from odoo import exceptions
import math
import logging
_logger = logging.getLogger(__name__) 

class MyInvoice(models.Model):
	_inherit = "account.invoice"
	
	@api.one
	@api.depends('amount_total')
	def _compute_amount_words(self):
		self.num_word = trad(self.amount_total)
				
	num_word=fields.Char(string='Total en lettre:',compute='_compute_amount_words')
	

class MySale(models.Model):
	_inherit = "sale.order"	
	
	@api.one
	@api.depends('amount_total')
	def _compute_amount_words(self):
		self.num_word = trad(self.amount_total)
				
	num_word=fields.Char(string='Total en lettre:',compute='_compute_amount_words')
			
class MyPayment(models.Model):
	_inherit = "account.payment"
	
	@api.one
	@api.depends('amount')
	def _compute_amount_words(self):
		self.num_word = trad(self.amount_total)
				
	num_word=fields.Char(string='Total en lettre:',compute='_compute_amount_words')





# -*- encoding: utf-8 -*-

"""
Traduction d'un nombre en texte.
Réalisation : Michel Claveau    http://mclaveau.com

SVP, n'enlevez pas mon adresse/URL ; merci d avance

Usage : voir les exemples, à la fin du script.

Note : traduction franco-francaise, avec unites variables, orthographe gere, unites et centiemes.
"""


def tradd(num):
    global t1,t2
    ch=''
    if num==0 :
        ch=''
    elif num<20:
        ch=t1[num]
    elif num>=20:
        if (num>=70 and num<=79)or(num>=90):
            z=int(num/10)-1
        else:
            z=int(num/10)
        ch=t2[z]
        num=num-z*10
        if (num==1 or num==11) and z<8:
            ch=ch+' et'
        if num>0:
            ch=ch+' '+tradd(num)
        else:
            ch=ch+tradd(num)
    return ch


def tradn(num):
    global t1,t2
    ch=''
    flagcent=False
    if num>=1000000000:
        z=int(num/1000000000)
        ch=ch+tradn(z)+' milliard'
        if z>1:
            ch=ch+'s'
        num=num-z*1000000000
    if num>=1000000:
        z=int(num/1000000)
        ch=ch+tradn(z)+' million'
        if z>1:
            ch=ch+'s'
        num=num-z*1000000
    if num>=1000:
        if num>=100000:
            z=int(num/100000)
            if z>1:
                ch=ch+' '+tradd(z)
            ch=ch+' cent'
            flagcent=True
            num=num-z*100000
            if int(num/1000)==0 and z>1:
                ch=ch+'s'
        if num>=1000:
            z=int(num/1000)
            if (z==1 and flagcent) or z>1:
                ch=ch+' '+tradd(z)
            num=num-z*1000
        ch=ch+' mille'
    if num>=100:
        z=int(num/100)
        if z>1:
            ch=ch+' '+tradd(z)
        ch=ch+" cent"
        num=num-z*100
        if num==0 and z>1:
           ch=ch+'s'
    if num>0:
        ch=ch+" "+tradd(num)
    return ch


def trad(nb, unite="Dinar Algérien et", decim="centime"):
    global t1,t2
    nb=round(nb,2)
    t1=["","un","deux","trois","quatre","cinq","six","sept","huit","neuf","dix","onze","douze","treize","quatorze","quinze","seize","dix-sept","dix-huit","dix-neuf"]
    t2=["","dix","vingt","trente","quarante","cinquante","soixante","soixante-dix","quatre-vingt","quatre-vingt dix"]
    z1=int(nb)
    z3=(nb-z1)*100
    z2=int(round(z3,0))
    if z1==0:
        ch="zéro"
    else:
        ch=tradn(abs(z1))
    if z1>1 or z1<-1:
        if unite!='':
            ch=ch+" "+unite+'s'
    else:
        ch=ch+" "+unite
    if z2>0:
        ch=ch+tradn(z2)
        if z2>1 or z2<-1:
            if decim!='':
                ch=ch+" "+decim+'s'
        else:
            ch=ch+" "+decim
    if nb<0:
        ch="moins "+ch
    return ch


