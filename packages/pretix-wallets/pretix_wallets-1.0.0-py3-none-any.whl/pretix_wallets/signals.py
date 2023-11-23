from collections import OrderedDict
from django.dispatch import receiver
from django import forms
from django.utils.translation import gettext_lazy as _


from pretix.base.signals import register_ticket_outputs, register_global_settings
from pretix.base.ticketoutput import BaseTicketOutput




@receiver(register_ticket_outputs, dispatch_uid="output_wallet")
def register_ticket_output(sender, **kwargs):
    from .ticketoutput import WalletTicketOutput
    return WalletTicketOutput

@receiver(register_global_settings, dispatch_uid="wallet_settings")
def register_global_settings(sender, **kwargs):
    return OrderedDict(
        [
            (
                "wallet_base_url",
                forms.CharField(
                    label=_("Google Wallet Base URL"),
                    initial='https://walletobjects.googleapis.com/walletobjects/v1',
                    required=False,
                )
            ),
            (
                "wallet_batch_url",
                forms.CharField(
                    label=_("Google Wallet Batch URL"),
                    initial='https://walletobjects.googleapis.com/batch',
                    required=False,
                )
            ),
            (
                "wallet_class_url",
                forms.CharField(
                    label=_("Google Wallet Class URL"),
                    initial='https://walletobjects.googleapis.com/walletobjects/v1/eventTicketClass',
                    required=False,
                )
            ),
            (
                "wallet_object_url",
                forms.CharField(
                    label=_("Google Wallet Object URL"),
                    initial='https://walletobjects.googleapis.com/walletobjects/v1/eventTicketObject',
                    required=False,
                )
            ),
            (
                "wallet_key_file",
                forms.CharField(
                    label=_("Google Wallet Keyfile"),
                    required=False,
                    widget=forms.Textarea,
                    help_text=_(
                        "To obtain a keyfile, please follow these instructions"
                        "https://developers.google.com/wallet/tickets/events/web/prerequisites"
                    ),

                )
            )
        ]
    )