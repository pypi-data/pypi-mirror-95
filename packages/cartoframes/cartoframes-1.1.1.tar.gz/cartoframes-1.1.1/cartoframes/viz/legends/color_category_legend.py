from ..legend import Legend


def color_category_legend(title=None, description=None, footer=None, prop='color',
                          variable=None, dynamic=True):
    """Helper function for quickly creating a color category legend.

    Args:
        title (str, optional):
            Title of legend.
        description (str, optional):
            Description in legend.
        footer (str, optional):
            Footer of legend. This is often used to attribute data sources.
        prop (str, optional): Allowed properties are 'color' and 'stroke_color'.
            It is 'color' by default.
        variable (str, optional):
            If the information in the legend depends on a different value than the
            information set to the style property, it is possible to set an independent
            variable.
        dynamic (boolean, optional):
            Update and render the legend depending on viewport changes.
            Defaults to ``True``.

    Returns:
        cartoframes.viz.legend.Legend

    Example:
        >>> color_category_legend(
        ...     title='Legend title',
        ...     description='Legend description',
        ...     footer='Legend footer',
        ...     dynamic=False)

    """
    return Legend('color-category', title, description, footer, prop, variable, dynamic, ascending=True)
