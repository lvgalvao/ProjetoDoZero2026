# Aquecimento: Git, pytest e CI/CD na mão

Três exercícios curtos: Git logo no começo, pytest e CI/CD depois do uv. A ideia é sentir na pele o que o agente vai fazer depois: quebrar, perceber que quebrou e voltar atrás.

Tudo roda numa pasta nova, fora deste repositório. No Windows, use o Git Bash.

## 1. Git: o botão de desfazer

```bash
mkdir projeto01
cd projeto01
```

Crie o `main.py` no editor:

```python
print("meu primeiro código python")
```

```bash
python main.py                      # meu primeiro código python
git init
git add main.py
git status                          # main.py pronto para o commit
git commit -m "meu primeiro commit"
```

Agora quebre de propósito: apague o `)` do final e salve.

```bash
python main.py                      # SyntaxError: '(' was never closed
git status                          # modified: main.py
git diff                            # mostra exatamente o que mudou
git restore main.py                 # volta para o último commit
python main.py                      # funciona de novo
```

**Por que importa:** o agente edita vários arquivos de uma vez. Com commit pequeno e frequente, qualquer estrago vira um `git diff` para entender e um `git restore` para desfazer.

## 2. pytest: o teste que avisa

Ainda na pasta `projeto01`:

```bash
uv init                             # cria pyproject.toml e .python-version
echo "__pycache__/" > .gitignore
uv add --dev pytest                 # dependência sempre com uv add
```

Crie `calculos.py`:

```python
def somar(a, b):
    return a + b
```

Crie `test_calculos.py`:

```python
from calculos import somar


def test_somar():
    assert somar(2, 3) == 5
```

```bash
uv run pytest -q                    # 1 passed
git add .
git commit -m "soma com teste"
```

Quebre: troque `a + b` por `a - b` e salve.

```bash
uv run pytest -q                    # FAILED ... assert -1 == 5
git restore calculos.py
uv run pytest -q                    # 1 passed
```

**Por que importa:** o teste é a regra que não depende de ninguém lembrar. Quando o agente muda o código, `pytest` diz na hora se ele quebrou algo. Neste projeto, o hook não deixa o agente dizer "pronto" com teste vermelho.

## 3. CI/CD: testar e entregar sozinho

**CI** (integração contínua): a cada push, uma máquina limpa instala tudo e roda os testes. **CD** (entrega contínua): só se os testes passaram, o código é entregue: roda, publica ou faz deploy.

A máquina do GitHub instala as dependências com `pip`, a partir de um `requirements.txt`. Crie o arquivo com o pytest:

```bash
echo "pytest" > requirements.txt
```

Crie `.github/workflows/ci.yml`:

```yaml
name: CI/CD

# Quando o pipeline roda
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # ---------- CI: integração contínua ----------
  test:
    name: CI - Testes
    runs-on: ubuntu-latest
    steps:
      - name: Baixar o código
        uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependências
        run: pip install -r requirements.txt

      - name: Rodar testes
        run: pytest -v

  # ---------- CD: entrega contínua ----------
  deploy:
    name: CD - Deploy
    needs: test                     # só roda se os testes passarem
    if: github.event_name == 'push' # só no push para a main (não em PR)
    runs-on: ubuntu-latest
    steps:
      - name: Baixar o código
        uses: actions/checkout@v4

      - name: Empacotar a aplicação
        run: |
          mkdir -p dist
          cp main.py dist/
          echo "Build gerado em $(date)" > dist/build-info.txt

      - name: Publicar artefato
        uses: actions/upload-artifact@v4
        with:
          name: app
          path: dist/

      - name: Deploy (simulado)
        run: echo "🚀 Deploy da versão ${{ github.sha }} realizado com sucesso!"
```

- `on`: quando roda (push e pull request na main).
- `test`: o CI. Máquina Linux nova, Python 3.12, `pip install -r requirements.txt` e `pytest -v`.
- `deploy`: o CD. `needs: test` faz esperar o verde; `if` limita ao push (PR só testa). Empacota o `main.py` em `dist/`, publica como artefato (baixável na aba Actions) e simula o deploy. Num projeto real, esse passo é o deploy ou a pipeline (neste repositório, o `diario.yml` roda a pipeline todo dia às 9h).

```bash
git add .
git commit -m "ci/cd com pytest"
gh repo create projeto01 --private --source=. --push
gh run watch                        # ou a aba Actions no GitHub: CI - Testes e CD - Deploy verdes
```

Quebre e mande para o GitHub:

```bash
# troque a + b por a - b e salve
git commit -am "quebrei a soma"
git push                            # CI - Testes vermelho, CD - Deploy nem roda
git revert HEAD --no-edit           # cria um commit que desfaz o anterior
git push                            # verde de novo, e o deploy roda
```

**Por que importa:** `git restore` desfaz o que ainda não foi commitado. Depois do push, quem desfaz é o `git revert`, que não reescreve o histórico. E o CI é a última barreira: mesmo que você esqueça de rodar o teste, o GitHub roda.

## Os comandos numa tela

| Para quê | Comando |
|---|---|
| Onde estou, o que mudou | `pwd` · `git status` · `git diff` |
| Guardar uma foto | `git add .` · `git commit -m "..."` |
| Desfazer antes do commit | `git restore arquivo` |
| Desfazer depois do push | `git revert HEAD --no-edit` |
| Dependência | `uv add pacote` · `uv add --dev pytest` |
| Testar | `uv run pytest -q` |
| Publicar | `gh repo create ... --push` · `git push` |

Ensaiado em 24/10/2026: os exercícios 1 e 2 com uv 0.6 e Python 3.13; os passos do workflow (`pip install -r requirements.txt`, `pytest -v` e o empacotamento em `dist/`) rodaram localmente com Python 3.12. O workflow é o que o Luciano já usa em aula.
