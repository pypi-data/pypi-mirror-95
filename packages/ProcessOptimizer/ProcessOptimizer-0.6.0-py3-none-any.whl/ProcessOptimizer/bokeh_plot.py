
import pickle
import bokeh
from bokeh.io import curdoc, showing
from bokeh.layouts import row, column, gridplot, Spacer
from bokeh.models import ColumnDataSource, Button, Range1d, Span, CustomJS
from bokeh.models.widgets import Slider, TextInput, Toggle, CheckboxButtonGroup, Div, PreText, Select
from bokeh.plotting import figure
from bokeh.models.glyphs import Text, ImageRGBA
from ProcessOptimizer.space import Integer, Categorical
from ProcessOptimizer.plots import _map_categories, dependence, expected_min_random_sampling
from ProcessOptimizer import expected_minimum
import numpy as np
from bokeh.models.markers import Circle
import matplotlib.pyplot as plt
import math
import copy
from bokeh.server.server import Server
import matplotlib as mpl

# Quick introduction.
# The GUI conists of several elements.
# Plots: the plots as they also appear in objective_plot
# Selectors: Sliders that appear on top of the plots with which the red markers can be adjusted
# Toggle_x button group: A group of buttons where we can toggle what parameters we want to plot.
# Generate button: Dependence is only calculated a new when this buton is pressed
# Other buttons: With buttons we can toggle partial dependence on and off, control the n_points variable (resolution when calculating dependence)
#   and control the evaluation method
# Y values: A small text field which shows the expected value as well as confidence interval

# Here we define the global variables (global variables are generally not advices so maybe we should change this at some point)
result = None
x_eval_selectors = None  # This list holds the sliders and selectors for parameter values
# Used to determine what x_eval_selectors were present before last update
old_active_list = None
# The 'reds' field is a (NxN) list. The diagonal holds a Span
source = {'reds': []}
# object with a "location" value, that detemines the location for the red line in the 1d plots.
# The off diagonals holds coordinates for the red markers used in the contour plot.
# 'samples"
x_eval_selectors_values = None
max_pars = None  # Defines the maximum number of parameters that can be plotted
layout = None
button_partial_dependence = None
button_color_map = None
button_draw_confidence = None
button_generate = None
buttons_toggle_x = None
dropdown_eval_method = None
slider_n_points = None
y_value = None
colorbar = None


def set_globals(parsed_result):
    global button_generate, buttons_toggle_x, dropdown_eval_method, slider_n_points, max_pars, source, old_active_list
    global result, x_eval_selectors, layout, x_eval_selectors_values, button_partial_dependence, y_value, button_color_map, colorbar, button_draw_confidence

    # Here we se the values of the global variables and create the layout
    result = parsed_result
    x_eval_selectors_values = copy.copy(result.x)
    max_pars = len(result.space.dimensions)

    # Layout
    button_generate = Button(label="Generate", button_type="success")
    button_generate.on_click(lambda: handle_button_generate(layout, result))
    buttons_toggle_x = CheckboxButtonGroup(
        labels=['x '+str(s) for s in range(max_pars)], active=[])
    button_partial_dependence = Toggle(
        label="Use partial dependence", button_type="default")
    button_color_map = Toggle(
        label="Use same color map", button_type="default")
    button_draw_confidence = Toggle(
        label="Draw upper confidence limit", button_type="default")
    dropdown_eval_method = Select(title="Evaluation method:", value='Result', options=[
                                  'Result', 'Exp min', 'Exp min rand', 'Sliders'], width=200, height=40)
    slider_n_points = Slider(start=1, end=40, value=20,
                             step=1, title="n-points", width=200, height=10)
    y_value = Div(text="""""", width=300, height=200)
    colorbar = Div()  # We initiate colorbar as an empty div first and then change it to a plot in case we want to show it
    row_plots = row([])
    row_top = row(button_generate, buttons_toggle_x)
    col_right_side = column(button_partial_dependence, button_color_map,
                            button_draw_confidence, dropdown_eval_method, slider_n_points, y_value, colorbar)
    col_left_side = column(row_top, row_plots)
    layout = row(col_left_side, col_right_side)


