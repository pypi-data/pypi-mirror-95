# -*- coding: utf-8 -*-

from collective.z3cform.select2.widget.widget import MultiSelect2FieldWidget
from imio.restapi import _
from plone.autoform import directives as form
from zope import schema
from zope.interface import Interface


class ISettings(Interface):

    form.mode(client_id="display")
    client_id = schema.TextLine(
        title=_(u"The client unique identifier"),
        description=_(
            u"This information is configured in the instance configuration file"
        ),
        required=False,
    )

    form.mode(application_id="display")
    application_id = schema.TextLine(
        title=_(u"The application identifier"),
        description=_(
            u"This information is configured in the instance configuration file"
        ),
        required=False,
    )

    form.mode(application_url="display")
    application_url = schema.TextLine(
        title=_(u"The public url of this application"),
        description=_(
            u"This information is configured in the instance configuration file"
        ),
        required=False,
    )

    form.mode(ws_url="display")
    ws_url = schema.TextLine(
        title=_(u"The url of the Webservice instance"),
        description=_(
            u"This information is configured in the instance configuration file"
        ),
        required=False,
    )

    form.widget(application_links=MultiSelect2FieldWidget)
    application_links = schema.List(
        title=_(u"Application links"),
        description=_(
            u"List of application with who this application will communicate"
        ),
        value_type=schema.Choice(
            title=_(u"Application links"), vocabulary="imio.restapi.applications"
        ),
        required=False,
    )


class ISettingsForm(Interface):
    """Marker interface for the settings form"""
