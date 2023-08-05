from ..legend import Legend


def color_bins_legend(title=None, description=None, footer=None, prop='color',
                      variable=None, dynamic=True, ascending=False, format=None):
    """Helper function for quickly creating a color bins legend.

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
        ascending (boolean, optional):
            If set to ``True`` the values are sorted in ascending order.
            Defaults to ``False``.
        format (str, optional): Format to apply to number values in the widget, based on d3-format
            specifier (https://github.com/d3/d3-format#locale_format).

    Returns:
        cartoframes.viz.legend.Legend

    Example:
        >>> color_bins_legend(
        ...     title='Legend title',
        ...     description='Legend description',
        ...     footer='Legend footer',
        ...     dynamic=False,
        ...     format='.2~s')

    """
    return Legend('color-bins', title, description, footer, prop, variable, dynamic, ascending, format)
