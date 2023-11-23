import secrets
import os
from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarPost, \
    FormExcluirPost, FormConversaoUnidade
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
from datetime import datetime

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts, datetime=datetime)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('E-mail ou senha incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript
        )
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email.data}', 'alert-success')
        login_user(usuario, remember=form_criarconta.lembrar_dados.data)
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/usuarios')
@login_required
def usuarios():
    users = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=users)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    profile_photo = url_for('static', filename=f'/profile_images/{current_user.foto_perfil}')
    posts = Post.query.filter_by(id_autor=current_user.id).order_by(Post.id.desc())

    return render_template('perfil.html', profile_photo=profile_photo, posts=posts, datetime=datetime)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)

    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path,'static/profile_images/',nome_arquivo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ";".join(lista_cursos)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_photo.data:
            nome_imagem = salvar_imagem(form.profile_photo.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        for curso in current_user.cursos.split(";"):
            for campo in form:
                if curso in campo.label.text:
                    campo.data = True

    profile_photo = url_for('static', filename=f'/profile_images/{current_user.foto_perfil}')
    posts = Post.query.filter_by(id_autor=current_user.id)
    return render_template('editar_perfil.html', profile_photo=profile_photo, form=form, posts=posts, datetime=datetime)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autorPost=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criar_post.html', form=form)


@app.route('/perfil/editar_post/<post_id>', methods=['GET', 'POST'])
def exibir_post(post_id):
    posts = Post.query.filter_by(id_autor=current_user.id).order_by(Post.id.desc())
    post = Post.query.get(post_id)
    form = FormEditarPost()
    if request.method == 'GET':
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
    elif request.method == 'POST':
        if 'botao_submit_cancelaredicao' in request.form:
            return redirect(url_for('perfil'))
        elif 'botao_submit_confirmaredicao' in request.form:
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            post.editado = 1
            post.data_criacao = datetime.now()
            database.session.commit()
            flash('Post editado com sucesso!', 'alert-success')
            return redirect(url_for('perfil'))

    profile_photo = url_for('static', filename=f'/profile_images/{current_user.foto_perfil}')
    return render_template('editarpost.html',  datetime=datetime, form=form, posts=posts, post=post, post_id=int(post_id), profile_photo=profile_photo)

@app.route('/perfil/excluir_post/<post_id>', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    posts = Post.query.filter_by(id_autor=current_user.id).order_by(Post.id.desc())
    post = Post.query.get(post_id)
    profile_photo = url_for('static', filename=f'/profile_images/{current_user.foto_perfil}')
    form = FormExcluirPost()
    if request.method == 'POST' and 'botao_submit_confirmarexclusao' in request.form:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif 'botao_submit_cancelarexclusao' in request.form:
        return redirect(url_for('perfil'))
    return render_template('excluir_post.html',  datetime=datetime, form=form, posts=posts, post=post, post_id=int(post_id), profile_photo=profile_photo)

@app.route('/conversor_unidades', methods=['GET', 'POST'])
@login_required
def conversor_unidades():
    form = FormConversaoUnidade()
    return render_template('conversor_unidades.html', form=form)