import streamlit as st
import pandas as pd
from datetime import datetime
import requests



dates = datetime.today().strftime('%m-%d')

df = pd.read_csv('./data/Ghy_avg_temp_51yrs_mma - avg.csv')
hist_data = df.set_index("datetime")

def mod_data(df, date, type):
    
    data = df.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Average Temperature (C)"}
        )
    data = data.rename(columns={"index": "Year"})
    data.replace(date,type, inplace=True )
        
    return data

data = hist_data.loc[dates]


st.write("""
# Guwahati is getting HOT, right? :hot_face: 

This app lets you guess how much hotter it is today compared to average temperature for 58 years!!! Data obtained from the [IMD](https://imdlib.readthedocs.io/en/latest/).
""")

st.sidebar.header('Guess today\'s temperature ')


data = data.T.reset_index()
data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Average Temperature (C)"}
        )

average_temp = round(data.head(50)['Average Temperature (C)'].mean(),2)

def get_current_temperature():
    url = f"https://api.open-meteo.com/v1/forecast?latitude=26.1844&longitude=91.7458&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_temp_min = data['daily']['temperature_2m_min'][0]
        current_temp_max = data['daily']['temperature_2m_max'][0]
        current_average = (current_temp_min + current_temp_max)/2
        return round(current_average, 1)

today_temp = get_current_temperature()


def compare_temp():
    
    input_deviation = input_df.at[0,'Deviation']
    deviation_real = today_temp - average_temp 
    difference = round(input_deviation - deviation_real,1)
    return difference


def user_input_features():
    with st.form("new form"):
        with st.sidebar:
            deviation_C = st.slider('Deviation in degree C from average', -10.0,10.0,0.1)
            
            submitted = st.form_submit_button("Submit")
            
    if submitted:
        data1 = {'Deviation': deviation_C }
    else:
        data1= {}
    features = pd.DataFrame(data1, index=[0])
    return features

input_df = user_input_features()



if input_df.empty:
    st.subheader('Prediction Probability')
    st.write(f"Today's average temperature is {today_temp}\N{DEGREE SIGN}C. How much hotter is today compared to the average of all these past years?")
    st.write("Make a guess in the sidebar!!")
else:
    st.subheader('Prediction Probability')
    if round(today_temp - average_temp,1) >0:
        st. write(f"Average temperature for today is {average_temp}\N{DEGREE SIGN}C which varies from today's temperature of {today_temp}\N{DEGREE SIGN}C by :red[{round(today_temp - average_temp,1)} \N{DEGREE SIGN}C]")
    elif round(today_temp - average_temp,1) <0:
        st. write(f"Average temperature for today is {average_temp}\N{DEGREE SIGN}C which varies from today's temperature of {today_temp}\N{DEGREE SIGN}C by :blue[{round(today_temp - average_temp,1)} \N{DEGREE SIGN}C]")
    else:
        st. write(f"Average temperature for today is {average_temp}\N{DEGREE SIGN}C which varies from today's temperature of {today_temp}\N{DEGREE SIGN}C by {round(today_temp - average_temp,1)} \N{DEGREE SIGN}C")

    
    diff = compare_temp()
    if diff < 0:
        st.write(f""":blue[Your Prediction was lower by {diff} \N{DEGREE SIGN}C ]""")
                 
        st.write( f"""  :blue[Spending too much time visiting Shillong?] :cold_face: :cold_face:""")
    elif diff > 0:
        st.write(f""":red[Your Prediction was higher by {diff} \N{DEGREE SIGN}C] """)
                 
        st.write( f""" :red[Relax dude, We'll get that hot in time, just not today!]  :hot_face: :hot_face:""")
    else :
        st.write(f""":green[Your Prediction was accurate] """)
                 
        st.write( f""":green[Guess you are an old timer !!!] :sunglasses: :sunglasses: """)
        

st.write(f"The following graph shows the variation in daily average temperature for Today ({dates})")
st.line_chart(data=data, 
              x="year", y="Average Temperature (C)", x_label="Year", y_label="Average Temperature (C)", 
                use_container_width=True)



