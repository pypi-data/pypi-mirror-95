# UriNormRules

[![PyPI version](https://badge.fury.io/py/acdh-uri-norm-rules.svg)](https://badge.fury.io/py/acdh-uri-norm-rules)
[![Latest Stable Version](https://poser.pugx.org/acdh-oeaw/uri-norm-rules/v/stable)](https://packagist.org/packages/acdh-oeaw/uri-norm-rules)
[![License](https://poser.pugx.org/acdh-oeaw/uri-norm-rules/license)](https://packagist.org/packages/acdh-oeaw/uri-norm-rules)

Set of URI normalization rules used within the [ACDH-CD](https://www.oeaw.ac.at/acdh/).

Provides Python 3 and PHP bindings.

Rules are stored as a JSON in the `UriNormRules/rules.json` file.

# Installation & usage

## Python

* Install using pip3:
  ```bash
  pip3 install acdh_uri-norm-rules
  ```
* Use with
  ```Python
  from AcdhUriNormRules import get_rules, get_normalized_uri
  print(AcdhUriNormRules.get_rules())

  wrong_id = "http://sws.geonames.org/1232324343/linz.html"

  good_id = get_normalized_uri(wrong_id)
  print(good_id)
  # "https://www.geonames.org/1232324343"
  ```

## PHP

* Install using using [composer](https://getcomposer.org/doc/00-intro.md):
  ```bash
  composer require acdh-oeaw/uri-norm-rules
  ```
* Usage with
  ```php
  require_once 'vendor/autoload.php';
  print_r(acdhOeaw\UriNormRules::getRules());
  ```
