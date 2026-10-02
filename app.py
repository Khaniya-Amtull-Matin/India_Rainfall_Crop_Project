import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# ─── 1. DATA LOADING & PREPROCESSING ───────────────────
df = pd.read_csv('yeild_data.csv')

df['State_Name'] = df['State_Name'].str.strip().str.title()
df['Crop'] = df['Crop'].str.strip().str.title()
df['Season'] = df['Season'].str.strip().str.title()

states_list = sorted(df['State_Name'].unique())
state_options = [{'label': 'All India (Comprehensive)', 'value': 'ALL'}] + [
    {'label': state, 'value': state} for state in states_list
]

seasons_list = sorted(df['Season'].unique())
season_options = [{'label': 'All Seasons (Overall)', 'value': 'ALL'}] + [
    {'label': season, 'value': season} for season in seasons_list
]

min_year = int(df['Crop_Year'].min())
max_year = int(df['Crop_Year'].max())

DARK_VIBRANT_PALETTE = [
    '#38bdf8', '#f43f5e', '#34d399', '#fbbf24', '#a855f7',
    '#06b6d4', '#ec4899', '#10b981', '#f97316', '#6366f1',
    '#f472b6', '#22c55e', '#eab308', '#8b5cf6', '#0284c7'
]

app = dash.Dash(__name__)
app.title = f"Refined India Rainfall & Crop Production ({min_year}-{max_year})"

