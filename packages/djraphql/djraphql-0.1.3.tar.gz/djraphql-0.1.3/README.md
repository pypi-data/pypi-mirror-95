# DjraphQL Schema Builder

## What

DjraphQL ("GiraffeQL") is a library that examines your Django models and builds a flexible, performant GraphQL schema using [Graphene](https://docs.graphene-python.org/en/latest/). No resolvers necessary.

You can of course extend this schema, reference the defined types and build custom business logic into your own resolvers. The goal is to remove the monotonous 90% of boilerplate generalized C.R.U.D. and allow you to focus on stuff that can't be auto-generated.

## Why

Django is a wonderful and ubiquitous framework that provides tons of great tooling and an active ecosystem of additional libraries. One such library is Django Rest Framework, which is great for serving a REST API.

I became frustrated with how DRF handles nested inserts and updates and how our Serializers tend to bloat into a mess of if-statements and validations and hacks like overriding `to_internal_value` and `to_representation` to get things working. You might say, "you're doing it wrong." Fair. I probably was. :)

Still, every time a frontend component needed a piece of data that wasn't already provided by an existing endpoint, you had to add the endpoint to urls.py, build the handler View, and use the ORM to serve the data. Don't forget error handling. Don't forget to check permissions. Multiply this by 10, 20, 100 developers and you have an explosion of endpoints all built in different ways: View, APIView, ViewSet. Some use Serializers, some use bespoke parsing.

What I'm getting at is a human problem: we could have done better at coaching people to do it The Right Way. But in a startup the time for that tends to slip as the end of the sprint approaches.

But it can also be the case that an API becomes more than what's easily served by REST. We have a lot of RPC-style endpoints that follow more of a command pattern. We have very deeply nested data served by our API. These things map well to GraphQL.

## How

You provide a list of Django models and some associated metadata. For example, you can define the QuerySet that will be used for each fetch of a certain model type (you have access to the Django request object in the definition lambda for the QuerySet). By providing a QuerySet that is already filtered by e.g., user account, the library will use that QuerySet in the resolvers it generates. The requirement that you must _remember_ to filter by account is all but eliminated.

It builds each relationship into the schema, so you can traverse from `Label` to `Artists` to `Albums` to `Songs` in a single query, still retreiving only the data you need.

You can specify arbitrarily complex SQL statements: the schema allows specifying filtering via `where`, `orderBy`, `offset`, `limit` clauses.

