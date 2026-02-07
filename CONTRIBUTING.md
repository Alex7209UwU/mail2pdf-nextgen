# Guide de Contribution à Mail2PDF NextGen

Merci de votre intérêt pour contribuer à Mail2PDF NextGen ! 🎉

Ce document fournit des lignes directrices pour contribuer au projet.

---

## 📋 Table des Matières

- [Code de Conduite](#code-de-conduite)
- [Comment Contribuer](#comment-contribuer)
- [Rapporter un Bug](#rapporter-un-bug)
- [Proposer une Fonctionnalité](#proposer-une-fonctionnalité)
- [Soumettre une Pull Request](#soumettre-une-pull-request)
- [Style de Code](#style-de-code)
- [Tests](#tests)
- [Documentation](#documentation)

---

## 🤝 Code de Conduite

En participant à ce projet, vous vous engagez à respecter notre communauté. Soyez respectueux, constructif et professionnel.

---

## 💡 Comment Contribuer

Il existe plusieurs façons de contribuer:

1. **Rapporter des bugs** - Aidez-nous à identifier et corriger les problèmes
2. **Proposer des fonctionnalités** - Suggérez de nouvelles idées
3. **Améliorer la documentation** - Clarifiez, corrigez ou étendez la doc
4. **Soumettre du code** - Corrigez des bugs ou implémentez des fonctionnalités
5. **Tester** - Testez les nouvelles versions et rapportez vos retours

---

## 🐛 Rapporter un Bug

Avant de rapporter un bug:

1. **Vérifiez les issues existantes** - Votre bug a peut-être déjà été rapporté
2. **Vérifiez avec la version actuelle** - Assurez-vous d'utiliser la dernière version
3. **Isolez le problème** - Essayez de créer un cas de test minimal

### Créer un Bug Report

Utilisez le [template de bug report](.github/ISSUE_TEMPLATE/bug_report.md) et incluez:

- **Description claire** du problème
- **Étapes pour reproduire** le bug
- **Comportement attendu vs réel**
- **Environnement** (OS, Python version, etc.)
- **Logs d'erreur** si disponibles
- **Screenshots** si pertinents

---

## ✨ Proposer une Fonctionnalité

Avant de proposer une fonctionnalité:

1. **Vérifiez les issues existantes** - Peut-être déjà proposée
2. **Lisez la roadmap** (si disponible) - Alignement avec la vision du projet
3. **Considérez les alternatives** - Y a-t-il d'autres façon de résoudre le problème?

### Créer une Feature Request

Utilisez le [template de feature request](.github/ISSUE_TEMPLATE/feature_request.md) et incluez:

- **Problème à résoudre** - Quel besoin cette fonctionnalité comble-t-elle?
- **Solution proposée** - Comment ça devrait fonctionner?
- **Cas d'usage** - Exemples concrets d'utilisation
- **Bénéfices** - Pourquoi c'est important?

---

## 🔧 Soumettre une Pull Request

### Workflow

1. **Fork le projet** sur GitHub
2. **Créez une branche** depuis `main`:
   ```bash
   git checkout -b feature/ma-super-fonctionnalite
   ```
3. **Faites vos modifications**
4. **Commitez** avec des messages clairs:
   ```bash
   git commit -m "feat: ajout de la fonctionnalité X"
   ```
5. **Pushez** vers votre fork:
   ```bash
   git push origin feature/ma-super-fonctionnalite
   ```
6. **Ouvrez une Pull Request** vers `main`

### Bonnes Pratiques pour les PRs

- ✅ **Une PR = Une fonctionnalité** - Gardez les PRs focalisées
- ✅ **Tests** - Ajoutez des tests pour votre code
- ✅ **Documentation** - Mettez à jour la doc si nécessaire
- ✅ **Commits** - Utilisez des messages de commit clairs
- ✅ **Description** - Expliquez POURQUOI et COMMENT dans la PR
- ✅ **Revue** - Répondez aux commentaires de revue

### Format des Commits

Utilisez [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: ajouter support pour format PST
fix: corriger parsing des accents dans MSG
docs: mettre à jour README avec exemples
style: formater code avec black
refactor: simplifier logique d'encodage
test: ajouter tests pour MBOX
chore: mettre à jour dépendances
```

---

## 🎨 Style de Code

### Python

- **PEP 8** - Suivre le guide de style Python
- **Black** - Formater le code avec Black:
  ```bash
  black .
  ```
- **Type Hints** - Ajouter des annotations de types quand possible
- **Docstrings** - Documenter les fonctions/classes avec docstrings
- **Nommage** - Utilisez des noms descriptifs

### Exemple

```python
def convert_email(file_path: str, output_dir: str) -> Optional[str]:
    """
    Convert an email file to PDF.
    
    Args:
        file_path: Path to the email file
        output_dir: Directory for the output PDF
    
    Returns:
        Path to the generated PDF, or None if error
    """
    pass
```

---

## 🧪 Tests

### Exécuter les Tests

```bash
# Tous les tests
python -m pytest tests/

# Tests spécifiques
python -m pytest tests/test_ui_config.py

# Avec coverage
python -m pytest tests/ --cov=.
```

### Écrire des Tests

- **Un test par comportement** - Testez une chose à la fois
- **Noms descriptifs** - `test_convert_email_with_invalid_format`
- **Arrange, Act, Assert** - Structure claire
- **Fixtures** - Utilisez pytest fixtures pour le setup

### Exemple

```python
def test_convert_email_success():
    # Arrange
    converter = EmailConverter()
    test_file = "test.eml"
    
    # Act
    result = converter.convert_email(test_file, "output/")
    
    # Assert
    assert result is not None
    assert Path(result).exists()
```

---

## 📚 Documentation

### Types de Documentation

1. **README.md** - Aperçu et quick start
2. **FULL_DOCUMENTATION.md** - Documentation technique détaillée
3. **Docstrings** - Documentation inline du code
4. **Comments** - Explications pour code complexe

### Bonnes Pratiques

- ✅ **Clarté** - Écrivez pour être compris facilement
- ✅ **Exemples** - Incluez des exemples concrets
- ✅ **À jour** - Mettez à jour la doc avec le code
- ✅ **Français** - Privilégiez le français (projet français)

---

## ❓ Questions?

- 💬 [Discussions GitHub](https://github.com/Alex7209UwU/mail2pdf-nextgen/discussions)
- 🐛 [Issues](https://github.com/Alex7209UwU/mail2pdf-nextgen/issues)
- 📧 Email: alexis.giroudspro@outlook.fr

---

## 🙏 Remerciements

Merci pour vos contributions! Chaque contribution, petite ou grande, est appréciée. 💙

---

**Happy Coding!** 🚀

Mail2PDF NextGen v1.0.0  
Ville de Fontaine 38600, France