def handle_button_generate(layout, result):
    global old_active_list
    # Remove plots when button is clicked. If we dont do this we ge the "Cant apply patch" bug.
    layout.children[0].children[1] = Div(text="""""",
                                         width=500, height=100)
    # Callback for when generate button gets pressed
    active_list = get_active_list()  # Get the current active list
    n_points = get_n_points()

    # Updating plots
    if active_list:  # Only plot if there is at least one selection
        # x_eval is used both for red markers and as the values for
        x_eval = get_x_eval(result, active_list)
        x_eval_transformed = result.space.transform([x_eval])
        # Calculate y and confidence interval
        y, std = result.models[-1].predict(x_eval_transformed, return_std=True)
        confidence = [round(y[0]-1.96*std[0], 5), round(y[0]+1.96*std[0], 5)]
        # We update the part of the layout that contains the plots
        plots, colorbar_interval = get_plots_layout(
            layout, result, active_list, n_points, x_eval, confidence)

        layout.children[0].children[1] = plots
        # Update text in right side of GUI
        y_value.text = """<font size="5"><b><br>"""+'Y = ' + \
            str(round(y[0], 5))+'</b><br> (' + str(confidence[0]) + \
            ', '+str(confidence[1]) + ')'+'</font>'
        if colorbar_interval:
            colorbar_plot = figure(plot_height=200, plot_width=100, tools='', x_range=[
                                   0, 1], y_range=colorbar_interval)
            im = get_colorbar_as_rgba()
            colorbar_plot.image_rgba(image=[
                                     im], x=0, y=colorbar_interval[0], dw=1, dh=colorbar_interval[1]-colorbar_interval[0])
            colorbar_plot.xaxis.visible = False
            colorbar_plot.toolbar.logo = None
        else:
            colorbar_plot = Div()
        layout.children[1].children[6] = colorbar_plot
    else:  # If no selection we encourage the user to select some parameters
        layout.children[0].children[1] = Div(text="""<font size="10"><br><br>Let's select som parameters to plot!</font>""",
                                             width=500, height=100)
    # Update the old_active_list for next update
    old_active_list = active_list


def get_x_eval_selectors_values():
    # Returns the values for the x_eval_selectors. Uses the global x_eval_selectors_values
    # and for each selector that is present in the GUI we replace the corresponding value.
    # Even though a selector isnot present in the GUI the last value that it had i still retrived.
    global x_eval_selectors
    global old_active_list
    values = x_eval_selectors_values
    if True:
        n = 0  # The index of the selctors in GUI
        for i in old_active_list:  # Use value from GUI selector instead
            val = x_eval_selectors[n].value
            values[i] = val
            n += 1
    values = x_eval_selectors_values
    return values


def get_active_list():
    # returns the a list of the indexes of parameters that have been toggled in
    # the buttons_toggle_x button-group in the GUI
    return buttons_toggle_x.active


def get_n_points():
    # Returns the value of the slider_n_points slider in the GUI
    return slider_n_points.value


def get_use_partial_dependence():
    # Returns True or false depending on wether or not the partial dependence button
    # is toggled in the GUI
    return button_partial_dependence.active


def get_use_same_color_map():
    # Returns True or false depending on wether or not the color_map button
    # is toggled in the GUI
    return button_color_map.active


