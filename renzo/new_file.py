from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
# import pathlib
# import shutil
# from bs4 import BeautifulSoup
from run_query_f import run_query
import ssl
import streamlit as st

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(page_title='Topics Evolution in UN Speeches', layout='centered')
st.title('Topics Evolution in UN Speeches')
st.header('How have our priorities changed over time?')
def inject_matamo():
    matamo_id = "matamo"
    matamo_js = """<script>
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://vizzuhq.matomo.cloud/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '3']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src='//cdn.matomo.cloud/vizzuhq.matomo.cloud/matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>"""

#     index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
#     soup = BeautifulSoup(index_path.read_text(), 'lxml')
#     if not soup.find(id=matamo_id):  # if cannot find tag
#         bck_index = index_path.with_suffix('.bck')
#         if bck_index.exists():
#             shutil.copy(bck_index, index_path)  # recover from backup
#         else:
#             shutil.copy(index_path, bck_index)  # keep a backup
#         html = str(soup)
#         new_html = html.replace('<head>', '<head>\n' + matamo_js)
#         index_path.write_text(new_html)

# inject_matamo()

width=750
height=450


# data = run_query()


# df = pd.read_csv('/home/ricorenzo/code/renzorico/speeches-at-UN/raw_data/data_st.csv')

query_new = f'''SELECT year , topic, COUNT(country) as count FROM `lewagon-bootcamp-384011.production_dataset.speeches`
GROUP BY year, topic
ORDER BY year ASC '''

df = pd.DataFrame(run_query(query_new))
st.dataframe(df)
#@title Create the story
topics = df['topic'].unique()
sel_topic = st.selectbox(
    'Select topic:',
    list(topics))
skip_intro = st.checkbox(
    'Skip intro slides', value=False
)

df_topic = df[df['topic'] == sel_topic]

# initialize chart
data = Data()
data.add_data_frame(df)
# pop_max = int(df_topic[df_topic['year'] == 'Population'][['Medium','High','Low']].max().T.max()*1.1)

# df_future = df_topic[df_topic['Period'] == 'Future']

# df_futureCategories = df_future[df_future['year']!='Population'][['year','Medium','High','Low']]

# df_future_sum = df_futureCategories.groupby('year').sum().T

# other_max = df_future_sum.max().max() * 1.1
# other_min = df_future_sum.max().max() * -1.1

topic_palette = ['#001219','#005F73','#0A9396','#94D2BD','#E9D8A6','#EE9B00','#CA6702', '#BB3E03','#AE2012','#9B2226','#606C38', '#FEFAE0','#FFAFCC','#8650A5']
topic_palette_str = ' '.join(topic_palette)

topic_color = topic_palette[list(topics).index(sel_topic)]

year_palette = ['#FF8080FF', '#808080FF', topic_color.replace('FF','20'), '#60A0FFFF', '#80A080FF']
year_palette_str = ' '.join(year_palette)

# Define the style of the charts in the story
style = {
        'legend' : {'width' : '13em'},
        'plot': {
            'yAxis': {
                'label': {
                    'fontSize': '1em',
                    'numberFormat' : 'prefixed',
                    'numberScale':'shortScaleSymbolUS'
                },
                'title': {'color': '#ffffff00'},
            },
            'marker' :{
                'label' :{
                    'numberFormat' : 'prefixed',
                    'maxFractionDigits' : '1',
                    'numberScale':'shortScaleSymbolUS',
                }
            },
            'xAxis': {
                'label': {
                    'angle': '2.5',
                    'fontSize': '1em',
                    'paddingRight': '0em',
                    'paddingTop': '1em',
                    'numberFormat' : 'grouped',
                },
                'title': {'color': '#ffffff00'},
            },
        },
    }

story = Story(data=data)
story.set_size(width, height)

# Add the first slide, containing a single animation step
# that sets the initial chart.

if skip_intro:
    style['plot']['marker']['colorPalette'] = topic_palette_str
else:
    slide1 = Slide(
        Step(
            df_topic,
            Config(
                {
                    'x':'topic',
                    'y': 'count',
                    'label': 'count',
                    'title': 'Topics over time',
                }
            ),
            Style(style)
        )
    )
    # Add the slide to the story
    story.add_slide(slide1)

    # Show components side-by-side
    slide2 = Slide(
        Step(
            Config(
                {
                    'y': ['Medium','topic'],
                    'color': 'topic',
                    'label': None,
                    'title': 'The Population of regions 1950-2020',
                }
            ),
            Style({ 'plot.marker.colorPalette': topic_palette_str })
        )
    )
    story.add_slide(slide2)

    # Show components side-by-side
    slide3 = Slide()
    slide3.add_step(
        Step(
            Data.filter("record.year === 'Population'"),
            Config(
                {
                    'y': ['Medium','topic'],
                    'color': 'topic',
            #     'lightness': 'Period',
            #     'x': ['Year','Period'],
                    'title': 'The Population of topics 1950-2100',
                }
            )
    ))

    slide3.add_step(
        Step(
            Config(
                {
                'geometry':'area'
                }
            )
    ))

    story.add_slide(slide3)

    slide4 = Slide(
        Step(
            Config(
                {
                    'split': True
                },
            ),
            Style({'plot' : {'yAxis' :{ 'label' :{ 'color' : '#99999900'}}}})
        )
    )
    story.add_slide(slide4)

    slide5 = Slide(
        Step(
            Config.percentageArea(
                {
                    'x':'Year',
                    'y':'Medium',
                    'stackedBy':'topic',
                    'title': 'The Population of topics 1950-2100 (%)'
                }
            ),
            Style({'plot' : {'yAxis' :{ 'label' :{ 'color' : '#999999FF'}}}})
        )
    )
    story.add_slide(slide5)


