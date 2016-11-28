
def get_exporter(short_name):
    from trader.exporters import AVAILABLE_EXPORTERS
    for name, exporter in AVAILABLE_EXPORTERS:
        if name == short_name:
            return exporter
    return KeyError("Exporter with name {} doesn't exist".format(short_name))