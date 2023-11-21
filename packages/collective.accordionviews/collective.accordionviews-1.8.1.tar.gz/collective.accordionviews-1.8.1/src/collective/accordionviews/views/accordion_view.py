# -*- coding: utf-8 -*-

# from collective.accordionviews import _
# from plone.app.contentlisting.interfaces import IContentListing
from bs4 import BeautifulSoup
from plone.app.layout.globals.interfaces import IViewView
from plone.memoize import ram
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import Interface


def _render_details_cachekey(method, self, brain):
    return (brain.getPath(), brain.modified)


def _html_fragment_cachekey(method, self, fragment, html):
    return (fragment, html,)


class AccordionView(BrowserView):

    def __call__(self):
        return self.index()

    @property
    def all_collapsed(self):
        return False

    @ram.cache(_render_details_cachekey)
    def _get_item_view_html(self, item):
        ctx = item.getObject()
        default_page = getattr(ctx.aq_explicit, "default_page", None)
        if default_page:
            ctx = ctx.restrictedTraverse(default_page)
        # without this a leadimage viewlet will not be rendered!
        self.request.set("URL", ctx.absolute_url())
        self.request.set("ACTUAL_URL", ctx.absolute_url())
        view_name = getattr(ctx.aq_explicit, "layout", ctx.getDefaultLayout())
        self.context_view = getMultiAdapter((ctx, self.request), name=view_name)
        alsoProvides(self.context_view, IViewView)
        return self.context_view()

    @ram.cache(_html_fragment_cachekey)
    def _get_fragment(self, fragment, raw_html):
        content_soup = BeautifulSoup(raw_html, "html.parser")
        content = content_soup.select_one(fragment)
        if not content:
            return ""
        return content.prettify()

    def render_above_content(self, item):
        html_str = self._get_item_view_html(item)
        return self._get_fragment("#viewlet-above-content-body", html_str)

    def render_content_core(self, item):
        html_str = self._get_item_view_html(item)
        return self._get_fragment("#content-core", html_str)

    def render_below_content(self, item):
        html_str = self._get_item_view_html(item)
        fragment_html = self._get_fragment("#viewlet-below-content-body", html_str)
        return fragment_html


class AccordionCollapsedView(AccordionView):
    """ a collapsed version of the accordion view """

    @property
    def all_collapsed(self):
        return True