# ─── 2. DASHBOARD LAYOUT ───────────────────────────────
app.layout = html.Div(
    style={
        'backgroundColor': '#0f172a',
        'fontFamily': "'Inter', 'Segoe UI', Roboto, sans-serif",
        'padding': '25px 35px',
        'minHeight': '100vh',
        'color': '#f8fafc',
        'boxSizing': 'border-box'
    },
    children=[
        dcc.Download(id="download-dataframe-csv"),

        # Executive Header Banner
        html.Div(
            style={
                'backgroundColor': '#1e293b',
                'padding': '25px 30px',
                'borderRadius': '12px',
                'border': '1px solid #334155',
                'boxShadow': '0 6px 16px rgba(0,0,0,0.4)',
                'marginBottom': '25px',
                'textAlign': 'center',
                'boxSizing': 'border-box'
            },
            children=[
                html.H1(
                    f"Refined India Rainfall & Crop Production Analysis ({min_year} - {max_year})",
                    style={
                        'margin': '0 0 8px 0',
                        'color': '#f8fafc',
                        'fontSize': '28px',
                        'fontWeight': '800',
                        'textAlign': 'center'
                    }
                ),
                html.P(
                    "Interactive Analytics Dashboard with Real-Time Weather & Yield Correlation",
                    style={'margin': '0 0 15px 0', 'color': '#94a3b8', 'fontSize': '15px', 'fontWeight': '500', 'textAlign': 'center'}
                ),
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'center'},
                    children=[
                        html.Button(
                            "📥 Export Filtered Data (CSV)",
                            id="btn-csv-download",
                            style={
                                'backgroundColor': '#38bdf8',
                                'color': '#0f172a',
                                'border': 'none',
                                'padding': '10px 22px',
                                'borderRadius': '8px',
                                'fontWeight': '700',
                                'fontSize': '14px',
                                'cursor': 'pointer',
                                'boxShadow': '0 4px 12px rgba(56, 189, 248, 0.3)'
                            }
                        )
                    ]
                )
            ]
        ),

        # Control Panel (State, Season, Top Crops)
        html.Div(
            style={
                'backgroundColor': '#1e293b',
                'padding': '20px 25px',
                'borderRadius': '12px',
                'border': '1px solid #334155',
                'boxShadow': '0 4px 12px rgba(0,0,0,0.3)',
                'marginBottom': '25px',
                'display': 'flex',
                'justifyContent': 'space-between',
                'gap': '20px',
                'alignItems': 'center',
                'boxSizing': 'border-box',
                'width': '100%'
            },
            children=[
                html.Div(
                    style={'flex': '1', 'minWidth': '0'},
                    children=[
                        html.Label("Select Geographic State:", style={'fontWeight': '700', 'color': '#cbd5e1', 'fontSize': '15px', 'marginBottom': '8px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='state-dropdown',
                            options=state_options,
                            value='ALL',
                            clearable=False,
                            style={'width': '100%', 'color': '#0f172a', 'fontSize': '14px'}
                        )
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'minWidth': '0'},
                    children=[
                        html.Label("Filter by Season:", style={'fontWeight': '700', 'color': '#cbd5e1', 'fontSize': '15px', 'marginBottom': '8px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='season-dropdown',
                            options=season_options,
                            value='ALL',
                            clearable=False,
                            style={'width': '100%', 'color': '#0f172a', 'fontSize': '14px'}
                        )
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'minWidth': '0'},
                    children=[
                        html.Label("Top Crops Display Limit:", style={'fontWeight': '700', 'color': '#cbd5e1', 'fontSize': '15px', 'marginBottom': '8px', 'display': 'block'}),
                        dcc.Dropdown(
                            id='top-n-crops-dropdown',
                            options=[
                                {'label': 'Top 5 Primary Crops', 'value': 5},
                                {'label': 'Top 10 Primary Crops', 'value': 10},
                                {'label': 'Top 15 Primary Crops', 'value': 15}
                            ],
                            value=10,
                            clearable=False,
                            style={'width': '100%', 'color': '#0f172a', 'fontSize': '14px'}
                        )
                    ]
                )
            ]
        ),

        # Clean Timeline Panel (Inputs + Valid RangeSlider)
        html.Div(
            style={
                'backgroundColor': '#1e293b',
                'padding': '20px 25px 25px 25px',
                'borderRadius': '12px',
                'border': '1px solid #334155',
                'boxShadow': '0 4px 12px rgba(0,0,0,0.3)',
                'marginBottom': '25px',
                'boxSizing': 'border-box',
                'width': '100%'
            },
            children=[
                html.Div(
                    style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '18px'},
                    children=[
                        html.Label("Historical Year Range:", style={'fontWeight': '700', 'color': '#cbd5e1', 'fontSize': '15px'}),
                        html.Div(
                            style={'display': 'flex', 'gap': '12px', 'alignItems': 'center'},
                            children=[
                                html.Span("Start Year:", style={'color': '#94a3b8', 'fontSize': '14px', 'fontWeight': '600'}),
                                dcc.Input(
                                    id='start-year-input',
                                    type='number',
                                    min=min_year,
                                    max=max_year,
                                    value=min_year,
                                    style={
                                        'backgroundColor': '#0f172a',
                                        'color': '#38bdf8',
                                        'border': '1px solid #334155',
                                        'padding': '6px 10px',
                                        'borderRadius': '6px',
                                        'fontSize': '14px',
                                        'fontWeight': '700',
                                        'width': '80px',
                                        'textAlign': 'center',
                                        'outline': 'none'
                                    }
                                ),
                                html.Span("End Year:", style={'color': '#94a3b8', 'fontSize': '14px', 'fontWeight': '600'}),
                                dcc.Input(
                                    id='end-year-input',
                                    type='number',
                                    min=min_year,
                                    max=max_year,
                                    value=max_year,
                                    style={
                                        'backgroundColor': '#0f172a',
                                        'color': '#38bdf8',
                                        'border': '1px solid #334155',
                                        'padding': '6px 10px',
                                        'borderRadius': '6px',
                                        'fontSize': '14px',
                                        'fontWeight': '700',
                                        'width': '80px',
                                        'textAlign': 'center',
                                        'outline': 'none'
                                    }
                                )
                            ]
                        )
                    ]
                ),
                dcc.RangeSlider(
                    id='year-range-slider',
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=[min_year, max_year],
                    marks={year: {'label': str(year), 'style': {'color': '#94a3b8', 'fontSize': '13px'}} for year in range(min_year, max_year + 1, 2)},
                    tooltip={"placement": "bottom", "always_visible": False}
                )
            ]
        ),

        # KPI Summary Cards Banner
        html.Div(
            style={'display': 'flex', 'gap': '20px', 'marginBottom': '25px', 'width': '100%', 'boxSizing': 'border-box'},
            children=[
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '12px', 'border': '1px solid #334155', 'textAlign': 'center'},
                    children=[
                        html.P("TOTAL PRODUCTION", style={'margin': '0', 'fontSize': '13px', 'color': '#94a3b8', 'fontWeight': '700'}),
                        html.H2(id='kpi-production', style={'margin': '8px 0 0 0', 'fontSize': '26px', 'color': '#38bdf8', 'fontWeight': '800'})
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '12px', 'border': '1px solid #334155', 'textAlign': 'center'},
                    children=[
                        html.P("AVG RAINFALL (MM)", style={'margin': '0', 'fontSize': '13px', 'color': '#94a3b8', 'fontWeight': '700'}),
                        html.H2(id='kpi-rainfall', style={'margin': '8px 0 0 0', 'fontSize': '26px', 'color': '#34d399', 'fontWeight': '800'})
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '12px', 'border': '1px solid #334155', 'textAlign': 'center'},
                    children=[
                        html.P("MAX CROP YIELD", style={'margin': '0', 'fontSize': '13px', 'color': '#94a3b8', 'fontWeight': '700'}),
                        html.H2(id='kpi-yield', style={'margin': '8px 0 0 0', 'fontSize': '26px', 'color': '#fbbf24', 'fontWeight': '800'})
                    ]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '12px', 'border': '1px solid #334155', 'textAlign': 'center'},
                    children=[
                        html.P("CROP TYPES ANALYZED", style={'margin': '0', 'fontSize': '13px', 'color': '#94a3b8', 'fontWeight': '700'}),
                        html.H2(id='kpi-crops', style={'margin': '8px 0 0 0', 'fontSize': '26px', 'color': '#a855f7', 'fontWeight': '800'})
                    ]
                )
            ]
        ),

        # Dynamic Intelligence Insights Banner
        html.Div(
            id='insights-banner',
            style={
                'backgroundColor': '#1e293b',
                'padding': '15px 25px',
                'borderRadius': '12px',
                'border': '1px solid #334155',
                'marginBottom': '25px',
                'color': '#cbd5e1',
                'fontSize': '15px',
                'display': 'flex',
                'justifyContent': 'space-around',
                'alignItems': 'center',
                'fontWeight': '600',
                'boxSizing': 'border-box'
            }
        ),

        # Charts Grid
        html.Div(
            style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'width': '100%', 'boxSizing': 'border-box'},
            children=[
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '15px', 'borderRadius': '12px', 'border': '1px solid #334155'},
                    children=[dcc.Graph(id='bar-top-crops', style={'height': '460px'})]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '15px', 'borderRadius': '12px', 'border': '1px solid #334155'},
                    children=[dcc.Graph(id='pie-season-share', style={'height': '460px'})]
                )
            ]
        ),

        html.Div(
            style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px', 'width': '100%', 'boxSizing': 'border-box'},
            children=[
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '15px', 'borderRadius': '12px', 'border': '1px solid #334155'},
                    children=[dcc.Graph(id='scatter-rainfall-yield', style={'height': '460px'})]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '15px', 'borderRadius': '12px', 'border': '1px solid #334155'},
                    children=[dcc.Graph(id='line-yearly-trend', style={'height': '460px'})]
                )
            ]
        ),

        html.Div(
            style={'display': 'flex', 'gap': '20px', 'width': '100%', 'boxSizing': 'border-box'},
            children=[
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '15px', 'borderRadius': '12px', 'border': '1px solid #334155'},
                    children=[dcc.Graph(id='histogram-rainfall', style={'height': '460px'})]
                ),
                html.Div(
                    style={'flex': '1', 'backgroundColor': '#1e293b', 'padding': '15px', 'borderRadius': '12px', 'border': '1px solid #334155'},
                    children=[dcc.Graph(id='box-season-rainfall', style={'height': '460px'})]
                )
            ]
        )
    ]
)

