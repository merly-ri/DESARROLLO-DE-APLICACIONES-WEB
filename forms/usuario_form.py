from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class UsuarioForm(FlaskForm):
    usuario = StringField(
        "Usuario",
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=4, max=100)]
    )
    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Registrar usuario")