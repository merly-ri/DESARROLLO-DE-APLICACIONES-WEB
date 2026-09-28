from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[DataRequired(), Length(min=2, max=100)]
    )

    contacto = StringField(
        "Contacto",
        validators=[DataRequired(), Length(min=7, max=15)]
    )

    correo = EmailField(
        "Correo electrónico",
        validators=[DataRequired(), Email()]
    )

    productos = StringField(
        "Productos",
        validators=[DataRequired(), Length(min=2, max=200)]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")