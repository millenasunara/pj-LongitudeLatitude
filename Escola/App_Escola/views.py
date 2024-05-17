from django.shortcuts import render, redirect, get_object_or_404
from hashlib import sha256
from django.db import models
from.models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.urls import reverse
import openpyxl
# Create your views here.
def initial_population():
  print("Vou Popular")
  cursor = connection.cursor()

  #Popular tabela do professor
  senha ="123456" #senha inicial para todos os usuarios
  senha_armazenar = sha256(senha.encode()).hexdigest()

  #intsruções sqls
  insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES "
  insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
  insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar + "'),"
  insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "')"

  cursor.execute(insert_sql_professor)
  transaction.atomic()

  #Popular Tabela Turma
  #instrucao sql para tbela turma
  insert_sql_turma = "INSERT INTO App_Escola_Turma (nome_turma, id_professor_id) VALUES"
  insert_sql_turma = insert_sql_turma + "('1° Semestre - Desenvolvimento de Sistemas',1),"
  insert_sql_turma = insert_sql_turma + "('2° Semestre - Desenvolvimento de Sistemas', 2),"
  insert_sql_turma = insert_sql_turma + "('4° Semestre - Desenvolvimento de Sistemas', 2),"
  insert_sql_turma = insert_sql_turma + "('3° Semestre - Desenvolvimento de Sistemas', 3)"

  cursor.execute(insert_sql_turma)
  transaction.atomic() #Necessario o commit para insert e update

  #Popular Tabela Atividade
  #instrucoes sql para tabela Atividade
  insert_sql_atividade = "INSERT INTO App_Escola_Atividade (nome_atividade, id_turma_id) VALUES"
  insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1),"
  insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
  insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork FASTAPI', 2),"
  insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projetos', 3)"

  cursor.execute(insert_sql_atividade)
  transaction.atomic()#Necessario o commit para insert e update
  #Fim TAbela Atividade

  print("Populei")
def abre_index(request):
    #return render(request, 'Index.html')
    # mensagem = "OLÁ, TURMA, MUITO BOM DIA!"
    #return HttpResponse(mensagem)

    # query set Tipos de Look Up
    # nome__exact='SS' - tem que ser exatamente igual
    # nome__contains='H' - contem o H maisculo
    # nome__icontains='H' - ignora se maisúculo ou minúsculo
    # nome__startswitch='M' - traz o que começa com a letra M ou sequencia de letras
    # nome__istartswitch='M' - traz o que começa com a letra M ignorando se maisculo ou minuscula u sequencia de letras
    # nome__endswitch='a' - traz o que termina com a letra 'a' minusculo ou sequencia de letras
    # nome__iendswitch='a' - traz o que termina com a letra a ignorando maiúscua ou minuscula
    # nome__in=['Michael', 'Obama']) traz somente os noem que estao na lista
    # Pode ser feito uma composição de 'and' utilizando, (vírgula entre os campos) ou 'or' utilizando | (pipe entre os campos)

    dado_pesquisa = 'Obama'

    verifica_populado = Professor.objects.filter(nome__icontains=dado_pesquisa)
    #verifica_populado = Professor.objects.flter(nome='Prof. Barak Obama')

    if len(verifica_populado) == 0:
      print("Não está populado")
      initial_population()
    else:
      print("Achei Obama", verifica_populado)

    usuario_logado = request.user.username
    return render(request,'index.html', {'usuario_logado': usuario_logado})
def enviar_login(request):
  if(request.method == 'POST'):
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha_criptografada = sha256(senha.encode()).hexdigest()
    dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
    print("Dados do Professor ", dados_professor)
    if dados_professor:
      senha = dados_professor[0]
      senha = senha['senha']
      usuario_logado = dados_professor[0]
      usuario_logado = usuario_logado['nome']
      if (senha == senha_criptografada):
        #se logou corretamente traz as turmas dos professores
        id_logado = dados_professor[0]
        id_logado = id_logado['id']
        turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
        print("Turmas do Professor ", turmas_do_professor)
        return render(request, 'Cons_Turmas_Lista.html', {'usuario_logado': usuario_logado,
                                                          'turmas_do_professor': turmas_do_professor,
                                                          'id_logado': id_logado})
      else:
        messages.info(request, 'Usuario ou senha incorretos. Tente Novamente.')
        return render(request, 'login.html')
    messages.info(request, "Olá " + email + ", seja bem-vindo! Percebemos que você é novo por aqui. Complete seu cadastro.")
    return render(request, 'cadastro.html', {'login': email})

