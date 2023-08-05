import copy
import urllib.parse
import re
import unidecode

import flask
import jinja2.exceptions

from . import navigation

app = flask.Flask(__name__, template_folder="templates")

def main():
    app.run(debug=True)

# favicon redirection - need when serving card images directly
@app.route("/favicon.ico")
def favicon():
    return flask.redirect(flask.url_for("static", filename="img/favicon.ico"))

# Defining Errors
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("404.html"), 404

# Default route
@app.route("/")
@app.route("/<path:page>")
@app.route("/fr/<path:page>")
def index(page=None):
	redirect = False
	if not page:
		page = "index.html"
		redirect = True
	if redirect:
		return flask.redirect(page, 301)

	return flask.render_template(page)

# Use of a navigation helper
def _url(page, _anchor=None, **params):
    url = page.url
    if params:
        url += "?" + urllib.parse.urlencode(params)
    if _anchor:
        url += "#" + _anchor
    return url


def _link(page, name=None, _anchor=None, _class=None, **params):
    if not page or not page.url:
        return ""
    name = name or page.name
    url = _url(page, _anchor, **params)
    if _class:
        _class = f"class={_class} "
    else:
        _class = ""
    return flask.Markup(f'<a {_class}href="{url}">{name}</a>')


@app.context_processor
def linker():
    path = flask.request.path
    if path[-11:] == "/index.html":
        path = path[:-11]
    if path[-5:] == ".html":
        path = path[:-5]
    if path[-1:] == "/":
        path = path[:-1]

    def link(page, name=None, _anchor=None, **params):
        return _link(
            navigation.HELPER.get(page, {}).get("self"),
            name=name,
            _anchor=_anchor,
            **params,
        )

    def top():
        return _link(navigation.HELPER.get(path, {}).get("top"))

    def next():
        return _link(navigation.HELPER.get(path, {}).get("next"), _class="next")

    def prev():
        return _link(navigation.HELPER.get(path, {}).get("prev"), _class="prev")

    def external(url, name):
        return flask.Markup(f'<a target="_blank" href="{url}">{name}</a>')

    return dict(
        link=link,
        top=top,
        next=next,
        prev=prev,
        external=external,
    )
