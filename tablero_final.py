# -*- coding: utf-8 -*-
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash_breakpoints import WindowBreakpoints
# Lectura del archivo csv desde un enlace
file_path = 'https://drive.google.com/uc?id=1pYCoZYra-3JzQsnnkiwBF12HzH1WTX98' #Es el dataset con las correcciones del analisis de datos
df = pd.read_csv(file_path) #Cargamos el dataset
filtered_data=df.copy()
seasons = ["Verano", "Otoño", "Primavera", "Invierno"]
seasonsIcon =["fas fa-sun", "fas fa-leaf", "fas fa-rainbow", "fas fa-snowflake"]
df['Estado del Vuelo'] = df['Estado del Vuelo'].astype('category')
df['Fecha de Salida']=pd.to_datetime(df['Fecha de Salida'])
df['Mes'] = df['Fecha de Salida'].dt.month
df['Dia']= df['Fecha de Salida'].dt.dayofweek
bins = [0, 12, 30, 60, 150]  # Intervalos de edad
labels = ['Infante', 'Joven', 'Mayor', 'Adulto Mayor']  # Etiquetas correspondientes
# Función para obtener la estación
app = dash.Dash(__name__,  meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],external_stylesheets=[dbc.themes.SANDSTONE,"https://use.fontawesome.com/releases/v5.15.4/css/all.css"])
def set_cat(row):
    if row['Total Vuelos'] == 0:
        return '0'
    if row['Total Vuelos'] > 0 and row['Total Vuelos'] < 101:
        return '1 - 100'
    if row['Total Vuelos'] > 101 and row['Total Vuelos'] < 1001:
        return '101 - 1000'
    if row['Total Vuelos'] > 1001 and row['Total Vuelos'] < 2001:
        return '1001 - 2000'
    if row['Total Vuelos'] > 2001 and row['Total Vuelos'] < 5001:
        return '2001 - 5000'
    if row['Total Vuelos'] > 5001 and row['Total Vuelos'] < 10001:
        return '5001 - 10.000'
    if row['Total Vuelos'] > 10001:
        return '10000 y mas'

selected_season = None  # Inicializar variable para almacenar la estación seleccionada
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        ],
    brand="Dashboard Arline Dataset",
    brand_href="#",
    color= "#1f2c56",
    fluid=True,
    dark=True,
    #id="btn_sidebar",

)

INPUT_STYLE = {"margin-right": "10px"}


navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                dbc.Row(
                    [
                        dbc.Col(dbc.Button(html.Img(src=PLOTLY_LOGO, height="30px"), id="btn_sidebar"), width="auto"),
                        dbc.Col(dbc.NavbarBrand("Airline Dashboard", className="ms-2"))
                       ],
                    align="center",
                    className="no-gutters",  # Aplicar la clase CSS no-gutters para eliminar los márgenes
                    ),
                href="#",
                style={"textDecoration": "none"},
                ),

            ],
        fluid=True,
        ),

    color="#1f2c56",
    dark=True,
    className="fixed-top"
)

style_graficos={
    "plot_bgcolor":"#6a6e73",  # Color de fondo
   "paper_bgcolor":"#6a6e73",  # Color del papel (general)
   "font_color":"#ffffff",     # Color de texto
   "bargap":0.1,                # Espacio entre barras
   "uniformtext_minsize":8,   # Tamaño mínimo del texto (evita superposición)
   "margin":dict(l=0, r=0, t=0, b=0),
   "legend":dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "4rem",
    "left": 0,
    "bottom": 0,
    "width": "9rem",
    "padding": "2rem 1rem",
    "background-color": "#1f2c56",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "position": "fixed"
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": "4rem",
    "left": "-9rem",
    "bottom": 0,
    "width": "9rem",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "padding": "2rem 1rem",
    "background-color": "#deb522"
}

INPUT_STYLE={
    "color": "white",
    "background-color": "#1f2c56",
    "border": "none",
    "display":"flex"

}


