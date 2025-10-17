from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta
from decimal import Decimal

from album.models import Album, Musica


class TesteModelAlbum(TestCase):
    """
    Conjunto de testes para os modelos Album e Musica.
    """

    def setUp(self):

        self.album = Album.objects.create(
            titulo='Abbey Road',
            artista='The Beatles',
            genero=2,  # Rock
            ano_lancamento=1969,
            tipo_album=3,  # Álbum Completo
            formato=2,  # Vinil
            idioma=2,  # Inglês
            preco=Decimal('150.00'),
            descricao='O 11º álbum de estúdio da banda.'
        )

        self.musica1 = Musica.objects.create(
            album=self.album,
            titulo='Come Together',
            duracao=timedelta(minutes=4, seconds=20)
        )

        self.musica2 = Musica.objects.create(
            album=self.album,
            titulo='Something',
            duracao=timedelta(minutes=3, seconds=2)
        )

    def test_criacao_album(self):
        """Verifica se os atributos do álbum foram criados corretamente."""
        self.assertEqual(self.album.titulo, 'Abbey Road')
        self.assertEqual(self.album.artista, 'The Beatles')
        self.assertEqual(self.album.ano_lancamento, 1969)
        self.assertEqual(self.album.preco, Decimal('150.00'))

    def test_criacao_musica(self):
        """Verifica se os atributos da música foram criados corretamente."""
        self.assertEqual(self.musica1.titulo, 'Come Together')
        self.assertEqual(self.musica1.album, self.album)
        self.assertEqual(self.musica1.duracao, timedelta(minutes=4, seconds=20))

    def test_metodo_str(self):
        """Verifica o retorno do método __str__ para Album e Musica."""
        self.assertEqual(str(self.album), 'Abbey Road')
        self.assertEqual(str(self.musica1), 'Come Together')

    def test_propriedade_duracao_total(self):
        """Verifica se a propriedade duracao_total calcula a soma corretamente."""
        duracao_esperada = self.musica1.duracao + self.musica2.duracao
        self.assertEqual(self.album.duracao_total, duracao_esperada)

    def test_metodos_relacionados_ao_ano(self):
        """Verifica os métodos e_novo e anos_desde_lancamento."""
        ano_atual = timezone.now().year

        # 1. Testa com um álbum antigo (de 1969)
        album_antigo = self.album
        self.assertFalse(album_antigo.e_novo(), "Um álbum de 1969 não deveria ser considerado novo.")
        self.assertEqual(album_antigo.anos_desde_lancamento(), ano_atual - 1969)

        # 2. Testa com um álbum lançado no ano atual
        album_novo = Album.objects.create(
            titulo='Lançamento do Ano',
            artista='Artista Novo',
            genero=1,
            ano_lancamento=ano_atual,
            tipo_album=1, formato=1, idioma=1, preco=Decimal('50.00')
        )
        self.assertTrue(album_novo.e_novo(), "Um álbum deste ano deve ser considerado novo.")
        self.assertEqual(album_novo.anos_desde_lancamento(), 0)

class TesteViewsListarAlbums(TestCase):
    """
    Conjunto de testes para a view ListarAlbums.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.album1 = Album.objects.create(
            titulo='Album A', artista='Artista X', genero=1, ano_lancamento=2020,
            tipo_album=1, formato=1, idioma=1, preco=Decimal('10.00'), descricao='...'
        )
        self.album2 = Album.objects.create(
            titulo='Album B', artista='Artista Y', genero=2, ano_lancamento=2021,
            tipo_album=2, formato=2, idioma=2, preco=Decimal('20.00'), descricao='...'
        )
        self.album3 = Album.objects.create(
            titulo='Outro Album', artista='Artista X', genero=1, ano_lancamento=2022,
            tipo_album=3, formato=3, idioma=1, preco=Decimal('30.00'), descricao='...'
        )

    def test_listar_albums_status_code(self):
        """Verifica se a página de listagem de álbuns carrega corretamente."""
        response = self.client.get(reverse('listar-albums'))
        self.assertEqual(response.status_code, 200)

    def test_listar_albums_template_usado(self):
        """Verifica se o template correto é usado para a listagem de álbuns."""
        response = self.client.get(reverse('listar-albums'))
        self.assertTemplateUsed(response, 'album/listar.html')

    def test_listar_albums_context_object_name(self):
        """Verifica se o nome do objeto de contexto está correto."""
        response = self.client.get(reverse('listar-albums'))
        self.assertIn('lista_albums', response.context)
        self.assertEqual(len(response.context['lista_albums']), 3)

    def test_listar_albums_busca_por_titulo(self):
        """Verifica se a busca por título funciona corretamente."""
        response = self.client.get(reverse('listar-albums') + '?q=Album A')
        self.assertEqual(len(response.context['lista_albums']), 1)
        self.assertEqual(response.context['lista_albums'][0], self.album1)

class TesteViewsEditarAlbuns(TestCase):
    """
    Conjunto de testes para a view EditarAlbums.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.album = Album.objects.create(
            titulo='Album Original', artista='Artista X', genero=1, ano_lancamento=2020,
            tipo_album=1, formato=1, idioma=1, preco=Decimal('10.00'), descricao='...'
        )

    def test_get(self):
        """Verifica se a requisição GET para editar álbum funciona corretamente."""
        response = self.client.get(reverse('editar-albums', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('musicas', response.context)

    def test_post(self):
        """Verifica se a requisição POST para editar álbum funciona corretamente."""
        response = self.client.post(reverse('editar-albums', args=[self.album.id]), {
            'titulo': 'Album Editado',
            'artista': 'Artista Y',
            'genero': 2,
            'ano_lancamento': 2021,
            'tipo_album': 2,
            'formato': 2,
            'idioma': 2,
            'preco': '20.00',
            'descricao': 'Descrição editada.'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso

        self.album.refresh_from_db()
        self.assertEqual(self.album.titulo, 'Album Editado')
        self.assertEqual(self.album.artista, 'Artista Y')
        self.assertEqual(self.album.genero, 2)
        self.assertEqual(self.album.ano_lancamento, 2021)
        self.assertEqual(self.album.preco, Decimal('20.00'))
        self.assertEqual(self.album.descricao, 'Descrição editada.')

    def test_editar_album_status_code(self):
        """Verifica se a página de edição de álbum carrega corretamente."""
        response = self.client.get(reverse('editar-albums', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)

    def test_editar_album_template_usado(self):
        """Verifica se o template correto é usado para a edição de álbum."""
        response = self.client.get(reverse('editar-albums', args=[self.album.id]))
        self.assertTemplateUsed(response, 'album/editar.html')

    def test_editar_album_atualizacao(self):
        """Verifica se a edição do álbum funciona corretamente."""
        response = self.client.post(reverse('editar-albums', args=[self.album.id]), {
            'titulo': 'Album Editado',
            'artista': 'Artista Y',
            'genero': 2,
            'ano_lancamento': 2021,
            'tipo_album': 2,
            'formato': 2,
            'idioma': 2,
            'preco': '20.00',
            'descricao': 'Descrição editada.'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso

        self.album.refresh_from_db()
        self.assertEqual(self.album.titulo, 'Album Editado')
        self.assertEqual(self.album.artista, 'Artista Y')
        self.assertEqual(self.album.genero, 2)
        self.assertEqual(self.album.ano_lancamento, 2021)
        self.assertEqual(self.album.preco, Decimal('20.00'))
        self.assertEqual(self.album.descricao, 'Descrição editada.')    