# ─── 3. CALLBACK ROUTINES ──────────────────────────────

# Two-Way Sync between Inputs and Slider
@app.callback(
    [Output('year-range-slider', 'value'),
     Output('start-year-input', 'value'),
     Output('end-year-input', 'value')],
    [Input('year-range-slider', 'value'),
     Input('start-year-input', 'value'),
     Input('end-year-input', 'value')]
)
def sync_slider_and_inputs(slider_val, input_start, input_end):
    ctx = dash.callback_context
    if not ctx.triggered:
        return slider_val, slider_val[0], slider_val[1]
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'year-range-slider':
        return slider_val, slider_val[0], slider_val[1]
    else:
        s_val = input_start if input_start is not None else min_year
        e_val = input_end if input_end is not None else max_year
        if s_val > e_val:
            s_val, e_val = e_val, s_val
        return [s_val, e_val], s_val, e_val


# Download CSV Callback
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-csv-download", "n_clicks"),
    [
        State('state-dropdown', 'value'),
        State('season-dropdown', 'value'),
        State('year-range-slider', 'value')
    ],
    prevent_initial_call=True
)
def export_filtered_csv(n_clicks, selected_state, selected_season, year_range):
    dff = df.copy()
    if selected_state != 'ALL':
        dff = dff[dff['State_Name'] == selected_state]
    if selected_season != 'ALL':
        dff = dff[dff['Season'] == selected_season]
    dff = dff[(dff['Crop_Year'] >= year_range[0]) & (dff['Crop_Year'] <= year_range[1])]
    return dcc.send_data_frame(dff.to_csv, index=False, filename="filtered_crop_rainfall_data.csv")