def get_plot_list(layout, result, active_list, n_points, x_eval, confidence):
    # Returns a NxN list of plots where N is the number of parameters to be plotted.
    # The diagonal is 1d plots and the off diagonal is contour plots
    global source
    use_same_color_map = get_use_same_color_map()
    draw_confidence = button_draw_confidence.active
    if get_use_partial_dependence():
        # Not passing any eval values to dependency function makes it calculate
        # partial dependence
        dependence_eval = None
    else:
        dependence_eval = x_eval

    # First we calculate all the data tat will beused for all the plots. After this we draw the plots.
    plots_data = []
    # It is important that we do it in this order as we need to know the maxmimum and minimum values before drawing the plots,
    # in order to create a correct color-mapping
    plots = []
    space = result.space
    model = result.models[-1]
    bounds = result.space.bounds
    # the iscat variable is a list of bools. True if parameter is categorical. False otherwise.
    # red_vals are the coordinates for the x_eval that is mapped to integers in case they are
    # categorical.
    _, red_vals, iscat = _map_categories(space, result.x_iters, x_eval)
    # We add 0.5 to the value of all categorical integers. This is due to the way bokeh
    # handles plotting of categorical values
    red_vals = [val+0.5 if iscat[i] else val for i, val in enumerate(red_vals)]
    # While iterating through each plot we keep track of the max and min values of y and z in case of 2d plots.
    # We use these values to set the axis of all plots, so they share the same axis.
    val_min_1d = float("inf")
    val_max_1d = -float("inf")
    val_min_2d = float("inf")
    val_max_2d = -float("inf")

    source['reds'] = []  # reset the sources for red markers
    plots_to_do = len(active_list)*(len(active_list)+1)/2  # Triangular numbers
    current_plot = 0  # count how many plots we have calculated so far

    # First we calculate xi, yi and zi for each combination of parameters
    for i_active in range(len(active_list)):
        row = []
        for j_active in range(len(active_list)):
            i = active_list[i_active]
            j = active_list[j_active]
            if j > i:  # We only plot the lower left half of the grid, to avoid duplicates.
                break
            elif i == j:  # Diagonal
                # Passing j = None to dependence makes it calculate a diagonal plot
                xi, yi = dependence(space, model, i, j=None, sample_points=None,
                                    n_samples=250, n_points=n_points, x_eval=dependence_eval)
                row.append({"xi": xi, "yi": yi})

                if np.min(yi) < val_min_1d:
                    val_min_1d = np.min(yi)
                if np.max(yi) > val_max_1d:
                    val_max_1d = np.max(yi)

            else:  # Contour plot
                xi, yi, zi = dependence(space, model, i, j=j, sample_points=None,
                                        n_samples=50, n_points=n_points, x_eval=dependence_eval)
                row.append({"xi": xi, "yi": yi, "zi": zi})
                if np.min(zi) < val_min_2d:
                    val_min_2d = np.min(zi)
                if np.max(zi) > val_max_2d:
                    val_max_2d = np.max(zi)
            current_plot += 1
            # We put the progress into the div where we normally show the y-values (confidence bounds)
            y_value.text = """<font size="5"><b><br> Calculating objective. Please wait. <br> """ + \
                str(int(current_plot))+" / " + \
                str(int(plots_to_do)) + """</font>"""

        plots_data.append(row)

    y_value.text = """<font size="5"><b><br> Drawing. Please wait. <br> """ + \
        str(int(current_plot))+" / "+str(int(plots_to_do)) + """</font>"""
    for i_active in range(len(active_list)):  # Only plot the selected parameters
        source['reds'].append([])
        plots.append([])
        for j_active in range(len(active_list)):
            i = active_list[i_active]
            j = active_list[j_active]
            if j > i:  # We only plot the lower left half of the grid, to avoid duplicates.
                break
            elif i == j:  # Diagonal
                # Passing j = None to dependence makes it calculate a diagonal plot
                xi = plots_data[i_active][j_active]["xi"]
                yi = plots_data[i_active][j_active]["yi"]

                if iscat[i]:  # Categorical
                    x_range = space.dimensions[i].categories
                    # Convert integers to catogorical strings
                    xi = [bounds[i][ind] for ind in xi]
                else:  # Numerical
                    x_range = [bounds[i][0], bounds[i][1]]

                # Source red is what we end up appending to the global source variable
                # So the location of the red line can be changed interactively
                source_red = Span(
                    location=red_vals[i], dimension='height', line_color='red', line_width=3)
                #dotte_line_low = Span(location=red_vals[i], dimension='height', line_color='red', line_width=3)
                # TODO : Create dotted lines
                plot = figure(plot_height=200, plot_width=250, tools='',
                              x_range=x_range, y_range=[val_min_1d, val_max_1d])
                source_line = ColumnDataSource(data=dict(x=xi, y=yi))
                plot.line('x', 'y', source=source_line,
                          line_width=3, line_alpha=0.6)
                # Add span i.e red line to plot
                plot.add_layout(source_red)
                # update max and minimum y _values

            else:  # Contour plot
                xi = plots_data[i_active][j_active]["xi"]
                yi = plots_data[i_active][j_active]["yi"]
                zi = plots_data[i_active][j_active]["zi"]

                if iscat[j]:  # check if values are categorical
                    # Convert integers to catogorical strings
                    xi = [bounds[j][ind] for ind in xi]
                    # At what coordinate in plot to anchor the contour image.
                    # In case of categorical this should be set to 0.
                    x_anchor = 0
                    # The size the image should take up in the plot
                    x_span = len(result.space.dimensions[j].categories)
                    # Range for axis
                    x_range = space.dimensions[j].categories
                else:
                    x_anchor = bounds[j][0]
                    x_span = bounds[j][1]-bounds[j][0]
                    x_range = [np.min(xi), np.max(xi)]
                if iscat[i]:  # check if values are categorical
                    yi = [bounds[i][ind] for ind in yi]
                    y_range = space.dimensions[i].categories
                    y_anchor = 0
                    y_span = len(result.space.dimensions[i].categories)
                else:
                    y_anchor = bounds[i][0]
                    y_span = bounds[i][1]-bounds[i][0]
                    y_range = [np.min(yi), np.max(yi)]

                plot = figure(plot_height=200, plot_width=250,
                              x_range=x_range, y_range=y_range, tools='')

                if use_same_color_map:
                    cmap = [val_min_2d, val_max_2d]
                else:
                    cmap = None
                # Get an rgba contour image from matplotlib as bokeh does not support contour plots
                im = get_plt_contour_as_rgba(
                    xi, yi, zi, confidence, cmap=cmap, draw_confidence=draw_confidence)
                plot.image_rgba(image=[im], x=x_anchor,
                                y=y_anchor, dw=x_span, dh=y_span)
                # x and y samples are the coordinates of the parameter values that have been
                # sampled during the creation of the model
                x_samples = [val[j] for val in result.x_iters]
                y_samples = [val[i] for val in result.x_iters]
                source_samples = ColumnDataSource(
                    data=dict(x=x_samples, y=y_samples))
                source_red = ColumnDataSource(
                    data=dict(x=[red_vals[j]], y=[red_vals[i]]))
                # We plot samples as black circles and the evaluation marker as a  red circle
                plot.circle(x='x', y='y', source=source_samples,
                            size=2, color="black", alpha=0.5)
                plot.circle(x='x', y='y', source=source_red,
                            size=5, color="red", alpha=1)

            # We rotate the categorical labels slighty so they take up less space
            if iscat[j]:
                plot.xaxis.major_label_orientation = 0.3
            if iscat[i] and i != j:  # In case of diagonal the y-labels are numbers and
                    # therefore should not be rotated
                plot.yaxis.major_label_orientation = 1.2

            plot.toolbar.logo = None  # Remove the bokeh logo fom figures
            plots[i_active].append(plot)
            source['reds'][i_active].append(source_red)

    # Setting the same y-range for all diagonal plots for easier comparison
    # for i in range(len(plots)):
       # plots[i][i].y_range = Range1d(y_min,y_max)
    if use_same_color_map:
        colorbar_interval = [val_min_2d, val_max_2d]
    else:
        colorbar_interval = None

    return plots, colorbar_interval


