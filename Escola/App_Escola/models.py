from django.db import models

# Create your models here.
#classe professor (dentro do parametro herdando da classe model)
class Professor(models.Model):

    nome = models.CharField(max_length=120)#defini o tamanho do campo
    email = models.CharField(max_length=120)#defini o tamanho do campo
    senha = models.CharField(max_length=64)#defini o tamanho do campo

    #representação de string do objeto Professor, então vai retorna o nome do professor
    def __str__(self):
        return self.nome

#classe Turma (dentro do parametro herdando da classe model)
class Turma(models.Model):
    nome_turma = models.CharField(max_length=120)#definindo o tamanho do campo
    #ForeignKey: estabelece relações de chave estrangeira com outro models
    id_professor = models.ForeignKey(Professor, null=True, on_delete=models.PROTECT)
    def __str__(self):
        return self.nome_turma

class Atividade(models.Model):
    nome_atividade = models.CharField(max_length=120)
    id_turma = models.ForeignKey(Turma, null=True, on_delete=models.PROTECT)
    arquivo = models.FileField(upload_to='atividade_arquivos', blank=True, null=True)
    def __str__(self):
        return self.nome_atividade