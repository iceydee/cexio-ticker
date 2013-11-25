import sublime
import sublime_plugin

try:
  import urllib
  from urllib.request import urlopen
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse
  from urllib import urlopen

import json
import re

class cexioticker(sublime_plugin.EventListener):

  def update_status(self):
    """
      Updates the view's status bar with the current exchange rate
    """

    self.view.set_status('ghs', "GHS/BTC %.2f" % self.get_ticker())

  def get_ticker(self):
    """
      Makes API call to cex.io to retrieve latest GHS rate.

      Returns a the current exchange rate of 1 GHS in XBT.
    """

    settings = sublime.load_settings('cexio-ticker.sublime-settings')

    url = 'https://cex.io/api/ticker/GHS/BTC'
    req = urllib.request.Request(url, headers={'User-Agent': 'sublime-text-ticker'})
    resp = json.loads(urlopen(req).read().decode('utf-8'))

    ghs_in_btc = float(resp['last'])

    return ghs_in_btc

  def on_load(self, view):
    self.view = view

    settings = sublime.load_settings(__name__ + '.sublime-settings')
    sublime.set_timeout(self.update_status, 10)

  def on_post_save(self, view):
    self.view = view

    sublime.set_timeout(self.update_status, 10)