HEADER_STYLE = {
    # "position": "fixed",
   "margin-top": "4rem",
    #"margin-left": "14rem",
    "margin-left": "9rem",
    "margin-right": "2rem",
    "padding": "1rem",
    "background-color": "#343434",
    "color": "white",
    #"display": "flex",
    "align-items": "center",
    #"width":"80%"
}
HEADER_STYLE1 = {
    #"position": "fixed",
    "margin-top": "4rem",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "1rem",
    "background-color": "#343434",
    "color": "white",
    #"display": "flex",
    "align-items": "center",
    #"width":"80%"
}

PAGE_STYLE = {
    #"margin-left": "14rem",  # Ancho del sidebar
    "margin-left": "9rem",  # Ancho del sidebar
    "margin-right": "2rem",
    "margin-top": "1rem",  # Altura del header
    "padding": "2rem 1rem",
    "background-color": "#343434",
     #"position": "fixed",
}


CONTENT_STYLE = {
    #"margin-left": "14rem",  # Ancho del sidebar
    "margin-left": "10rem",  # Ancho del sidebar
    "margin-right": "2rem",
    "margin-top": "4rem",  # Altura del header
    #"padding": "2rem 1rem",
    "background-color": "#343434",
     #"position": "fixed",
}

CONTENT_STYLE1 = {
    "margin-left": "2rem",  # Ancho del sidebar
    "margin-right": "2rem",
    "margin-top": "4rem",  # Altura del header
    #"padding": "2rem 1rem",
    "background-color": "#343434",
     #"position": "fixed",
}

CARD_STYLE = {
    "background-color": "#6a6e73",
    "color": "white",
    "border-radius": "10px",
}

sidebar = html.Div([
    html.H2("Menu", className="display-8", style={"text-align": "center", "color": "white"}),
    html.Img(src="https://drive.google.com/thumbnail?id=1UcOZWJJWzuZ0WY9CUnW8hmVs8h-dj9Hw", className="img-fluid"),
    html.Hr(),
    html.P("", className="lead"),
    html.Hr(),
    dbc.InputGroup([
        dbc.InputGroupText(
                    html.Div([
                        html.Div(dbc.Checkbox(id=f"season-checkbox-{season}", value=season, style=INPUT_STYLE)),
                        html.Div([
                            html.I(className=seasonsIcon[seasons.index(season)],style={"font-size": "1rem"}),
                            html.Span(season, style={"margin-left": "0.5rem", "font-size": "0.8rem"})
                        ], style={"display": "flex", "align-items": "center"})
                    ], style={"display": "flex"})
                ,style=INPUT_STYLE)
           for season in seasons if season != "x"  # Excluir los datos del eje "x"
           ]),
   ], id="sidebar", style=SIDEBAR_STYLE)


@app.callback(
    [   Output("display", "children"),
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("headers", "style"),
        Output("side_click", "data"),

        ],
    [#Input("navbar-toggler", "n_clicks"),
     Input("btn_sidebar", "n_clicks"),
     Input("breakpoints", "widthBreakpoint")
     ],
    [
        State("side_click", "data"),
        State("breakpoints", "width"),
    ]
)
def toggle_navbar_collapse(n,breakpoint_name: str,nclick, window_width: int):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            header_style=HEADER_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            header_style=HEADER_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        header_style=HEADER_STYLE
        cur_nclick = 'SHOW'
        if window_width<768:
            sidebar_style = SIDEBAR_HIDEN
            header_style = HEADER_STYLE1
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"

    return None,sidebar_style, content_style, header_style, cur_nclick



card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Vuelos", className="card-title"),
            html.I(className="fas fa-plane", style={"margin-right": "5px"}),  # Agrega el icono de avión
            html.P(
                ""
                ,id="tarjeta1"),
            ],style={"text-align": "center"}
        ),style={'paddingBlock':'10px',"backgroundColor":'#deb522','border':'none','borderRadius':'10px'}
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Masculinos", className="card-title"),
            html.I(className="fas fa-male", style={"margin-right": "5px"}),
            html.P(
                ""
                ,id="tarjeta2"),
            ],style={"text-align": "center"}
    ),style={'paddingBlock':'10px',"backgroundColor":'#deb522','border':'none','borderRadius':'10px'}
)

card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Femeninos", className="card-title"),
            html.I(className="fas fa-female", style={"margin-right": "5px"}),
            html.P(
                ""
                ,id="tarjeta3"),
            ],style={"text-align": "center"}
    ),style={'paddingBlock':'10px',"backgroundColor":'#deb522','border':'none','borderRadius':'10px'}
)

