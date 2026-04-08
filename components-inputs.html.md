# Inputs

Inputs are used to create interactive visualisations by targeting either [Param](reference/inspect_viz.html.md#param) values or [Selection](reference/inspect_viz.html.md#selection) ranges. Available inputs include:

- [select()](reference/inspect_viz.input.html.md#select)
- [slider()](reference/inspect_viz.input.html.md#slider)
- [search()](reference/inspect_viz.input.html.md#search)
- [checkbox()](reference/inspect_viz.input.html.md#checkbox)
- [radio_group()](reference/inspect_viz.input.html.md#radio_group)
- [checkbox_group()](reference/inspect_viz.input.html.md#checkbox_group)

All inputs can write updates to a provided [Param](reference/inspect_viz.html.md#param) or [Selection](reference/inspect_viz.html.md#selection). Param values are updated to match the input value. Selections are provided a predicate clause. This linking can be bidirectional: an input component will also subscribe to a param and track its value updates.

## Select

The [select()](reference/inspect_viz.input.html.md#select) input is used to select one more more values from a list. The list can be sourced from a data column (via the `column` parameter) or be static (via the `options` parameter). Here is a select input bound to a column (this input targets the default [Selection](reference/inspect_viz.html.md#selection) associated with the passed [Data](reference/inspect_viz.html.md#data)):

``` python
from inspect_viz import Data
from inspect_viz.input import select

penguins = Data.from_file("penguins.parquet")

select(penguins, label="Species", column="species")
```

Note that by default the select has no value so does not filtering (represented by the default “All” selection). If you want a [select()](reference/inspect_viz.input.html.md#select) to have an initial value then specify it using the `value` parameter (or pass ‘auto’ to select the first value):

``` python
select(penguins, label="Species", column="species", value="auto")
```

Here is a select input with explicit options (this input targets a [Param](reference/inspect_viz.html.md#param)):

``` python
from inspect_viz import Param

fruit = Param("Apple")

select(label="Fruit", options=["Apple", "Orange", "Banana"], target=fruit)
```

Pass `multiple=True` to enable multiple inputs. In this case values are specified via typing/autocomplete rather than a drop down menu.

``` python
athletes = Data.from_file("athletes.parquet")

select(athletes, label="Sports", column="sport", multiple=True)
```

## Slider

The [slider()](reference/inspect_viz.input.html.md#slider) input enables specificiation of either a single numeric value or a range of values. Here we enable the selection of a maximum body mass for a column:

``` python
from inspect_viz.input import slider

slider(penguins, label="Max Body Mass", column="body_mass")
```

Pass `select="interval"` to specify an interval rather than single value:

``` python
slider(penguins, label="Body Mass Range", column="body_mass", select="interval")
```

Sliders can also target a [Param](reference/inspect_viz.html.md#param) and have explicit `min`, `max`, and `step` values:

``` python
bias = Param(0.5)

slider(label="Bias", min=0, max=1.0, step=0.1, target=bias)
```

## Search

The [search()](reference/inspect_viz.input.html.md#search) input enables filtering a dataset based on text matching. For example, this input filters by WNBA player name

``` python
from inspect_viz.input import search

players = Data.from_file("wnba-shots-2023.parquet")

search(players, label="Athlete", column="athlete_name")
```

## Checkbox

The [checkbox()](reference/inspect_viz.input.html.md#checkbox) input enables toggling a binary value. You can either target boolean [Param](reference/inspect_viz.html.md#param) values or provide custom values mapped to checked and unchecked.

``` python
from inspect_viz.input import checkbox

enabled = Param(True)

checkbox(label="Enabled", target=enabled)
```

Here we provide custom values that map to checked and unchecked states:

``` python
bias = Param(0.1)

checkbox(label="Use Bias", values=[0.0, 0.1], target=bias)
```

## Radio Group

The [radio_group()](reference/inspect_viz.input.html.md#radio_group) is an alternative to [select()](reference/inspect_viz.input.html.md#select) which displays all of the available options rather than collapsing them into a menu:

``` python
from inspect_viz.input import radio_group

penguins = Data.from_file("penguins.parquet")

radio_group(penguins, label="Species", column="species")
```

Or targeting a [Param](reference/inspect_viz.html.md#param):

``` python
fruit = Param("Apple")

radio_group(label="Fruit", options=["Apple", "Orange", "Banana"], target=fruit)
```

## Checkbox Group

The [checkbox_group()](reference/inspect_viz.input.html.md#checkbox_group) provides an interface to select multiple values (similar to `select(..., multiple=True)`):

``` python
from inspect_viz.input import checkbox_group

penguins = Data.from_file("penguins.parquet")

checkbox_group(penguins, label="Species", column="species")
```

You can also use [checkbox_group()](reference/inspect_viz.input.html.md#checkbox_group) with a [Param](reference/inspect_viz.html.md#param):

``` python
fruit = Param(["Apple", "Orange"])

checkbox_group(label="Fruit", options=["Apple", "Orange", "Banana"], target=fruit)
```
