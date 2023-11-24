# Installation

To install crudify, use the following pip command:

```bash
pip install crudify

### `docs/configuration.md`

```markdown
# Configuration

After installing crudify, you need to configure it in your Django project.

1. Add 'ModelMagicAPI' to your `INSTALLED_APPS` in your Django project's `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'ModelMagicAPI',
    # ...
]

from modelmagicapi.utils import router, generate_swagger_schema

urlpatterns = [
    # Your other URL patterns
    path('api/', include(router.urls)),
    path('swagger/', generate_swagger_schema(title="Test Apis", version='v1').with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')

]

(Optional) Configure the models you want to expose by adding the following to your project's settings.py:

AUTO_API_USER_MODELS = ['app_name.Model1', 'app_name.Model2']


### `docs/usage.md`

```markdown
# Usage

After completing the installation and configuration, the CRUD APIs for the specified models will be available at `/api/`.