def get_plots_layout(layout, result, active_list, n_points, x_eval, confidence):
    global x_eval_selectors
    plots, colorbar_interval = get_plot_list(
        layout, result, active_list, n_points, x_eval, confidence)
    x_eval_selectors = get_x_eval_selectors_list(result, active_list, x_eval)
    # Create the layout using the lists of plots and selectors.
    # The layout consists of rows that we append plots and selectors to.
    # The selectors should be on top of each diagonal plot, and therefore
    # the layout can be regarded as a (N+1,N) grid to make room for the top selector.
    # The top row therefore consists of only on selector and the bottom row has no
    # selector as the selector for the last diagonal was added in the second last row.

    rows = []
    # The selector in the top left corner
    rows.append(row(x_eval_selectors[0]))
    for i in range(len(plots)):
        if i == len(x_eval_selectors)-1:  # Last row
            rows.append(row(*plots[i]))
        else:
            rows.append(row(*plots[i], x_eval_selectors[i+1]))
    # Create a column with all the rows
    plot_layout = column(*rows)
    return plot_layout, colorbar_interval


def get_x_eval_selectors_list(result, active_list, x_eval):
    # Returns a list of selectors. The selectors are sliders for numerical values and dropdown menus
    # ("Select" object) for categorical values. The selectors are interactive with callbacks everytime
    # a changed by the user
    global x_eval_selectors_values

    bounds = result.space.bounds  # Used for defining what values can be selected
    x_eval_selectors = []
    n = 0  # Index of the plots. Example: If only parameter 3 and 5 is being plotted
    # the selectors for these parameters still have index n = 0 and n= 1.
    for i in active_list:  # Only get selecters that is going to be shown in GUI
        if isinstance(result.space.dimensions[i], Categorical):  # Categorical
            cats = list(result.space.dimensions[i].categories)  # Categories
            # Create a "Select" object which is a type of dropdown menu
            # This object gets a title equal to the parameter number, and the value is set to
            # x_eval
            select = Select(
                title='X'+str(i), value=x_eval[i], options=cats, width=200, height=45)
            # Here we define a callback that updates the appropiate red markers by changing
            # with the current value of the selector by changing the global "source" variable
            # The callback function is written in javascript
            select.js_on_change('value', CustomJS(args=dict(source=source, n=n, cats=cats), code="""
                // Convert categorical to index
                var ind = cats.indexOf(cb_obj.value); 
                // Change red line in diagonal plots
                source['reds'][n][n]['location'] = ind + 0.5;
                // Change red markers in all contour plots
                // First we change the plots in a vertical direction
                for (i = n+1; i < source.reds.length; i++) { 
                    source.reds[i][n].data.x = [ind + 0.5] ;
                    source.reds[i][n].change.emit()
                }
                // Then in a horizontal direction
                for (j = 0; j < n; j++) { 
                    source.reds[n][j].data.y = [ind + 0.5] ;
                    source.reds[n][j].change.emit();
                }
                """)
                                )
            x_eval_selectors.append(select)
            # We update the global selector values
            x_eval_selectors_values[i] = x_eval[i]
        else:  # Numerical
            # For numerical values we create a slider
            # Minimum and maximum values for slider
            start = bounds[i][0]
            end = bounds[i][1]
            # We change the stepsize according to the range of the slider
            step = get_step_size(start, end)
            slider = Slider(
                start=start, end=end, value=x_eval[i], step=step, title='X'+str(i), width=200, height=30)
            # javascript callback function that gets called everytime a user changes the slider value
            slider.js_on_change('value', CustomJS(args=dict(source=source, n=n), code="""
                source.reds[n][n].location = cb_obj.value;
                source.reds[n][n].change.emit()
                for (i = n+1; i < source.reds.length; i++) { 
                    source.reds[i][n].data.x = [cb_obj.value] ;
                    source.reds[i][n].change.emit();
                }
                for (j = 0; j < n; j++) { 
                    source.reds[n][j].data.y = [cb_obj.value] ;
                    source.reds[n][j].change.emit();
                }
                """)
                                )
            x_eval_selectors.append(slider)
            x_eval_selectors_values[i] = x_eval[i]
        n += 1
    return x_eval_selectors


