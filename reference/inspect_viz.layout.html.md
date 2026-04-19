# inspect_viz.layout – Inspect Viz

### hconcat

Horizontally concatenate components in a row layout.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/da0a73dfe16a54cafe18cb65dc40676bab93e9cc/src/inspect_viz/layout/_concat.py#L16)

``` python
def hconcat(*component: Component) -> Component
```

`*component` [Component](../reference/inspect_viz.html.md#component)  
Components to concatenate.

### vconcat

Vertically concatenate components in a column layout.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/da0a73dfe16a54cafe18cb65dc40676bab93e9cc/src/inspect_viz/layout/_concat.py#L6)

``` python
def vconcat(*component: Component) -> Component
```

`*component` [Component](../reference/inspect_viz.html.md#component)  
Components to concatenate.

### hspace

Horizontal space to place between widgets.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/da0a73dfe16a54cafe18cb65dc40676bab93e9cc/src/inspect_viz/layout/_space.py#L4)

``` python
def hspace(hspace: float | str = 10) -> Component
```

`hspace` float \| str  
Amount of space. Number values indicate screen pixels. String values may use CSS units (em, pt, px, etc).

### vspace

Veritcal space to place between widgets.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/da0a73dfe16a54cafe18cb65dc40676bab93e9cc/src/inspect_viz/layout/_space.py#L13)

``` python
def vspace(vspace: float | str = 10) -> Component
```

`vspace` float \| str  
Amount of space. Number values indicate screen pixels. String values may use CSS units (em, pt, px, etc).
