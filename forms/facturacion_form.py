from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, IntegerField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import date


class FacturacionForm(FlaskForm):
    numero = StringField(
        "N.º Factura",
        validators=[DataRequired()]
    )

    cliente_id = SelectField(
        "Cliente",
        coerce=int,
        validators=[DataRequired()]
    )

    producto_id = SelectField(
        "Producto",
        coerce=int,
        validators=[DataRequired()]
    )

    fecha = DateField(
        "Fecha",
        default=date.today,
        validators=[DataRequired()]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    total = DecimalField(
        "Total",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar factura")