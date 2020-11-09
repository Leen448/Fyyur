from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SelectField,
                     SelectMultipleField, 
                     DateTimeField,
                     BooleanField)
from wtforms.validators import DataRequired, AnyOf, URL ,Length
from enum import Enum, auto
from wtforms.widgets import TextArea

def anyof_multiple_field(values_list):
  message ='Invalid value, must be one of: {0}.'.format( 
           ','.join(values_list))

  def _validate(form, field):
    error = False
    for value in field.data:
      if value not in values:
        error = True

    if error:
      raise ValidationError(message)

  return _validate

class Genre(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    Hip_Hop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    R_AND_B = 'R&B'
    Reggae = 'Reggae'
    Rock_n_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'    

    @classmethod
    def choices(choice_list):
       return [ (choice.value, choice.value) for choice in choice_list ]

class ShowForm(FlaskForm):
    artist_id = StringField('artist_id',validators=[DataRequired()])
    venue_id  = StringField('venue_id',validators=[DataRequired()])
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    
    state_choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]

    name = StringField('name', validators=[DataRequired()] )
    city = StringField(
           'city',validators=[DataRequired(),Length(min=5, max=120)])
    
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf(state_choices)],
         choices=[(state) for state in state_choices],
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired(),Length(min=10, max=16)]
    )
    image_link = StringField(
        'image_link', validators=[URL(),Length(min=5, max=500)]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(),
         anyof_multiple_field( [ choice.value for choice in Genre ] )],
         choices=Genre.choices()
    )   
    facebook_link = StringField(
       'facebook_link', validators=[URL(),Length(min=5, max=120)]
    ) 
    website = StringField(
        # TODO implement enum restriction
        'website', validators=[URL(),Length(min=5, max=120)]
    )
    seeking_talent = BooleanField(
        'seeking_talent',default=False, validators=[AnyOf([True, False])])
    
    seeking_description = StringField(
        'seeking_description', widget=TextArea())

class ArtistForm(FlaskForm):
    state_choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
   
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired(),Length(min=5, max=120)] 
    )
   
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf(state_choices)],
         choices=[(state) for state in state_choices],
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired(),Length(min=10, max=16)]
    )
    image_link = StringField(
        'image_link', validators=[URL(),Length(min=5, max=500)]
    )
    
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(),
         anyof_multiple_field( [ choice.value for choice in Genre ] )],
         choices=Genre.choices()
    ) 
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL(),Length(min=5, max=120)]
    )
    website = StringField(
        # TODO implement enum restriction
        'website', validators=[URL(),Length(min=5, max=120)]
    )
    seeking_venue =  BooleanField(
        'seeking_venue',default=False, validators=[AnyOf([True, False])])
    
    seeking_description = StringField(
        'seeking_description', widget=TextArea())

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
