# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from flask_nemo.query.resolve import Resolver, HTTPRetriever
from flask_nemo.query.interface import SimpleQuery
from capitains_nautilus.flask_ext import FlaskNautilus
from pkg_resources import resource_filename
from MyCapytain.common.reference import URN
from aperire_ui import AperireUI
from nemo_arethusa_plugin import Arethusa
     
app = Flask("Nautilus")
nautilus = FlaskNautilus(
    app=app,
    prefix="/api/cts",
    name="nautilus",
    resources=["."]
)


def lesson_chunker(version, getValidReff):
    reffs = [urn.split(":")[-1] for urn in getValidReff(level=2)]
    # Satura scheme contains three level (book, poem, lines) but only the Satura number is sequential
    # So as human readable, we give only the second member of the reference body
    return [(reff, "Text {1}".format(*tuple(reff.split(".")))) for reff in reffs]

# Setup the Query Interface
# this is temporary to allow for demo of functionality 
# should eventually call to a collections api
query = SimpleQuery(
    [
        ("urn:cts:aperire:delver.init.opp-lat1:2.1","http://sosol.perseids.org/sosol/dmm_api/item/TreebankCite/35716","http://data.perseus.org/rdfvocab/treebank"),
        ("urn:cts:aperire:delver.init.opp-lat1:3.1","http://sosol.perseids.org/sosol/dmm_api/item/TreebankCite/36035","http://data.perseus.org/rdfvocab/treebank"),
        ("urn:cts:aperire:delver.init.opp-lat1:3.2","http://sosol.perseids.org/sosol/dmm_api/item/TreebankCite/36036","http://data.perseus.org/rdfvocab/treebank"),
        ("urn:cts:aperire:delver.init.opp-lat1:4.1","http://sosol.perseids.org/sosol/dmm_api/item/TreebankCite/36120","http://data.perseus.org/rdfvocab/treebank")
    ],
    resolver=Resolver(HTTPRetriever())
)

# We set up Nemo
nemo = Nemo(
    app=app,
    name="nemo",
    base_url="",
    api_url="/api/cts",
    retriever=nautilus.retriever,
	plugins=[Arethusa(queryinterface=query), AperireUI()],
    chunker={
        "default": lesson_chunker
    },
    transform={
        "default": resource_filename("aperire_ui","data/assets/static/xslt/epidocShort.xsl")
    }
)
query.process(nemo)

if __name__ == "__main__":
    app.DEBUG = True
    app.run()