# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from capitains_nautilus.flask_ext import FlaskNautilus
from pkg_resources import resource_filename
from MyCapytain.common.reference import URN
     
app = Flask("Nautilus")
nautilus = FlaskNautilus(
    app=app,
    prefix="/api/cts",
    name="nautilus",
    resources=["."]
)

# We set up Nemo
nemo = Nemo(
    app=app,
    name="nemo",
    base_url="",
    api_url="/api/cts",
    retriever=nautilus.retriever,
    chunker={
        "default": level_grouper
    },
    transform={
        "default": resource_filename("perseus_nemo_ui","data/assets/static/xslt/epidocShort.xsl")
    }
)
nemo.init_app(app)
# We register its routes
nemo.register_routes()
# We register its filters
nemo.register_filters()