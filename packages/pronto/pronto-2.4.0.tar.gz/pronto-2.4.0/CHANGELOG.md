# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
[Unreleased]: https://github.com/althonos/pronto/compare/v2.4.0...HEAD

## [2.4.0] - 2021-02-18
[2.4.0]: https://github.com/althonos/pronto/compare/v2.3.2...v2.4.0
### Added
- Deprecation warnings for the retrieval of relationships via
  indexing, to be deprecated in `v3`.
### Changed
- Replaced Travis-CI with GitHub Actions to handle continuous integration.
- Bumped `fastobo` dependency to `v0.10.0`.
### Removed
- Retrieval of terms via their alternate IDs (introduced in `v2.3.0`,
  caused multiple issues ([#120](https://github.com/althonos/pronto/issues/120),
  [#126](https://github.com/althonos/pronto/issues/126)).

## [2.3.2] - 2020-12-17
[2.3.2]: https://github.com/althonos/pronto/compare/v2.3.1...v2.3.2
### Added
- Support for path-like objects when creating an `Ontology`
  ([#108](https://github.com/althonos/pronto/pull/108)).
### Fixed
- Avoid decoding file-like objects if they are already **UTF-8**
  encoded when creating an `Ontology`
  ([#110](https://github.com/althonos/pronto/pull/110)).

## [2.3.1] - 2020-09-21
[2.3.1]: https://github.com/althonos/pronto/compare/v2.3.0...v2.3.1
### Fixed
- `pronto.entity` package not being included in source distribution.

## [2.3.0] - 2020-09-21 - **YANKED**
[2.3.0]: https://github.com/althonos/pronto/compare/v2.2.4...v2.3.0
### Added
- Retrieval of entities via their alternate IDs on the source `Ontology`.
- Direct edition of entity relationships via the `Relationships` view.
- `__all__` attribute to all modules of the data model.
- `RelationshipSet` container like `TermSet` with shortcut attributes and
  proxying of actual `Relationship` instances.
- `Relationship.subproperties` and `Relationship.superproperties` methods
  to add, remove, clear and iterate over the subproperties and superproperties
  of a `Relationship` instance.
- `Ontology.synonym_types` method to count (via `SizedIterator`) and iterate
  over the synonym types of an ontology and all of its imports.
- `Ontology.get_synonym_type` method to retrieve a single synonym type by ID
  from an ontology or one of its imports.
### Changed
- Management of sub-properties / super-properties is now consistent with
  the management of subclasses / superclasses.
- `consider`, `disjoint_from`, `disjoint_over`, `equivalent_to`, `replaced_by`
  `transitive_over` and `union_of` properties of `Relationship` now return
  a `RelationshipSet`.
### Fixed
- Outdated documentation in `Term.subclasses` describing the performances of
  the previous algorithm.
- Possible `AttributeError` with the setter of the `Entity.synonyms` property.
- Issue with synonym types declared in imported ontologies not being usable
  with synonyms of the actual ontology.
- Various type annotations not updated since version [2.2.2].

## [2.2.4] - 2020-09-11
[2.2.4]: https://github.com/althonos/pronto/compare/v2.2.3...v2.2.4
### Changed
- Make `Entity.annotations` return a mutable set and add a setter.
### Fixed
- `Term.relationship` erroneously updating the `Ontology._lineage` cache.
- Unneeded code in `pronto.serializers._fastobo` handling `is_a` clauses.

## [2.2.3] - 2020-07-31
[2.2.3]: https://github.com/althonos/pronto/compare/v2.2.2...v2.2.3
### Changed
- Replaced `frozendict` with `immutabledict` ([#90](https://github.com/althonos/pronto/pull/90)).
- Bumped `fastobo` dependency to `v0.9.0` to support inline comments.
- Parsers will now process their imports in parallel using a thread pool.
### Fixed
- Argument type checking in view layer is now disabled during the parsing
  phase to reduce overhead.

## [2.2.2] - 2020-07-18
[2.2.2]: https://github.com/althonos/pronto/compare/v2.2.1...v2.2.2
### Added
- Extraction of basic relationships from RDF/XML documents.
### Fixed
- Erroneous type annotations on `Term.subclasses` and `Term.superclasses`.
- Bug with `Term.equivalent_to` setter crashing with a `NameError`.
- Bug with `Entity.synonyms` setter not extracting synonym data.

## [2.2.1] - 2020-06-17
[2.2.1]: https://github.com/althonos/pronto/compare/v2.2.0...v2.2.1
### Fixed
- Extraction of subclasses/superclasses hierarchy from nested imports.
- Serialization of OBO frames not being done in order.
- Parsing issue with `anti_symmetric` clauses in OBO typedefs.
- Xrefs not being extracted when declared as axioms in RDF/XML documents.
- `ResourceWarning` when creating `Ontology` from file-handles not mapping
  to a filesystem location.

## [2.2.0] - 2020-06-17
[2.2.0]: https://github.com/althonos/pronto/compare/v2.1.0...v2.2.0
### Added
- `threads` parameter to `Ontology` constructor to control the number of
  threads used by parsers supporting multithreading (OBO and OBO JSON at
  the moment).
- Deprecation warnings for suspected uses of the `is_a` pseudo-relationship
  since subclasses/superclasses is now to be handled by the owner `Ontology`.
- Support for subclass/superclass edition directly from the objects returned
  by `Term.subclasses()` and `Term.superclasses()`. ([#84](https://github.com/althonos/pronto/issues/84))
### Changed
- Updated `fastobo` to `v0.8`, which reduce memory footprint of identifiers,
  and improves the parser speed.
- Improved OBO parser performance using threading plus zero-copy validation
  of identifiers on `Xref` instantiation.
- Improved performance in debug mode by having the typechecker only extract
  the wrapped function signature once.
### Fixed
- OBO parser crashing on files containing `idspace` clauses in their headers.
- Reference management issue with binary operations of `TermSet`.
### Removed
- `nanoset` depency, which was not useful anymore in Python 3.8 and caused
  issues with multithreading when processing OBO frames in parallel.

## [2.1.0] - 2020-03-23
[2.1.0]: https://github.com/althonos/pronto/compare/v2.0.1...v2.1.0
### Added
- `Synonym.xrefs` now has a setter. ([#70](https://github.com/althonos/pronto/issues/70))
- `pickle` support for `Ontology`. ([#66](https://github.com/althonos/pronto/issues/66))
- `RdfXmlParser` support for `owl:inverseOf` and `rdfs:subPropertyOf`.
### Changed
- `Synonym.xrefs` now returns a mutable set that can be used to add
  `Xref` to the synonym directly.
### Fixed
- `SynonymType.type` setter does not consider all synonym types as
  undeclared anymore. ([#71](https://github.com/althonos/pronto/issues/71))
- `RdfXmlParser` crashing on synonym types definition without a label
  like in Uberon. ([#67](https://github.com/althonos/pronto/issues/67))
- `FastoboSerializer` crashing when encountering a relationship with
  at least one `replaced_by` clause.

## [2.0.1] - 2020-02-19
[2.0.1]: https://github.com/althonos/pronto/compare/v2.0.0...v2.0.1
### Fixed
- Internal handling of ontology data forcing an `Ontology` to outlive all
  of the `Term`s created from it.
- `Term.id` property missing a return type annotation.
- `Term.equivalent_to` not returning a `TermSet` but a set of strings.
### Changed
- Refactored implementation of `SubclassesIterator` and  
  `SuperclassesIterator` to make both use the interal subclassing cache.
- Make `Term.is_leaf` use internal subclassing cache to make it run in
  constant time.

## [2.0.0] - 2020-02-14
[2.0.0]:https://github.com/althonos/pronto/compare/v1.2.0...v2.0.0
### Added
- `TermSet.subclasses` and `TermSet.superclasses` methods to query all    
  the subclasses / superclasses of all `Term`.
- `TermSet` class to the top-level `pronto` module.
- Dynamic management of subclassing cache for the `Ontology` class.
- Setters for `Term.consider`, `Term.union_of` and `Term.intersection_of`.
### Removed
- `cache` keyword argument for the `Ontology`.
### Fixed
- `SuperclassesIterator.to_set` being named `to_self` because of a typo.
- Several bugs affecting the `fastobo`-backed serializer.

## [1.2.0] - 2020-02-10
[1.2.0]: https://github.com/althonos/pronto/compare/v1.1.5...v1.2.0
### Added
- Parameter `with_self` to disable reflexivity of `Term.subclasses` and
  `Term.superclasses` iterators.
- `TermSet` class which stores a set of terms efficiently while providing
  some useful shortcuts to access the underlying data.
### Changed
- Moved code of `Term.subclasses` and `Term.superclasses` to a dedicated
  iterator class in the `pronto.logic` submodule.
- Dropped `contexter` requirement.
### Fixed
- Fix a typo in `Synonym.type` setter leading to a potential bug when
  the given `type` is `None`.
- Fix miscellaneous bugs found with `mypy`.
- `fastobo` serializer crashing on namespace clauses because of a type
  issue.
- `fastobo` parsers using data version clauses as format version clauses.

## [1.1.5] - 2020-01-25
[1.1.5]: https://github.com/althonos/pronto/compare/v1.1.4...v1.1.5
### Changed
- Bumped `fastobo` to `v0.7.0`, switching parser implementation to use
  multi-threading in order to speedup the parser process.

## [1.1.4] - 2020-01-21
[1.1.4]: https://github.com/althonos/pronto/compare/v1.1.3...v1.1.4
### Added
- Explicit support for Python 3.8.
- Support for Windows-style line endings
  ([#53](https://github.com/althonos/pronto/issues/53))

## [1.1.3] - 2019-11-10
[1.1.3]: https://github.com/althonos/pronto/compare/v1.1.2...v1.1.3
### Fixed
- Handling of some clauses in `FastoboParser`.
- `OboSerializer` occasionaly missing lines between term and typedef frames.
### Added
- Missing docstrings to some `Entity` properties.

## [1.1.2] - 2019-10-30
[1.1.2]: https://github.com/althonos/pronto/compare/v1.1.1...v1.1.2
### Fixed
- `RdfXMLParser` crashing on entities with `rdf:label` elements
  without literal content.

## [1.1.1] - 2019-10-29
[1.1.1]: https://github.com/althonos/pronto/compare/v1.1.0...v1.1.1
### Fixed
- `pronto.serializers` module not being embedded in Wheel distribution.

## [1.1.0] - 2019-10-24
[1.1.0]: https://github.com/althonos/pronto/compare/v1.0.0...v1.1.0
### Added
- `Entity.add_synonym` method to create a new synonym and add it to an entity.
- `@roundrepr` now adds a minimal docstring to the generated `__repr__` method.
- `Ontology` caches subclassing relationships to greatly improve performance of
  `Term.subclasses`.
### Changed
- `Entity` subclasses now store their `id` directly to improve performance.
- `Term.subclasses` and `Term.superclasses` use `collections.deque` instead of
  `queue.Queue` as a LIFO structure since thread-safety is not needed.
- `chardet` result is now used even when prediction confidence is under 100%
  to detect encoding of the handle passed to `Ontology`.
### Fixed
- `SynonymType` comparison implementation.
- `Synonym.type` getter crashing on `type` not being `None`.
- `RdfXMLParser` crashing on synonymtypedefs without scope specifiers.

## [1.0.0] - 2019-10-11
[1.0.0]: https://github.com/althonos/pronto/compare/v1.0.0-alpha.3...v1.0.0
### Fixed
- Issues with typedef serialization in `FastoboSerializer`.
- `Ontology.create_term` and `Ontology.create_relationship` not raising `ValueError`
  when given an identifier already in the knowledge graph.
- Signature of `BaseSerializer.dump` to remove `encoding` argument.
- Missing `__slots__` in `Entity` in non-typechecking runtime.
### Changed
- Bumped `fastobo` requirement to `v0.6.0`.

## [1.0.0-alpha.3] - 2019-10-10
[1.0.0-alpha.3]: https://github.com/althonos/pronto/compare/v1.0.0-alpha.2...v1.0.0-alpha.3
### Added
- Extraction of `oboInOwl:consider` annotation in `RdfXMLParser`.
- Extraction of `oboInOwl:savedBy` annotation in `RdfXMLParser`.
- Extraction of `subsetdef` and `synonymtypedef` as annotation properties in
  `RdfXMLParser`.
- Support for `doap:Version` instead of `owl:VersionIri` for specification
  of ontology data version.
- Proper comparison of `PropertyValue` classes, based on the lexicographic order
  of their serialization.
- `Ontology.dump` and `Ontology.dumps` methods to serialize an ontology in
  **obo** or **obojson** format.
### Fixed
- `Metadata` not storing optional description of ID spaces if any.
- Wrong type hints in `RelationshipData.equivalent_to_chain`.
### Changed
- Added type checking to some more property setters.
- Avoid using `networkx` in `Term.subclasses`.
- `fastobo`-derived parsers will not create a new entity if one exists in the
  graph of dependencies already.
- Exposed `pronto.warnings` and the complete warnings hierarchy.

## [1.0.0-alpha.2] - 2019-10-03
[1.0.0-alpha.2]: https://github.com/althonos/pronto/compare/v1.0.0-alpha.1...v1.0.0-alpha.2
### Added
- Support for extraction of relationships from OWL/XML files to `OwlXMLParser`.
### Fixed
- Type hints of `RelationshipData.synonyms` attribute.

## [1.0.0-alpha.1] - 2019-10-02
[1.0.0-alpha.1]: https://github.com/althonos/pronto/compare/v0.12.2...v1.0.0-alpha.1
### Changed
- Dropped support for Python earlier than `3.6`.
- Brand new data model that follow the OBO 1.4 object model.
- Partial OWL XML parser implementation using the OBO 1.4 semantics.
- New OBO parser implementation based on `fastobo`.
- Imports are properly separated from the top-level ontology.
- `Ontology.__getitem__` can also access entities from imports.
- `Term`, `Relationship`, `Xref`, `SynonymType` compare only based on their ID.
- `Subset`, `Definition` compare only based on their textual value.
### Added
- Support for OBO JSON parser based on `fastobo`.
- Provisional `mypy` type hints.
- Type checking for most properties in `__debug__` mode.
- Proper `repr` implementation that should roundtrip most of the time.
- Detection of file format and encoding based on buffer content.
### Removed
- OBO and JSON serialization support (for now).
- `Term.rchildren` and `Term.rparents` and stop making direction assumptions on relationships.
