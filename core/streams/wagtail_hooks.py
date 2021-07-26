import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import ( InlineStyleElementHandler )
from wagtail.core import hooks

from django.templatetags.static import static
from django.utils.html import format_html


@hooks.register("register_rich_text_features")
def register_code_styling(features):
	# Step 1
	feature_name = "code"
	type_ = "CODE"
	tag = "code"

	# Step 2
	control = {
		"type": type_,
		"label": "</>",
		"description": "Code Style"
	}

	# Step 3
	features.register_editor_plugin(
		"draftail", feature_name, draftail_features.InlineStyleFeature(control)
	)

	# Setp 4 - Register this in the DB
	db_conversion = {
		"from_database_format": { tag: InlineStyleElementHandler(type_) },
		"to_database_format": { "style_map": {type_: {"element": tag}} },
	}

	# Step 5
	features.register_converter_rule("contentstate", feature_name, db_conversion)

	# Step 6 (Optional) - This will register this feature with all richtext editors by default
	features.default_features.append(feature_name)



@hooks.register("register_rich_text_features")
def register_centertext_feature(features):

	feature_name = "center"
	type_ = "CENTERTEXT"
	tag = "div"

	control = {
		"type": type_,
		"label": "C",
		"description": "Centered text",
		"style": {
			"display": "block",
			"text-align": "center",
		},
	}

	features.register_editor_plugin(
		"draftail", feature_name, draftail_features.InlineStyleFeature(control)
	)

	db_conversion = {
		"from_database_format": { tag: InlineStyleElementHandler(type_) },
		"to_database_format": { 
			"style_map": {
				type_: {
					"element": tag,
					"props": {
						"class": "d-block qualquierClase"
					}
				}
			} 
		},
	}

	features.register_converter_rule("contentstate", feature_name, db_conversion)

	features.default_features.append(feature_name)



@hooks.register("register_rich_text_features")
def register_righttext_feature(features):

	feature_name = "right"
	type_ = "RIGHTTEXT"
	tag = "div"

	control = {
		"type": type_,
		"label": "R",
		"description": "Pull the text into the Right",
		"style": {
			"display": "block",
			"text-align": "right",
		},
	}

	features.register_editor_plugin(
		"draftail", feature_name, draftail_features.InlineStyleFeature(control)
	)

	db_conversion = {
		"from_database_format": { tag: InlineStyleElementHandler(type_) },
		"to_database_format": { 
			"style_map": {
				type_: {
					"element": tag,
					"props": {
						"class": "d-block"
					}
				}
			} 
		},
	}

	features.register_converter_rule("contentstate", feature_name, db_conversion)

	features.default_features.append(feature_name)



@hooks.register("register_rich_text_features")
def register_lefttext_feature(features):

	feature_name = "left"
	type_ = "LEFTTEXT"
	tag = "div"

	control = {
		"type": type_,
		"label": "L",
		"description": "Pull the text into the Left",
		"style": {
			"display": "block",
			"text-align": "left",
		},
	}

	features.register_editor_plugin(
		"draftail", feature_name, draftail_features.InlineStyleFeature(control)
	)

	db_conversion = {
		"from_database_format": { tag: InlineStyleElementHandler(type_) },
		"to_database_format": { 
			"style_map": {
				type_: {
					"element": tag,
					"props": {
						"class": "d-block"
					}
				}
			} 
		},
	}

	features.register_converter_rule("contentstate", feature_name, db_conversion)

	features.default_features.append(feature_name)

'''
# Uncomment to allow custom css in your wagtail-admin
@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
	return format_html('<link rel="stylesheet" href="{}"/>', static("css/style.css"))

@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
	return format_html('<script src="{}"></script>', static("css/custom.js"))
'''