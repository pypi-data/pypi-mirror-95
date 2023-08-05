try:
    # python2
    from urllib import unquote
    from urlparse import urlparse
    from urlparse import parse_qsl
except ImportError:
    # python3
    from urllib.parse import unquote
    from urllib.parse import urlparse
    from urllib.parse import parse_qsl

from redis.connection import URL_QUERY_ARGUMENT_PARSERS


def _parse_url(url):
    scheme = urlparse(url).scheme
    schemeless = url[len(scheme) + 3:]
    # parse with HTTP URL semantics
    parts = urlparse('http://' + schemeless)

    # The first pymongo.Connection() argument (host) can be
    # a mongodb connection URI. If this is the case, don't
    # use port but let pymongo get the port(s) from the URI instead.
    # This enables the use of replica sets and sharding.
    # See pymongo.Connection() for more info.
    port = scheme != 'mongodb' and parts.port or None
    hostname = schemeless if scheme == 'mongodb' else parts.hostname
    path = parts.path or ''
    path = path[1:] if path and path[0] == '/' else path
    return (scheme, unquote(hostname or '') or None, port,
            unquote(parts.username or '') or None,
            unquote(parts.password or '') or None,
            unquote(path or '') or None,
            dict(parse_qsl(parts.query)))


def parse_url(url):
    scheme, host, port, user, password, db, query = _parse_url(url)
    assert scheme == 'redis'
    for param, value in query.items():
        if param in URL_QUERY_ARGUMENT_PARSERS:
            parser = URL_QUERY_ARGUMENT_PARSERS[param]
            query[param] = parser(value)
    return dict(host=host, port=port, password=password, db=db, **query)

if __name__ == '__main__':
    print(parse_url('redis://127.0.0.1:6379/1?name=node2&max_connections=100'))