def confirmar_cadastro(request):
  if(request.method == 'POST'):
    nome = request.POST.get('nome')
    email = request.POST.get('login')
    senha = request.POST.get('senha')
    senha_criptografada = sha256(senha.encode()).hexdigest()

    grava_professor = Professor(
      nome=nome,
      email=email,
      senha=senha_criptografada
    )
    grava_professor.save()

    mensagem = "OLÁ PROFESSOR " + nome + ", SEJA BEM VINDO"
    return HttpResponse(mensagem)

def cad_turma(request, id_professor):
  usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
  usuario_logado = usuario_logado[0]
  usuario_logado = usuario_logado['nome']
  return render(request, 'Cad_Turma.html', {'usuario_logado': usuario_logado, 'id_logado': id_professor})

def salvar_turma_nova(request):
  if(request.method == 'POST'):
    nome_turma = request.POST.get('nome_turma')
    id_professor = request.POST.get('id_professor')
    professor = Professor.objects.get(id=id_professor)
    gravar_turma = Turma(
      nome_turma=nome_turma,
      id_professor=professor
    )
    gravar_turma.save()
    messages.info(request, 'Turma' + nome_turma + ' cadastrado com sucesso.')

    #Redirecionar para uma nova URL após a gravação bem sucedida
    return redirect('lista_turma', id_professor=id_professor)

def lista_turma(request, id_professor):
  dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
  usuario_logado = dados_professor[0]
  usuario_logado = usuario_logado['nome']
  id_logado = dados_professor[0]
  id_logado = id_logado['id']
  turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
  return render(request, 'Cons_Turmas_Lista.html',
                {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor,
                 'id_logado': id_logado})


def excluir_turma(request, id_turma):
  turma = get_object_or_404(Turma, pk=id_turma)
  atividades_relacionadas = Atividade.objects.filter(id_turma=id_turma)
  for atividade in atividades_relacionadas:
    atividade.delete()
  turma.delete()
  messages.success(request, 'Turma e atividades relacionadas excluídas com sucesso.')
  return redirect('lista_turma', id_professor=turma.id_professor.id)


def ver_atividades(request, id_turma):
  # Obtenha todas as atividades associadas à turma com o ID fornecido
  atividades = Atividade.objects.filter(id_turma=id_turma)

  # Renderize o template com as atividades, passando também o id_turma
  return render(request, 'atividades.html', {'atividades': atividades, 'id_turma': id_turma})



def sair(request):
    return render(request, 'index.html')

def cadastrar_atividade(request, id_turma):
  print(">>>>>Entrei em cadastrar atividade")
  if request.method == 'POST':
    nome_atividade = request.POST.get('nome')
    arquivo = request.FILES.get('arquivo')
    print(arquivo)
    print(nome_atividade)
    turma = Turma.objects.get(id=id_turma)
    nova_atividade = Atividade(
        nome_atividade=nome_atividade,
        id_turma=turma,
        arquivo =arquivo)
    nova_atividade.save()
    print(">>>Gravei")
    messages.success(request, 'Atividade cadastrada com sucesso.')
    return redirect('ver_atividades', id_turma=id_turma)
  else:
    return HttpResponseNotAllowed(['POST'])

def logout(request):
    # Faça qualquer limpeza necessária aqui

    # Redirecione de volta para a página de login
    return redirect(reverse('enviar_login'))

def exportar_para_excel_turma(request):

    dados_turma = Turma.objects.all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Turmas"

    sheet['A1'] = "ID"
    sheet['B1'] = "Nome da Turma"

    for index, turma in enumerate(dados_turma, start=2):
      sheet[f'A{index}'] = turma.id
      sheet[f'B{index}'] = turma.nome_turma


    response = HttpResponse (content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=turma.xslx'
    workbook.save(response)
    return response

def exportar_para_excel_Atividades(request):

    dados_atividades = Atividade.objects.all()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Atividades"

    sheet['A1'] = "ID"
    sheet['B1'] = "Nome da Ativdade"
    sheet['C1'] = "Turma"

    for index, atividade in enumerate(dados_atividades, start=2):
      sheet[f'A{index}'] = atividade.id
      sheet[f'B{index}'] = atividade.nome_atividade
      sheet[f'C{index}'] = atividade.id_turma.nome_turma

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=atividades.xlsx'
    workbook.save(response)
    return response