def get_colorbar_as_rgba():
    # plots a colorbar without axes. Code stolen from

    fig, ax = plt.subplots()
    col_map = plt.get_cmap('viridis_r')
    mpl.colorbar.ColorbarBase(ax, cmap=col_map, orientation='vertical')
    fig.subplots_adjust(top=1.01, bottom=0, left=0, right=1)
    plt.axis('off')
    # As for a more fancy example, you can also give an axes by hand:
    fig.canvas.draw()
    # Grab the pixel buffer and dump it into a numpy array
    X = np.array(fig.canvas.renderer._renderer)
    xdim = X.shape[1]
    ydim = X.shape[0]
    # Converting image so that bokeh's image_rgba can read it. (code stolen of the internet)
    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    view[:, :, :] = np.flipud(X)
    plt.close()
    return img


def get_plt_contour_as_rgba(xi, yi, zi, confidence, cmap=None, draw_confidence=None):
    # Returns a matplotlib contour plot as an rgba image
    # We create a matplotlib figure and draws it so we can capture the figure as an image.

    fig = plt.figure()
    ax = fig.add_axes([0., 0., 1., 1.])
    ax = plt.gca()
    if cmap:
        ax.contourf(xi, yi, zi, 10, locator=None,
                    cmap='viridis_r', vmin=cmap[0], vmax=cmap[1])
    else:
        ax.contourf(xi, yi, zi, 10, locator=None, cmap='viridis_r')
    if draw_confidence:
        ax.contour(xi, yi, zi, levels=[
                   confidence[1]], locator=None, colors='black', linestyles=('--',), linewidths=(3,))
    plt.axis('off')
    fig.canvas.draw()
    # Grab the pixel buffer and dump it into a numpy array
    X = np.array(fig.canvas.renderer._renderer)
    xdim = X.shape[1]
    ydim = X.shape[0]
    # Converting image so that bokeh's image_rgba can read it. (code stolen of the internet)
    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    view[:, :, :] = np.flipud(X)
    plt.close()
    return img


