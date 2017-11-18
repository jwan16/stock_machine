# -*- coding:utf-8 -*-

""" custom context processors """
from model.models import Model
from backtest.models import Backtest
from django.contrib.auth.decorators import login_required

def active_shows(request):
    """ context processors returning currently active shows """
    if request.user.is_authenticated:
        return {
            'models': Model.objects.filter(owner = request.user),
            'backtests': Backtest.objects.filter(owner = request.user),
            'request': request}
    else:
        return {'models': [], 'request': request}