# slide6 = Slide()
# slide6.add_step(
#     Step(
#         Config.stackedArea(
#             {
#                 'x':'Year',
#                 'y':'Medium',
#                 'stackedBy':'topic',
#             }
#         ),
#      Style(style) #,{'plot.marker.colorPalette': topic_palette_str}
# ))

# slide6.add_step(
#     Step(
#         Data.filter(f'record.year === "Population" && record.topic === "{sel_topic}"'),
#         Config({
#                 'title': 'The Population of '+sel_topic+' 1950-2100',
#                 'channels':{'y':{
#                     'range':{'max':pop_max}
#                 }}
#         }),
#     ))

# story.add_slide(slide6)

# slide7 = Slide(
#     Step(
#         Config(
#             {
#                 'y':'High',
#                 'title': 'High prediction for '+sel_topic
#             }
#         )
#     )
# )
# story.add_slide(slide7)

# slide8 = Slide(
#     Step(
#         Config(
#             {
#                 'y':'Low',
#                 'title': 'Low prediction for '+sel_topic
#             }
#         )
#     )
# )
# story.add_slide(slide8)

# slide9 = Slide(
#     Step(
#         Config(
#             {
#                 'y':'Medium',
#                 'title': 'Medium prediction for '+sel_topic
#             }
#         )
#     )
# )
# story.add_slide(slide9)

# slide10 = Slide()

# slide10.add_step(
#     Step(
#         Config({
# 			'y':['Medium','year'],
# 			'title': 'Adding Sources of Gain and Loss to the Mix '
#         }),
#     )
# )

# slide10.add_step(
#     Step(
#         Data.filter(f'record.topic === "{sel_topic}" && (record.year === "Population" || record.year === "Migration+" || record.year === "Births")'),
#         Config(
#             {
#                 'color': ['year']
#             }),
#         Style({ 'plot.marker.colorPalette': year_palette_str })
#     )
# )

# slide10.add_step(
#     Step(
#         Data.filter(f'record.topic === "{sel_topic}"'),
#     )
# )
# story.add_slide(slide10)

# slide11 = Slide()

# slide11.add_step(
#     Step(
#         Config(
#             {
#                 'geometry':'rectangle',
#             }
#         )
#     )
# )

# slide11.add_step(
#     Step(
#         Data.filter(f'record.Period === "Future" && record.topic === "{sel_topic}"'),
#         Config(
#             {
#                 'title': 'Zoom to the future'
#             }
#         )
#     )
# )

# slide11.add_step(
#     Step(
#         Data.filter(f'record.Period === "Future" && record.topic === "{sel_topic}" && record.year !== "Population"'),
#         Config(
#             {
#                 'channels':{
#                     'x':{'set':['Medium','Year'],'range':{'max':other_max,'min':other_min}},
#                     'y':{'set': 'year', 'range':{'max':'auto'}},
#                 },
#                 'title': 'Sources of Population Gain and Loss - Medium Scenario'
#             },
#         ),
#         Style({'plot' : {'marker' :{ 'label' :{ 'maxFractionDigits' : '1'}}}})

#     )
# )

# slide11.add_step(
#     Step(
#         Config(
#             {
#                 'x':'Medium',
#                 'label':'Medium',
#             }
#         )
#     )
# )


# story.add_slide(slide11)

# slide12 = Slide(
#     Step(
#         Config(
#             {
#                 'x':'High',
#                 'label': 'High',
#                 'title': 'Sources of Population Gain and Loss - High Scenario'
#             }
#         )
#     )
# )
# story.add_slide(slide12)

# slide13 = Slide(
#     Step(
#         Config(
#             {
#                 'x':'Low',
#                 'label': 'Low',
#                 'title': 'Sources of Population Gain and Loss - Low Scenario'
#             }
#         )
#     )
# )
# story.add_slide(slide13)

# Switch on the tooltip that appears when the user hovers the mouse over a chart element.
story.set_feature('tooltip', True)

html(story._repr_html_(), width=width, height=height)

# st.download_button('Download HTML export', story.to_html(), file_name=f'world-population-story-{sel_topic}.html', mime='text/html')

st.header('Thanks for using the app! :heart_eyes:')
# col1, col2 = st.columns(2)
# with col1:
# 	st.markdown('If you want to learn more about how it works, check out this [blog post](https://blog.streamlit.io/create-an-animated-data-story-with-ipyvizzu-and-streamlit/) on creating animated data stories with ipyvizzu and Streamlit. :chart_with_upwards_trend::film_frames::balloon:')
# 	st.markdown('You can find the code for the app on this \n [GitHub repo](https://github.com/vizzu-streamlit/world-population-story)')
# 	st.markdown('Visit our [homepage](https://vizzuhq.com) to learn more about our open-source charting and data storytelling tools.')
# with col2:
# 	st.markdown('![homepage [homepage](https://vizzuhq.com)](https://github.com/vizzuhq/vizzu-lib-doc/raw/main/docs/readme/infinite-60.gif)')
