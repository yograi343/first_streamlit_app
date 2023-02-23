import streamlit
import snowflake.connector
import pandas
import requests

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smotthie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#let's put a pick list here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
      fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)
      streamlit.write('The user entered',fruit_choice)
except URLEroor as e:
  streamlit.error()


#don't run anything past here while we trobleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The Fruit load list contains")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit you like to add?')
streamlit.write('Thanks for adding',add_my_fruit)

#This will not work corrrectly but just go with with it for now
my_cur.excecute("insert into fruit_load_list values ('from streamlit')")