card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Menu", className="card-title"),
            html.I(className="fas fa-building", style={"margin-right": "5px"}),
            html.P(
                ""
                ,id="tarjeta4"),
            ],style={"text-align": "center"}
        ),style={'paddingBlock':'10px',"backgroundColor":'#deb522','border':'none','borderRadius':'10px'}
)

header = html.Div(
    [
        html.Div(
            [
                       dbc.Row(
                           [
                               dbc.Col(card1, className="col-md-3 col-sm-6 mb-4"),
                               dbc.Col(card2, className="col-md-3 col-sm-6 mb-4"),
                               dbc.Col(card3, className="col-md-3 col-sm-6 mb-4"),
                               dbc.Col(card4, className="col-md-3 col-sm-6 mb-4"),
                               ],
                           className="mb-4"
                           ),
                       ],

                   id="headers",

    style=HEADER_STYLE  # Aplica el estilo del header
    ),
    ]
)



graficos = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Distribución de edades y géneros en las temporadas", className="card-title")),
                    (dcc.Graph(id="season-graph1"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-6 col-sm-12 mb-3"),
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Distribución de estados de vuelos en las temporades", className="card-title")),
                    (dcc.Graph(id="season-graph2"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-6 col-sm-12 mb-3")
            ]
            ,className="p-4"
            ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Vuelos por continente en las temporadas", className="card-title")),
                    (dcc.Graph(id="season-graph3"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-6 col-sm-12 mb-3 mu-1"),
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Frencuencia de vuelos según días", className="card-title")),
                    (dcc.Graph(id="season-graph4"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-6 col-sm-12 mb-3 mu-1")
                ],
            className="p-4"
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Destinos más frecuentes", className="card-title")),
                    (dcc.Graph(id="season-graph5"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-12 col-sm-12 mb-3 ml-3"        )]),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Distribucion de Estados de vuelos en ", className="card-title",id="card-title6")),
                    (dcc.Graph(id="season-graph6"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-4 col-sm-12 mb-3 mu-1"),
                dbc.Col(dbc.Card(dbc.CardBody([
                    (html.H5("Nacionalidades más frecuentes que vuelan a", className="card-title",id="card-title7")),
                    (dcc.Graph(id="season-graph7"))
                    ]),style=CARD_STYLE
                                 ), className="col-md-8 col-sm-12 mb-3 mu-1")
                ],
            className="p-4"
        ),


    ])


# Layout principal
app.layout = html.Div(
    [   dcc.Store(id='side_click'),
        #dcc.Store(id='window-size'),
        html.Div(id="display"),
        WindowBreakpoints(
                    id="breakpoints",
                    # Define the breakpoint thresholds
                    widthBreakpointThresholdsPx=[800, 1200],
                    # And their name, note that there is one more name than breakpoint thresholds
                    widthBreakpointNames=["sm", "md", "lg"],
                    ),
                navbar,
        sidebar,
        # Agrega el header
        header,
        html.Div(
            #   [
            [graficos]
            #  ],
          ,id="page-content",
        style=PAGE_STYLE  # Añade el estilo del contenido principal
        ),

        ]
,style={'backgroundColor':  "#343434"})

# Callbacks para actualizar los gráficos

@app.callback(
    [Output('season-graph6', 'figure'),Output('season-graph7', 'figure'),Output('card-title6', 'children'),Output('card-title7', 'children')],
    [Input ('season-graph5', 'clickData')]
)

def map_click(clickData):
    if clickData is None:
        selected_country="Argentina"
    if clickData is not None:
        selected_country = clickData["points"][0]["location"]


    country_data = filtered_data[filtered_data['Pais'] == selected_country]
    colors = ["gold", "mediumturquoise", "darkorange", "lightgreen"]
    fig = go.Figure(
       data=[
       go.Pie(
           labels=country_data['Estado del Vuelo'].unique(),
            hole=0.5,
            values=country_data['Estado del Vuelo'].value_counts(),
            marker=dict(colors=colors)
       )
       ]
    )

    fig2=px.treemap(country_data , path=[px.Constant("Pais"), 'Nacionalidad','Genero'])
    fig.update_layout(style_graficos)
    fig2.update_layout(style_graficos)
    title=f"Estados de los vuelos en {selected_country}"
    title2=f"Nacionalidades más frecuentes que vuelan a {selected_country}"
    return fig,fig2,title,title2

@app.callback(
    [Output("season-graph1", "figure"), Output("season-graph2", "figure"), Output("season-graph3", "figure"), Output("season-graph4", "figure"),Output("season-graph5", "figure")],
    [Input(f"season-checkbox-{season}", "value") for season in seasons]
)




def update_graph(*selected_season_values):
    global filtered_data

        # Reset selected_season if no checkboxes are selected
    selected_seasons = [season for season, value in zip(seasons, selected_season_values) if value]
    if not selected_seasons:
            # If no season is selected, return an empty figure for all graphs
        empty_fig = px.bar()
        empty_fig.update_layout(style_graficos)
        return [empty_fig] * 5


        # Filter data based on the selected season
    filtered_data = df[df['Estacion'].isin(selected_seasons)]

        # Create figures for each graph
    edades=filtered_data.groupby(["Edad","Genero"])['Genero'].size().unstack(fill_value=0).reset_index()
    edades['Edad']=pd.cut(df['Edad'], bins=bins, labels=labels, right=False)
    edades=edades.groupby("Edad")[['Femenino','Masculino']].sum().reset_index()
    colors = ["gold", "mediumturquoise", "darkorange", "lightgreen"]
    masculino_values = edades['Masculino'].values
    femenino_values = edades['Femenino'].values
    max_value = max(masculino_values.max(), femenino_values.max())
    range_limit = int(max_value * 1.1)  # Un 10% más del valor máximo para dar espacio

    # Calcular los valores de las marcas (tickvals)
    tick_step = range_limit // 4
    positive_ticks = list(range(0, range_limit + tick_step, tick_step))
    negative_ticks = [-val for val in positive_ticks if val != 0]
    tickvals = negative_ticks[::-1] + positive_ticks
    ticktext = [abs(val) if val < 0 else val for val in tickvals]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=-edades['Masculino'].values,
                         y=edades['Edad'],
                           orientation='h',
                           name='Masculino',
                           customdata=edades['Masculino'],
                           marker=dict(color='lightgreen'),
                           hovertemplate='Edad: %{y} <br>Valor: %{customdata}'
                           ))
    fig1.add_trace(go.Bar(x= edades['Femenino'],
                         y =edades['Edad'],
                           orientation='h',
                           name='Femenino',
                           marker=dict(color='mediumturquoise')
                           ))

    fig1.update_layout(barmode='relative',
                    yaxis_autorange='reversed',
                     bargap=0.01,
                     legend_orientation ='h',
                     legend_x=-0.05, legend_y=1.1,
                     xaxis=dict(
                         range=[-range_limit, range_limit],
                         tickvals=tickvals,
                         ticktext=ticktext,

                     )

                     )

    #fig1.update_traces(marker=dict(colors=colors))
    fig1.update_layout(style_graficos)
    #fig1.update_xaxes

    fig2 = go.Figure(
       data=[
       go.Pie(
           labels=filtered_data['Estado del Vuelo'].unique(),
            hole=0.5,
            values=filtered_data['Estado del Vuelo'].value_counts(),
            marker=dict(colors=colors)
       )
   ]
)
    fig2.update_layout(style_graficos)
    vuelos_continente =filtered_data.pivot_table(index='Continente del Aeropuerto', columns='Estado del Vuelo', aggfunc='size', fill_value=0).reset_index()
    fig3 = px.bar(vuelos_continente, x='Continente del Aeropuerto', y=['A tiempo','Cancelado','Demorado'],barmode='stack',color_discrete_sequence=colors)
    fig3.update_layout(style_graficos)
    fig3.update_layout(font=dict(color='yellow'))
    dias_viajes = filtered_data.groupby('Dia')['ID Pasajero'].size().reset_index(name='Cantidad')
    dias_semana = {0: 'L', 1: 'Ma', 2: 'Mi', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
    dias_viajes['Dia'] = dias_viajes['Dia'].map(dias_semana)

    # Crear el gráfico de barras
    fig4 = px.bar(dias_viajes, x="Dia", y="Cantidad", orientation='v', color_discrete_sequence=['orange'])

    # Añadir la línea curva de distribución
    fig4.add_trace(go.Scatter(x=dias_viajes['Dia'], y=dias_viajes['Cantidad'], mode='lines+markers', name='Distribución', line=dict(shape='spline', color='blue')))
    fig4.update_layout(style_graficos)



    pivot_df =filtered_data.pivot_table(index='Pais', columns=['Estado del Vuelo'], aggfunc='size', fill_value=0).reset_index()

    pivot_df['Total Vuelos'] = pivot_df['Cancelado'] + pivot_df['A tiempo'] + pivot_df['Demorado']
    pivot_df = pivot_df.assign(cantidad=pivot_df.apply(set_cat, axis=1))
    fig5 = px.choropleth(
    pivot_df,
    locations="Pais",
    locationmode='country names',

    color="cantidad",
    color_discrete_map={
                          '0': '#fffcfc',
                          '1 - 100' : "#92c5de",
                           '101 - 1000' : "#506FBE",
                            '1001 - 2000' : "#F1CD6B",
                            '2001 - 5000' : "#fddbc7",
                            '5001 - 10.000' :  "#ef8a62",
                            '10000 y mas' : "#b2182b"},
                        category_orders={
                          'cantidad' : [
                              '0',
                              '1 - 100'
                              '101 - 1000'
                              '1001 - 2000'
                              '2001 - 5000'
                              '5001 - 10.000'
                              '10000 y mas'

                          ]
                              }    ,
    scope="world",
    title="Click en país para ver detalles",
    hover_name="Pais",
    hover_data={
        "cantidad": False,
        "A tiempo":True,
        "Cancelado": True,
        "Demorado":True,
        "Total Vuelos": True,

    },
    projection='winkel tripel',

    )


    fig5.update_layout(style_graficos)
    fig5.update_layout(geo_bgcolor="#6a6e73")
    fig5.update_coloraxes(colorbar_orientation="h")
    fig5.update_coloraxes(colorbar_title_side="bottom")
    fig5.update_coloraxes(colorbar_ticklabelposition="outside bottom")
    fig5.update_coloraxes(
    colorbar_orientation="h",
    colorbar_title_side="bottom",
    colorbar_ticklabelposition="outside bottom",
    colorbar_yanchor="bottom",
    colorbar_x=0.5,
    colorbar_xanchor="center",
    colorbar_y=-0.2  # Ajusta esta cifra según sea necesario para mover la barra más abajo
    )
    fig5.update_layout(coloraxis_colorbar_y=-0.3)


    fig5.update_geos(
         visible=True,
        showcountries=True,
        showland=True,
        showocean=True,
        oceancolor="LightBlue",
        lakecolor="LightBlue",
    )


    #fig5 = px.line(status_category, x='Fecha de Salida', y=status_category.columns[1:], title='Flight Status Over Time')



    return fig1, fig2, fig3, fig4,fig5

# Callbacks para actualizar las tarjetas con la estación seleccionada
@app.callback(
    [Output("tarjeta1", "children"), Output("tarjeta2", "children"), Output("tarjeta3", "children"),Output("tarjeta4", "children")],
    [Input(f"season-checkbox-{season}", "value") for season in seasons]

)

def update_output_div(*selected_season_values):
    selected_seasons = [season for season, value in zip(seasons, selected_season_values) if value]
    if not selected_seasons:
        return ["No hay estaciones seleccionadas" for _ in range(4)]
    else:
        filtered_data = df[df['Estacion'].isin(selected_seasons)]
        cantidad_total=len(filtered_data)
        tarjeta1=f'{round(cantidad_total/ 1000, 2)} mil'
        tarjeta2 = f'{round(len(filtered_data[filtered_data["Genero"] == "Masculino"]) / 1000, 2)} mil'
        tarjeta3 = f'{round(len(filtered_data[filtered_data["Genero"] == "Femenino"]) / 1000, 2)} mil'
        tarjeta4 = f'{round(len(filtered_data["Aeropuerto de Llegada"].unique()) / 1000, 2)} mil'
        return tarjeta1,tarjeta2,tarjeta3,tarjeta4

# Inicializar la aplicación



# Inicializar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
