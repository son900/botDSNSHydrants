from django.views.generic import TemplateView

from src.hydrants.dependencies import get_hydrants_import_service
from src.hydrants.forms import ImportForm
from src.hydrants.services.import_service import HydrantsImportService


# Create your views here.


class HydrantsImportView(TemplateView):
    """
    Hydrant import view.
    """

    template_name = "hydrants/index.html"
    import_form = ImportForm

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        context = super().get_context_data(**kwargs)
        context["import_form"] = self.import_form
        return context

    def post(self, request, *args, **kwargs):
        """
        Check is ajax request and form is valid.
        """
        form = self.import_form(
            request.POST or None,
            request.FILES or None,
        )

        if form.is_valid():
            file = form.cleaned_data.get("file")
            hydrants_import_service: HydrantsImportService = get_hydrants_import_service()
            file_data = file.read()

            sheet = hydrants_import_service.get_sheet(file_data)
            data = hydrants_import_service.read_data(sheet)
            hydrants_import_service.bulk_create_or_update_hydrants(
                hydrants_list=data
            )

        return self.render_to_response(self.get_context_data(form=form))





