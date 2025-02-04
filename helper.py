#utility stuff
import os, sys
this_dir = os.path.abspath('.')
sys.path.append(this_dir)
import app
housing_data_frame = app.read_data('Housing.csv')
age_house = app.DisplayData(housing_data_frame['AGE'])
bed_house = app.DisplayData(housing_data_frame['BEDRMS'])
built_house = app.DisplayData(housing_data_frame['BUILT'])
room_house = app.DisplayData(housing_data_frame['ROOMS'])
utility_house = app.DisplayData(housing_data_frame['UTILITY'])

pop_data_frame = app.read_data('PopChange.csv')
apr_pop = app.DisplayData(housing_data_frame['Pop Apr 1'])
jul_pop = app.DisplayData(housing_data_frame['Pop Jul 1'])
chg_pop = app.DisplayData(housing_data_frame['Change Pop'])



data_choice = app.sub_menu('house_choice')
2
