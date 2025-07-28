import random

import factory
from django.db import IntegrityError
from factory.django import DjangoModelFactory

from authentication.tests.factories import UserFactory
from coupons.models import Coupon, Redemption

coupons_options = [
    ("MONSTERDASEG", "Uma bebida Monster grátis na Segundona"),
    ("CAFEDOCEO", "Café premium liberado por conta do CEO (só hoje!)"),
    ("UBERTOFIM", "Uber para casa no fim do sprint (sem julgamentos)"),
    ("PIZZADODEV", "Pizza grátis para bugs acima de 500 linhas"),
    ("IFOODCHORA", "R$25 de Ifood porque hoje ninguém cozinhou"),
    ("CODGAMERPASS", "1 mês de Game Pass porque codar cansa a alma"),
    ("CAFELOOP", "Café infinito até você sair do loop"),
    ("ALMOCOFANTASMA", "Almoço grátis quando o deploy falha e ninguém sabe por quê"),
    ("SUSHINAFRIA", "Sushi congelado só pra quem ficou até depois das 20h"),
    ("BURGERDABRABA", "Combo do Brabo liberado pra quem mergeia sem conflito"),
    ("DESCONTOBUG", "Desconto para cada bug resolvido antes do meio-dia"),
    ("TAXIDODEV", "Corrida de táxi grátis após call traumática"),
    ("HAPPYHOURQA", "Vale-bebida por aguentar o QA encontrando tudo"),
    ("PASTELDEPROD", "Pastel na faixa pra reunião que podia ser e-mail"),
    ("SORVETEDOTESTE", "Sorvete liberado quando o teste finalmente passa"),
    ("GASOLINADEV", "Cupom simbólico: 'Combustível moral' pós deploy"),
    ("PAUSAPOMODORO", "Vale-snack pra cada Pomodoro cumprido com honra"),
    ("MERGESEMDRAMA", "Benefício simbólico: você conseguiu mergear sem tretar"),
    ("ZAPZAPREUNIAO", "Cupom de lanche se você mutou o mic a tempo na daily"),
    ("LANCHEOFFBYONE", "Vale-lanche pra quem sofreu com o erro off-by-one"),
    ("DEPLOYNASEXTA", "Cupom de coragem: você fez deploy na sexta-feira 😱"),
    ("SQLDABOA", "Pizza liberada para a query que rodou de primeira"),
    ("ZOMBIESTANDUP", "Café + pão de queijo pra quem abriu o olho na daily"),
    ("PIXDOCEO", "PIX emocional do CEO (mentira, mas vale um snack)"),
    ("CODENOLIMBO", "Vale energético pra código que ninguém entende"),
    ("RAMENDEBUG", "Lamen gourmet por cada bug que você não causou (provavelmente)"),
    ("CHURRASDOFEEDBACK", "Cupom por sobreviver à 1:1 sem surtar"),
    ("BRIEFDABRABA", "Almoço free se você entendeu o briefing de primeira"),
    ("CAFESEMIF", "Café extra por cada `if` removido no refactor"),
    ("NAOTEMBUG", "Snack misterioso: funciona na minha máquina™"),
    ("FOCOTOTAL", "Água com gás e moral elevada pra foco total no sprint"),
    ("DOCECRITICAL", "Doce de consolo por bug em produção no fim de semana"),
    ("CATCHERXPERT", "Refri liberado por capturar uma exception como um ninja"),
    ("REVIEW5ESTRELAS", "Cupom gourmet pra review sem apontamento"),
    ("BACKLOGPIZZA", "Lanche premiado por limpar 5 cards do backlog"),
    ("SPRINTFUGIDA", "Bolacha + sumo: pra quem tentou fugir da retro"),
    ("MUTEOPORTA", "Café grátis se você mutou o microfone antes do cachorro latir"),
    ("BONUSKAFKA", "Shot de expresso pra cada tópico Kafka que você entende"),
    ("FIXEIBONITO", "Cookie dourado por resolver um bug com elegância"),
    ("STANDUPEXPRESS", "Lanche premiado por standup de menos de 2 minutos"),
    (
        "REUNIÃOQUEPODIA",
        "Um café grátis por cada reunião que podia ser um e-mail (limite: infinito)",
    ),
    ("BUGFEATURE", "Cupom de chocolate por convencer alguém que é feature, não bug"),
    ("NAOMAISNEMMENOS", "Água da casa por seguir requisitos 'claramente ambíguos'"),
    ("SOBREVIVISPRINT", "Snack por sobreviver ao sprint com o time 'focado' no WhatsApp"),
    ("NAOMEXENOSEUCOD", "Bala de menta por não reescrever o código legado (ainda)"),
    ("CODOPRODCEO", "Chá calmante após push do CEO direto em produção"),
    ("COMITESEMTESTE", "Mini doce por aprovar PR sem testes e sem culpa"),
    ("FEEDBACKCORTES", "Coxinha emocional por feedback 'construtivo' com passivo-agressivo"),
    ("BRIEFINGQUEM", "Café grátis pra quem descobriu o briefing durante o deploy"),
    ("HOTFIXDAALEGRIA", "Red Bull por fazer hotfix às 23h e sorrir às 9h na daily"),
    ("ZAPDURANTESTAND", "Bolacha por responder grupo da família no meio da standup"),
    ("REFACTORINFAME", "Chiclete sabor arrependimento por mexer em método de 300 linhas"),
    ("COMMITDEUS", "Água com gás premium por commit com mensagem: 'ajustes gerais'"),
    ("ESCOPODINAMICO", "Salaminho premiado por lidar com escopo 'mutante' em tempo real"),
    ("QAOUDEUS", "Recompensa simbólica por testes rodando direto em produção"),
    ("TRAVOUEDEUS", "Balinha por usar a clássica solução: 'reinicia e vê se volta'"),
    ("NAOSEIALINEA", "Kit sobrevivência após explicar para a linha de negócios o que é API"),
    ("JUNTOEMISTURADO", "Refri por deploy, debug e daily acontecendo simultaneamente"),
    ("FEITOEMPROD", "Troféu moral: se funcionou em produção, tá validado"),
    ("SINDICATODODEV", "Biscoito de direito trabalhista simbólico por código escrito pós 22h"),
]


class CouponFactory(DjangoModelFactory):
    class Meta:
        model = Coupon

    code = factory.LazyAttribute(lambda _: random.choice(coupons_options)[0])
    description = factory.LazyAttribute(lambda o: dict(coupons_options)[o.code])
    max_redemptions = factory.Faker("random_int", min=1, max=10)
    available = factory.Faker("boolean", chance_of_getting_true=75)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                instance = super()._create(model_class, *args, **kwargs)
                return instance
            except IntegrityError as e:
                if attempt == max_attempts - 1:
                    raise
                # Gera um novo código aleatório
                kwargs["code"] = random.choice(coupons_options)[0]
                kwargs["description"] = dict(coupons_options)[kwargs["code"]]
                continue


class RedemptionFactory(DjangoModelFactory):
    class Meta:
        model = Redemption

    user = factory.SubFactory(UserFactory)
    coupon = factory.SubFactory(CouponFactory)
