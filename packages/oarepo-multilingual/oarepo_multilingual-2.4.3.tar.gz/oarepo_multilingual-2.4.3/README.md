OARepo multilingual data model
==============================

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Multilingual string data model for OARepo.

Instalation
----------
```bash
    pip install oarepo-multilingual
```
Usage
----------
The library provides multilingual type for json schema with marshmallow validation and deserialization and elastic search mapping.
Multilingual is type which allows you to add multilingual strings in your json schema in format ``"en":"something, 
"en-us":"something else"`` or default value ``"_" : "default value"``

JSON Schema
----------
Add this package to your dependencies and use it via ``$ref`` in json schema as ``"[server]/schemas/multilingual-v2.0.0.json#/definitions/multilingual"``.

### Usage example
```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "title": {
            "$ref": "https://localhost:5000/schemas/multilingual-v2.0.0.json#/definitions/multilingual"
      }
  }
}
```
```json
{
  "type": "object",
  "properties": {
    "title": {
            "en": "something",
            "en-us": "something else"
      }
  }
}
```
Marshmallow
-----------
For data validation and deserialization.

If marshmallow validation is performed within application context, languages are validated against SUPPORTED_LANGUAGES config.
If the validation is performed outside app context, the keys are not checked against a list of languages
but a generic validation is performed - keys must be in ISO 639-1 or language-region format from RFC 5646.

### Usage example
```python
    class MD(marshmallow.Schema):
         title = MultilingualStringSchemaV2()

    data = {
        'title':
            {
            "en": "something",
            "en-us": "something else",
            }
        }

    MD().load(data)
```
Supported languages validation
------------------------------
You can specified supported languages in your application configuration in ``SUPPORTED_LANGUAGES`` . Then only these
languages are allowed as multilingual string. 
You must specified your languages in format ``"en"`` or ``"en-us"``.
### Usage example
```python
app.config.update(SUPPORTED_LANGUAGES = ["cs", "en"])
```
Elastic search mapping
----------------------
Define type of your multilingual string as ``multilingual``
Add to your configuration definition of `ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE` which will be used as default mapping template for supported languages.
### Default template example
```python
ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE={
            "type": "text",
            "fields": {
                "keywords": {
                    "type": "keyword"
                }
            }
        }
```
You can also specified different templates for specific languages with `ELASTICSEARCH_LANGUAGE_TEMPLATES`. Use `#` and `id` for adding more 
templates for one specific language
### Language templates example
```python
ELASTICSEARCH_LANGUAGE_TEMPLATES={
        "cs": {
            "type": "text",
            "fields": {
                "keywords": {
                    "type": "keyword"
                }
            }
        },
        "cs#plain": {
            "type": "text",
        },
        "en": {
            "type": "text",
            "fields": {
                "keywords": {
                    "type": "keyword"
                }
            }
        }
    }
```
### Usage example
```json
{
  "mappings": {
    "properties": {
    "title":
      {"type": "multilingual"}
    }
  }
}
```
### Usage example with context
```json
{
  "mappings": {
    "properties": {
    "title":
      {"type": "multilingual#plain"}
    }
  }
}
```
Analyzer configuration
----------------------
You can specified analysis in app configuration with `ELASTICSEARCH_LANGUAGE_ANALYSIS`. Use `#` and `id` for adding more 
analysis for one specific language.
### Language analysis example
```python
ELASTICSEARCH_LANGUAGE_ANALYSIS= {
        "cs#title": {"czech#title": {
        "type": "custom",
        "char_filter": [
            "html_strip"
        ],
        "tokenizer": "standard"
        }},
        "cs": {"czech": {
            "type": "custom",
            "char_filter": [
                "html_strip"
            ],
            "tokenizer": "standard",
            "filter": [
                "lowercase",
                "stop",
                "snowball"
            ]
        }}
    }
```
### Usage example
```json
{
"settings":{
      "analysis": {
        "analyzer": {
         "oarepo:extends": "multilingual_analysis"
          }
      }
},
"mappings": {
   ...
}
}
```
```json
{
"settings":{
      "analysis": {
        "analyzer": {
         "oarepo:extends": "multilingual_analysis#title"
          }
      }
},
"mappings": {
   ...
}
}
```

  [image]: https://img.shields.io/github/license/oarepo/oarepo-multilingual.svg
  [1]: https://github.com/oarepo/oarepo-multilingual/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/oarepo-multilingual.svg
  [3]: https://travis-ci.org/oarepo/oarepo-multilingual
  [4]: https://img.shields.io/coveralls/oarepo/oarepo-multilingual.svg
  [5]: https://coveralls.io/r/oarepo/oarepo-multilingual
  [6]: https://img.shields.io/pypi/v/oarepo-multilingual.svg
  [7]: https://pypi.org/pypi/oarepo-multilingual
  
