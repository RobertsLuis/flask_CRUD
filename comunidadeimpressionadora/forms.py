from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired(), Length(3, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirmacao = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('senha')])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_criar_conta = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado!')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired(), Length(3, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_photo = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png', 'webm'])])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    curso_excel = BooleanField('Excel Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_phyton = BooleanField('Phyton Impressionador')
    curso_ppt = BooleanField('PowerPoint Impressionador')
    curso_sql = BooleanField('SQL Impressionador')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este e-mail cadastrado!')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(1, 140)])
    corpo = TextAreaField('Conteúdo', validators=[DataRequired()])
    botao_submit_criarpost = SubmitField('Criar Post')

class FormEditarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(1, 140)])
    corpo = TextAreaField('Conteúdo', validators=[DataRequired()])
    botao_submit_confirmaredicao = SubmitField('Confirmar edição')
    botao_submit_cancelaredicao = SubmitField('Cancelar edição')

class FormExcluirPost(FlaskForm):
    botao_submit_confirmarexclusao = SubmitField('Excluir Post')
    botao_submit_cancelarexclusao = SubmitField('Cancelar Exclusão')

class FormConversaoUnidade(FlaskForm):
    unidade1 = StringField('De', validators=[DataRequired()])
    unidade2 = StringField('Para', validators=[DataRequired()])
    valor = DecimalField('Valor', validators=[DataRequired()])
    resultado = StringField('Resultado', validators=[DataRequired()])
