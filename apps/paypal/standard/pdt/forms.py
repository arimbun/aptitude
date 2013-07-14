#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.paypal.standard.forms import PayPalStandardBaseForm
from apps.paypal.standard.pdt.models import PayPalPDT


class PayPalPDTForm(PayPalStandardBaseForm):
    class Meta:
        model = PayPalPDT