Datamart geospatial data
========================

This package contains geospatial data and associated facilities to resolve administrative areas.

To use the fuzzy-search capabilities (`GeoData.resolve_name_fuzzy()`), you will need to install ``datamart-geo[fuzzy]``.

Example usage::

    >>> geo_data = datamart_geo.GeoData.download()  # Download data if needed

    >>> france = geo_data.resolve_name('France')
    >>> france
    <datamart_geo.Area "Republic of France" (3017382) type=Type.ADMIN_0>
    >>> france.latitude, france.longitude
    (46.0, 2.0)
    >>> france.bounds
    (-61.797841, 55.854503, -21.370782, 51.087541)
    >>> assert france.type == datamart_geo.Type.ADMIN_0
    >>> assert france.type == datamart_geo.Type.COUNTRY

    >>> cuers = geo_data.resolve_name('Cuers')
    >>> cuers
    <datamart_geo.Area "Cuers" (6451482) type=Type.ADMIN_4>
    >>> cuers.latitude, cuers.longitude
    (43.2375, 6.07083)
    >>> cuers.get_parent_area()
    <datamart_geo.Area "Arrondissement de Toulon" (2972326) type=Type.ADMIN_3>

    >>> [
    ...     # Show multiple results with their parent ADMIN_1
    ...     (a, a.get_parent_area(datamart_geo.Type.ADMIN_1))
    ...     for a in geo_data.resolve_name_all('Var')
    ... ]
    [(<datamart_geo.Area "Var" (2970749) type=Type.ADMIN_2>,
      <datamart_geo.Area "Provence-Alpes-Côte d'Azur" (2985244) type=Type.ADMIN_1>),
     (<datamart_geo.Area "Vars" (6427887) type=Type.ADMIN_4>,
      <datamart_geo.Area "Nouvelle-Aquitaine" (11071620) type=Type.ADMIN_1>),
     (<datamart_geo.Area "Vars" (6442138) type=Type.ADMIN_4>,
      <datamart_geo.Area "Bourgogne-Franche-Comté" (11071619) type=Type.ADMIN_1>)]

This package was built for Auctus, the dataset search engine from NYU, to resolve named areas during profiling.

See also:

* `The datamart-profiler library, used to profile datasets for search <https://pypi.org/project/datamart-profiler/>`__
* `Auctus, the dataset search engine from NYU <https://auctus.vida-nyu.org/>`__
* `Our project on GitLab <https://gitlab.com/ViDA-NYU/auctus/auctus>`__