def get_x_eval(result, active_list):
    # Returns the evaluation values that is defined by the evaluationmethod dropdown menu
    _, _, iscat = _map_categories(result.space, [result.x], result.x)
    eval_method = dropdown_eval_method.value  # Get evaluation method from GUI

    if eval_method == 'Exp min' and any(iscat):
        # Expected_minimum does not support categorical values
        eval_method = "Exp min rand"
    if eval_method == 'Result':
        x = result.x
    elif eval_method == 'Sliders':
        x = get_x_eval_selectors_values()
    elif eval_method == 'Exp min' and not any(iscat):
        x, _ = expected_minimum(result, n_random_starts=10, random_state=None)
    elif eval_method == 'Exp min rand':
        x = expected_min_random_sampling(
            result.models[-1], result.space, np.min([10**len(result.x), 10000]))
    else:
        ValueError('Could not find evalmethod from dropdown menu')
    return x


def get_step_size(start, end):
    # Returns the stepsize to be used for sliders the stepsize will always be of the form 10**x
    range_log = round((math.log(end-start, 10)))
    # The bigger the range the bigger the stepsize
    step = 10**(range_log-3)
    return step


def modify_doc(doc):
    # Add layout to document
    doc.add_root(layout)
# Update once to initialize message
    handle_button_generate(layout, result)


def start(parsed_result):
    # Set the global variables using the parsed "result"
    set_globals(parsed_result)
    # Start server
    server = Server({'/': modify_doc}, num_procs=1)
    server.start()
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