It allows smooth (nested, if you're bold enough!) updates & inserts.

It even allows aggregate queries. You can `sum`, `avg`, `max`, `min` columns right from the frontend.

Perhaps best of all, it automatically generates `select_related` and `prefetch_related` calls to your QuerySet. This avoids the classic GraphQL N+1 problem usually solved by things like [dataloader](https://docs.graphene-python.org/en/latest/execution/dataloader/).

A hand-rolled schema providing all of this for a single model would be hundreds of lines of code. Multiply that by a realistic, mature application with a hundred or more models, and you have an unmaintainable mess. This library auto-generates it for you, leaving the "fun" stuff for you.

## Show me some code!

Let's walk through some examples. We'll start with creating our Django models for our Spotify clone.

```python
from djraphql import SchemaBuilder
from djraphql.entities import Entity
from sample_music_app.models import Artist, Album, Label, Song
from graphene import Schema

class LabelEntity(Entity):
    class Meta:
        model = Label

class ArtistEntity(Entity):
    class Meta:
        model = Artist

class AlbumEntity(Entity):
    class Meta:
        model = Album

class SongEntity(Entity):
    class Meta:
        model = Song

type_generator = SchemaBuilder([
    LabelEntity,
    ArtistEntity,
    AlbumEntity,
    SongEntity
])

schema = Schema(
    query=type_generator.QueryRoot,
    mutation=type_generator.MutationRoot,
)
```

We've created a `Entity` class for each Django model we want to add to our schema. We pass these classes to the `SchemaBuilder` which will then expose two properties: `QueryRoot` and `MutationRoot`. We pass these properties to our `Schema` instance, imported from the `graphene` library.

Let's insert some data:

```python
parlophone = Label.objects.create(name='Parlophone', established_year=1896)
Artist.objects.create(name='The Beatles', label=parlophone)

sue_records = Label.objects.create(name='Sue Records', established_year=1957)
Artist.objects.create(name='Jimmy Hendrix', label=sue_records)
```

Now, let's query it.

```python
result = schema.execute("""
    query {
        ArtistsMany {
            name
            label {
                name
                establishedYear
            }
        }
    }
""")

assert result.data == {
    'ArtistsMany': [
        {
            'name': 'The Beatles',
            'label': {
                'name': 'Parlophone',
                'establishedYear': 1896,
            }
        }, {
            'name': 'Jimmy Hendrix',
            'label': {
                'name': 'Sue Records',
                'establishedYear': 1957,
            }
        }
    ]
}
```

## Default behavior of entity objects

Each class inheriting from `Entity` requires a single subclass called `Meta`, which must contain a `model` field that indicates which Django model class we're dealing with.

This will expose 3 queries:

- `MyModelByPk(pk: Int!): MyModel!`
- `MyModelsMany(where: WhereMyModel orderBy: OrderByMyModel limit: Int offset: Int): [MyModel!]!`
- `MyModelsAggregate(where: WhereMyModel orderBy: OrderByMyModel): MyModelAggregateResult!`

By default, no mutations are generated, because `Entity`s are read-only unless specified otherwise (via the `access_permissions` field).

## Customizing entity objects

There are a few properties we can leverage on `Entity` to customize the behavior of our generated schema.

### `access_permissions`

A read-only API is useful, but at some point we'll need to mutate our data. We can add mutations by defining an `access_permissions` field on our entity class.

`Entity` contains a `access_permissions` bit-field with a default value of `R` (`READ`).

To add the ability to create, update, or delete an object, we must override `access_permissions`:

```python
from cool_app.models import MyModel
from djraphql.access_permissions import C, R, U, D
# If too much brevity, CREATE, READ, UPDATE, DELETE works too!

class MyModelEntity(Entity):
    class Meta:
        model = MyModel

    access_permissions = C | R | U | D
```

This will instruct the schema generator to create 3 GraphQL mutations:

- `insertMyModel(data: MyModelInput! tag: String): InsertMyModel` (`C`/`CREATE` required)
- `updateMyModel(pk: Int! data: MyModelUpdateInput! tag: String): UpdateMyModel` (`U`/`UPDATE` required)
- `deleteMyModel(pk: Int!): DeleteMyModel` (`D`/`DELETE` required)

### `filter_backends`

TODO

### `include_fields`/`exclude_fields`

TODO

### `properties`

TODO

### `get_for_insert`

TODO

### `before_insert`

TODO

# Contributing

## Virtual environments

Create virtual environments to run the Django app (assumes `python --version` prints `Python 2.7.17`):

- `virtualenv .venv-py2`
- `virtualenv -p python3 .venv-py3`

Activate one of them

> In VSCode, it may be necessary to `cmd+shift+p`, `Python: Select interpreter` to set the correct venv for the debugger.

- `source .venv-py3/bin/activate`

Install dependencies. Leave Django out of requirements and explicitly install it, so that we can easily test across multiple versions.

- `pip install -r requirements.txt django==1.11.17`

## Run tests

First activate one of your virtual environments:

- `python ./manage.py test`

### Run tests w/ test coverage metrics

```
coverage run --source djraphql -m pytest
coverage report -m
```

## Remove unused imports

- `pip install autoflake`
- `autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports ./**/*.py`

## Build for distribution

See tutorial [here](https://packaging.python.org/tutorials/packaging-projects/).

#### Install setuptools

- `pip install --user --upgrade setuptools wheel`

#### Package the library

- `python setup.py sdist bdist_wheel`

#### Build the docs

- `pip install -r requirements-docs.txt`
- `cd docs && make html`
