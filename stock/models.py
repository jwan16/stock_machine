from django.db import models
import django_tables2 as tables
from django.contrib.auth.models import User

class Company(models.Model):
    stock_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    board_lot = models.IntegerField(null=True, blank= True)
    industry = models.CharField(max_length=50, null=True, blank=True)
    profile = models.CharField(max_length=50, null=True, blank=True)
    listing_date = models.DateField(null=True, blank=True)
    auth_capital = models.IntegerField(null=True, blank=True)
    issued_capital = models.IntegerField(null=True, blank=True)
    sector = models.CharField(max_length=50, null=True, blank=True)
    par_currency = models.CharField(max_length=50, null=True, blank=True)
    par_value = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.stock_id)

class Ratio(models.Model):
    stock_id = models.ForeignKey(Company)
    date = models.DateField()
    current_ratio = models.FloatField(blank=True, null=True)
    div_payout = models.FloatField(blank=True, null=True)
    fiscal_year_high = models.FloatField(blank=True, null=True)
    fiscal_year_low = models.FloatField(blank=True, null=True)
    fiscal_year_per_high = models.FloatField(blank=True, null=True)
    fiscal_year_per_low = models.FloatField(blank=True, null=True)
    fiscal_year_yield_high = models.FloatField(blank=True, null=True)
    fiscal_year_yield_low = models.FloatField(blank=True, null=True)
    inventory_turnover = models.FloatField(blank=True, null=True)
    longterm_de = models.FloatField(blank=True, null=True)
    npm = models.FloatField(blank=True, null=True)
    opm = models.FloatField(blank=True, null=True)
    pretax_pm = models.FloatField(blank=True, null=True)
    quick_ratio = models.FloatField(blank=True, null=True)
    roce = models.FloatField(blank=True, null=True)
    roe = models.FloatField(blank=True, null=True)
    rota = models.FloatField(blank=True, null=True)
    total_de_employed = models.FloatField(blank=True, null=True)
    total_de = models.FloatField(blank=True, null=True)
    def __str__(self):
        return str(self.stock_id) + ' on ' +  str(self.date)

class LatestPriceInfo(models.Model):
    stock_id = models.OneToOneField(Company, primary_key=True)

class Historical_Price(models.Model):
    stock_id = models.ForeignKey(Company)
    date = models.DateField()
    open = models.FloatField(null=True, blank= True)
    low = models.FloatField(null=True, blank= True)
    close = models.FloatField(null=True, blank= True)
    adj_close = models.FloatField(null=True, blank= True)
    volume = models.FloatField(null=True, blank= True)
    def __str__(self):
        return str(self.stock_id)

