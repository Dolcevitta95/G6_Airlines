from sqlalchemy.orm import Session
import joblib
import pandas as pd

import model

with open('../model_pipeline.pkl', 'rb') as f:
    pipeline = joblib.load('../model_pipeline.pkl')

def ages():
	r_age = range(5, 101)[::5]
	dict_age = {}
	j = 0
	for i in r_age:
		key = f"{j}-{i}"
		value = range(j, i)
		dict_age[key] = value
		j = i
	return dict_age

def which_age(num):
	range_age = ages()
	# btw_age = (k for k, v in range_age.items() if num in v)
	# return btw_age
	for k, v in range_age.items():
		if num in v:
			return k


def post_data(db: Session, datax: model.FeatureSchema):

	x_dict = datax.model_dump()
	# new_data = model.Data(**datax.model_dump())
	# print(new_data)
	x_dict['Age Group'] = which_age(x_dict['age'])
	x_dict['arrival_dealy'] = float(x_dict['arrival_dealy'])
	df = pd.DataFrame([list(x_dict.values())], columns=['Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class',
       'Flight Distance', 'Inflight wifi service',
       'Departure/Arrival time convenient', 'Ease of Online booking',
       'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
       'Inflight entertainment', 'On-board service', 'Leg room service',
       'Baggage handling', 'Checkin service', 'Inflight service',
       'Cleanliness', 'Departure Delay in Minutes', 'Arrival Delay in Minutes',
       'Age Group'])
	df['Age Group'] = df['Age Group'].astype('category')
	if not df.empty:
		print(df.head())
		print(df.info())
		prediction = pipeline.predict(df)
		return(prediction)
	else:
		return({'Error': 'Empty df'})

def get_all_data(db: Session):
	pass