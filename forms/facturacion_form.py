from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    cliente = StringField('Cliente', validators=[DataRequired()])
    producto = StringField('Producto', validators=[DataRequired()])
    cantidad = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    total = FloatField('Total', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Generar factura')