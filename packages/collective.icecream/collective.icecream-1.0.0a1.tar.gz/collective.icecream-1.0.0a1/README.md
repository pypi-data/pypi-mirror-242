[![image](https://github.com/collective/collective.icecream/actions/workflows/plone-package.yml/badge.svg)](https://github.com/collective/collective.icecream/actions/workflows/plone-package.yml)
[![Coveralls](https://coveralls.io/repos/github/collective/collective.icecream/badge.svg?branch=main)](https://coveralls.io/github/collective/collective.icecream?branch=main)
[![image](https://codecov.io/gh/collective/collective.icecream/branch/master/graph/badge.svg)](https://codecov.io/gh/collective/collective.icecream)
[![Latest Version](https://img.shields.io/pypi/v/collective.icecream.svg)](https://pypi.python.org/pypi/collective.icecream/)
[![Egg Status](https://img.shields.io/pypi/status/collective.icecream.svg)](https://pypi.python.org/pypi/collective.icecream)
![image](https://img.shields.io/pypi/pyversions/collective.icecream.svg?style=plastic%20%20%20:alt:%20Supported%20-%20Python%20Versions)
[![License](https://img.shields.io/pypi/l/collective.icecream.svg)](https://pypi.python.org/pypi/collective.icecream/)

# collective.icecream

An addon for Plone that does allow you to use the [icecream](https://github.com/gruns/icecream) package

## Installation

Install `collective.icecream` by adding it to your buildout, e.g.:

    [instance]
    eggs +=
        collective.icecream

and then running `bin/buildout`.

When you start your instance in foreground mode you will see:

```shell
[ale@flo collective.icecream]$ ./bin/instance fg
...
ic| 'Icecream installed'
2023-11-24 16:45:13,799 INFO    [Zope:42][MainThread] Ready to handle requests
```

Then you can use the `ic` function everywhere in your code without importing it.

You can also use it in your page templates:

```xml
<?python from icecream import ic; ic("This was placed in a template") ?>
```

TODO: it is planned to not have to import ic from icecream in the templates.

## Authors

The [Syslab.com](https://www.syslab.com) Team.

## Contributors

Put your name here, you deserve it!

- Alessandro Pisa, [Syslab.com](https://www.syslab.com)

## Contribute

- Issue Tracker:
  <https://github.com/collective/collective.icecream/issues>
- Source Code: <https://github.com/collective/collective.icecream>
- Documentation: <https://docs.plone.org/foo/bar>

## Support

If you are having issues, please let us know in the [issue tracker](https://github.com/collective/collective.icecream/issues).

## License

The project is licensed under the GPLv2.
