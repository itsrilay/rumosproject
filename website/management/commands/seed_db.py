from django.core.management.base import BaseCommand
from website.models import *
from datetime import date
import random

class Command(BaseCommand):
    help = 'Preenche a base de dados com dados de exemplo (categorias, produtos, perguntas, respostas e desafios)'

    def handle(self, *args, **kwargs):
        # Limpar dados antigos (opcional)
        Category.objects.all().delete()
        Product.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Challenge.objects.all().delete()

        # === Criar Categorias ===
        categories = [
            "Ervas",
            "Flores",
            "Suculentas",
            "Árvores",
            "Frutas",
            "Legumes"
        ]
        category_objs = []
        for name in categories:
            cat = Category.objects.create(name=name)
            category_objs.append(cat)

        # === Criar Produtos ===
        products = [
            {"name": "Óleo de Lavanda", "price": 12.99, "desc": "Óleo aromático extraído de lavanda.", "image": "https://images-na.ssl-images-amazon.com/images/I/51KFx9JV7GL._SL1000_.jpg"},
            {"name": "Sementes de Rosa", "price": 4.50, "desc": "Sementes de rosa de alta qualidade."},
            {"name": "Vaso com Cacto", "price": 9.99, "desc": "Cacto em vaso, ideal para decoração."},
            {"name": "Árvore Bonsai", "price": 29.99, "desc": "Árvore bonsai em miniatura para interior."},
            {"name": "Planta de Tomate", "price": 5.25, "desc": "Planta de tomate pronta para ser plantada."},
            {"name": "Folhas de Manjericão", "price": 3.75, "desc": "Folhas de manjericão frescas."},
            {"name": "Hortelã", "price": 3.25, "desc": "Planta de hortelã refrescante."},
            {"name": "Sementes de Girassol", "price": 2.99, "desc": "Sementes de girassol para plantar ou petiscar."},
            {"name": "Muda de Limoeiro", "price": 15.00, "desc": "Muda jovem de limoeiro."},
            {"name": "Gel de Aloé Vera", "price": 7.99, "desc": "Gel natural de aloé vera."},
        ]

        for p in products:
            Product.objects.create(
                name=p["name"],
                category=random.choice(category_objs),
                price=p["price"],
                description=p["desc"]
            )

        # === Criar utilizador de teste ===
        user, _ = User.objects.get_or_create(username="utilizador_teste")
        user.set_password("password123")
        user.save()

        # === Criar Perguntas e Respostas ===
        q1 = Question.objects.create(
            user=user,
            title="Como posso propagar suculentas?",
            body="Já ouvi dizer que é fácil, mas não sei bem por onde começar. Alguém tem dicas?",
        )
        q2 = Question.objects.create(
            user=user,
            title="Porque é que as folhas do meu manjericão estão a ficar castanhas?",
            body="Estavam bem na semana passada. Tenho regado com frequência.",
        )

        Answer.objects.create(
            user=user,
            question=q1,
            body="Corta uma folha saudável e coloca-a sobre terra seca. Deve criar raízes em uma ou duas semanas."
        )

        Answer.objects.create(
            user=user,
            question=q2,
            body="Pode ser excesso de água ou algum fungo. Reduz a rega e verifica se há pragas."
        )

        # === Criar Desafios ===
        Challenge.objects.create(
            text="Que parte da planta é responsável pela fotossíntese?",
            correct_answer="Folhas",
            date=date.today()
        )

        Challenge.objects.create(
            text="Como se chama uma planta que completa o ciclo de vida numa só estação?",
            correct_answer="Anuais",
            date=date.today()
        )

        self.stdout.write(self.style.SUCCESS('✅ Base de dados preenchida com sucesso!'))