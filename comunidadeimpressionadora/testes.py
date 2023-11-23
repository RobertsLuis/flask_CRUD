from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario, Post

# with app.app_context():
#     database.drop_all()


with app.app_context():
    posts = Post.query.all()
    usuarios = Usuario.query.all()
    for post in posts:
        print(post.corpo)
        print(post.editado)

# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     for i,usuario in enumerate(meus_usuarios):
#         print("")
#         print(f"Usuário {i+1}: ")
#         print(f"ID: {usuario.id}")
#         print(f"Nome: {usuario.username}")
#         print(f"E-mail: {usuario.email}")
#         print(f"Senha: {usuario.senha}")
#     #query filtering
#     usuario_teste = Usuario.query.filter_by(email='bejr2002@gmail.com').first() #se usar o all da merda na consulta de atributos
#     print(usuario_teste)
#     print(usuario_teste.username)


# with app.app_context(): #CREATING POSTS
#     post1 = Post(titulo='Testando Parte 2', corpo='Agora é o Lira postando', id_autor=2)
#     database.session.add(post1)
#     database.session.commit()


# with app.app_context(): #CONSULTING POSTS
#     posts = Post.query.all()
#     for post in posts:
#         print('')
#         print(post.corpo)
#         print(post.autorPost.username)


# with app.app_context():
#     database.drop_all()
#     database.create_all()