# Visualizations Callback
@app.callback(
    [
        Output('kpi-production', 'children'),
        Output('kpi-rainfall', 'children'),
        Output('kpi-yield', 'children'),
        Output('kpi-crops', 'children'),
        Output('insights-banner', 'children'),
        Output('bar-top-crops', 'figure'),
        Output('pie-season-share', 'figure'),
        Output('scatter-rainfall-yield', 'figure'),
        Output('line-yearly-trend', 'figure'),
        Output('histogram-rainfall', 'figure'),
        Output('box-season-rainfall', 'figure')
    ],
    [
        Input('state-dropdown', 'value'),
        Input('season-dropdown', 'value'),
        Input('top-n-crops-dropdown', 'value'),
        Input('year-range-slider', 'value')
    ]
)
def update_dashboard_visualizations(selected_state, selected_season, top_n, year_range):
    dff = df.copy()
    if selected_state != 'ALL':
        dff = dff[dff['State_Name'] == selected_state]
    if selected_season != 'ALL':
        dff = dff[dff['Season'] == selected_season]
    
    dff = dff[(dff['Crop_Year'] >= year_range[0]) & (dff['Crop_Year'] <= year_range[1])]

    state_str = "All India" if selected_state == 'ALL' else selected_state
    season_str = "All Seasons" if selected_season == 'ALL' else selected_season
    
    region_title = f"{state_str} | {season_str}"

    # KPI Values
    tot_prod = f"{dff['Production'].sum() / 1e6:.2f} M Tons" if not dff.empty else "0"
    avg_rain = f"{dff['Rainfall'].mean():.1f} mm" if not dff.empty else "0"
    max_yield = f"{dff['Yeild'].max():.1f}" if not dff.empty else "0"
    num_crops = f"{dff['Crop'].nunique()}" if not dff.empty else "0"

    # Insights Content
    if not dff.empty:
        yearly_prod = dff.groupby('Crop_Year')['Production'].sum()
        peak_year = yearly_prod.idxmax() if not yearly_prod.empty else "N/A"
        top_crop_series = dff.groupby('Crop')['Production'].sum()
        top_crop_name = top_crop_series.idxmax() if not top_crop_series.empty else "N/A"
        insights_children = [
            html.Span(f"🏆 Dominant Crop: {top_crop_name}", style={'color': '#38bdf8'}),
            html.Span(f"📈 Peak Harvest Year: {peak_year}", style={'color': '#fbbf24'}),
            html.Span(f"🌧 Mean Precipitation: {dff['Rainfall'].mean():.1f} mm", style={'color': '#34d399'})
        ]
    else:
        insights_children = [html.Span("No data available for the selected filters.")]

    # Dark Layout Config
    dark_layout_base = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=30, t=50, b=50),
        font=dict(color='#f8fafc', family="Inter, sans-serif", size=14),
        title=dict(font=dict(color='#f8fafc', size=18, family="Inter, sans-serif"), x=0.02, y=0.96),
        xaxis=dict(
            gridcolor='#334155', zerolinecolor='#334155',
            tickfont=dict(color='#cbd5e1', size=13),
            title=dict(font=dict(size=14, color='#f8fafc'))
        ),
        yaxis=dict(
            gridcolor='#334155', zerolinecolor='#334155',
            tickfont=dict(color='#cbd5e1', size=13),
            title=dict(font=dict(size=14, color='#f8fafc'))
        ),
        legend=dict(font=dict(size=13, color='#f8fafc'))
    )

    # 1. Bar Chart
    top_crops_df = dff.groupby('Crop')['Production'].sum().reset_index()
    top_crops_df = top_crops_df.sort_values(by='Production', ascending=False).head(top_n)

    fig_bar = px.bar(
        top_crops_df,
        x='Production',
        y='Crop',
        orientation='h',
        color='Crop',
        title=f"Top {top_n} Produced Crops ({region_title})",
        labels={'Production': 'Total Production (Tons)', 'Crop': 'Crop Category'},
        color_discrete_sequence=DARK_VIBRANT_PALETTE,
        template='plotly_dark'
    )
    fig_bar.update_layout(**dark_layout_base, showlegend=False, yaxis_categoryorder='total ascending')

    # 2. Pie Chart
    season_df = dff.groupby('Season')['Production'].sum().reset_index()
    fig_pie = px.pie(
        season_df,
        names='Season',
        values='Production',
        title=f"Crop Production Share by Season ({region_title})",
        color_discrete_sequence=DARK_VIBRANT_PALETTE,
        hole=0.42,
        template='plotly_dark'
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=13,
        marker=dict(line=dict(color='#0f172a', width=2))
    )
    fig_pie.update_layout(**dark_layout_base)

    # 3. Scatter Plot
    fig_scatter = px.scatter(
        dff,
        x='Rainfall',
        y='Yeild',
        color='Season',
        hover_data=['Crop', 'Crop_Year'],
        title=f"Rainfall vs Crop Yield Pattern ({region_title})",
        labels={'Rainfall': 'Annual Rainfall (mm)', 'Yeild': 'Crop Yield'},
        color_discrete_sequence=DARK_VIBRANT_PALETTE,
        template='plotly_dark'
    )
    fig_scatter.update_traces(marker=dict(size=9, opacity=0.85))
    fig_scatter.update_layout(**dark_layout_base)

    # 4. Line Chart
    yearly = dff.groupby('Crop_Year')['Production'].sum().reset_index()
    fig_line = px.line(
        yearly,
        x='Crop_Year',
        y='Production',
        markers=True,
        title=f"Historical Crop Production Trajectory ({region_title})",
        labels={'Crop_Year': 'Year', 'Production': 'Annual Production'},
        template='plotly_dark'
    )
    fig_line.update_traces(line_color='#38bdf8', line_width=3.5, marker=dict(size=8, color='#f43f5e'))
    fig_line.update_layout(**dark_layout_base)

    # 5. Histogram
    fig_hist = px.histogram(
        dff,
        x='Rainfall',
        nbins=25,
        title=f"Annual Rainfall Frequency Distribution ({region_title})",
        labels={'Rainfall': 'Precipitation Level (mm)', 'count': 'Frequency'},
        color_discrete_sequence=['#34d399'],
        template='plotly_dark'
    )
    fig_hist.update_traces(marker_line_color='#0f172a', marker_line_width=1)
    fig_hist.update_layout(**dark_layout_base)

    # 6. Box Plot
    fig_box = px.box(
        dff,
        x='Season',
        y='Rainfall',
        color='Season',
        title=f"Seasonal Rainfall Spread & Outliers ({region_title})",
        labels={'Rainfall': 'Rainfall (mm)', 'Season': 'Farming Season'},
        color_discrete_sequence=DARK_VIBRANT_PALETTE,
        template='plotly_dark'
    )
    fig_box.update_layout(**dark_layout_base, showlegend=False)

    return (
        tot_prod, avg_rain, max_yield, num_crops,
        insights_children,
        fig_bar, fig_pie, fig_scatter, fig_line, fig_hist, fig_box
    )


if __name__ == '__main__':
    app.run(debug=True)